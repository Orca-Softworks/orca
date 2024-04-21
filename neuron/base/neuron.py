import typing

NAME = "Neuron"
# Brain, Neuron, Pyramid, Nw, NNW, Nnw, nnw,

RESERVED_WORDS = [
    "out",
]


# need to use this for parsing rust input files.
class RustTranslator:
    pass


class Node:
    def __init__(
        self,
        name,
        description="",
        tags=[],
        visibility="**/*",
    ):
        # Gives this component
        self.name = name
        # lets us describe, in human terms, what this does
        self.description = description
        # allows to append whatever sorts of tags we want to this component
        self.tags = tags
        # allows us to limit those that can see this part of the network.
        self.visibility = visibility

        if self.name in RESERVED_WORDS:
            self.error(
                f"""Cannot use '{self.name}' as your component name.
                See the list of reserved Orca words: {RESERVED_WORDS}"""
            )

    def validate(self):
        return

    def overview(self):
        return f"""
        name: {self.name}
        description: {self.description}
        tags: {self.tags}
        """

    def error(self, message):
        raise BaseException(
            f"""
        Bad {self.__class__.__name__}: {message}.
        {self.overview()}
        """
        )


class Input(Node):
    """_summary_

    Args:
        Node (_type_): _description_
    """

    def __init__(
        self,
        *args,
        # The type of the input. Can translate (sometimes) one type to
        # another.
        input_type,
        # The output we should listen to somewhere else in the graph.
        query=None,
        # If this input comes from an output somewhere later in the network.
        feedback=False,
        # If this input should resolve to multiple neurons.
        many=None,
        # The initial value, if this does not have a query
        initial_value=None,
        # If this value is really just a const.
        constant=False,
        # If we want to buffer values up to some count or duration.
        buffered=None,
        # We can average our value over some time period. Impl depends on
        # type.
        persistence=None,
        # we can auto generate an input that stores the latest write
        # time for us.
        save_latest_write_time=False,
        keeparound_duration="10_s",
        unit=None,
        track_disconnect=False,
        report_disconnect=False,
        big=False,
        **kwargs,
    ):
        Node.__init__(self, *args, **kwargs)

        # should be possible to come up with different translations schemes.
        self.input_type = input_type
        # If we should listen to some output.
        self.query = query
        # If this channel is fed back from a downstream calculation
        # into this one.
        self.feedback = feedback
        self.many = many
        self.initial_value = initial_value
        self.constant = constant
        self.buffered = buffered
        self.persistence = persistence
        self.save_latest_write_time = save_latest_write_time
        self.keeparound_duration = keeparound_duration
        self.unit = unit
        self.track_disconnect = track_disconnect
        self.report_disconnect = report_disconnect
        self.big = big

    def validate(self):
        super().validate()

        if self.query == None and self.initial_value == None:
            self.error("Cannot set query and initial value together.")

        if self.query != None and self.initial_value != None:
            self.error("Must set an initial value if there is not query.")

        # This input is going to have some set of resolved neurons based on its query.
        self._resolved_neurons = []

    def overview(self):
        return f"""
        {super().overview()}
        input_type: {self.input_type}
        query: {self.query}
        initial_value: {self.initial_value}
        """


class Neuron(Node):
    """_summary_

    Args:
        Node (_type_): _description_
    """

    def __init__(
        self,
        *args,
        output_type,
        impl_file,
        inputs=[],
        networks=[],
        multi_cycle=False,
        big=False,
        per_cycle_transmit=None,
        rate_limit_output=None,
        allow_heap=False,
        allow_spawning_networks=False,
        # Memoize will mean not emitting an output signal
        # if the value has not changed.
        memoize=False,
        # if we should check the connection status of our inputs each time
        # we do our calculation. If they are not connected, we can take some
        # action.
        connect_inputs=False,
        **kwargs,
    ):
        Node.__init__(self, *args, **kwargs)

        self.output_type = output_type
        self.inputs = inputs
        self.impl_file = impl_file
        self.networks = networks
        self.multi_cycle = multi_cycle
        self.big = big
        self.per_cycle_transmit = per_cycle_transmit
        self.rate_limit_output = rate_limit_output
        self.allow_heap = allow_heap
        self.allow_spawning_networks = allow_spawning_networks
        self.memoize = memoize
        self.connect_inputs = connect_inputs

    def validate(self):
        super().validate()
        return

    def overview(self):
        return f"""
        {super().overview()}
        type: {self.output_type}
        impl: {self.impl_file}
        inputs: {self.inputs}
        networks: {self.networks}
        multiCycle: {self.multi_cycle}
        visibility: {self.visibility}
        """


class Network(Node):
    """
    A Network is a type that may have many inputs and many outputs.
    It consists of collections of neuorons and other networks.

    Args:
        Node (_type_): _description_
    """
    def __init__(
        self,
        *args,
        neurons: list[Neuron],
        # https://peps.python.org/pep-0484/#forward-references
        networks: list['Network'] = [],
        multi_cycle: bool =False,
        **kwargs,
    ):
        """_summary_

        Args:
            neurons (list[Neuron]): _description_
            networks (list[Network], optional): _description_. Defaults to [].
            multi_cycle (bool, optional): _description_. Defaults to False.
        """
        Node.__init__(self, *args, **kwargs)

        self.neurons = {neuron.name: neuron for neuron in neurons}

        self.multi_cycle = multi_cycle
        self.networks = networks

    def validate(self):
        self.resolve_all_neurons()

    # TODO see about moving this to lower level components. Resolve
    def resolve_all_neurons(self):
        for neuron in self.neurons.values():
            self.resolve_single_neuron(neuron)

    def resolve_single_neuron(self, neuron_to_resolve):
        for input in neuron_to_resolve.inputs:
            self.resolve_single_input(input)

    def resolve_single_input(self, input_to_resolve):
        resolved_input_neurons = []

        if input_to_resolve.query == None:
            return

        for neuron in self.neurons.values():
            if input_to_resolve.query == f".{neuron.name}":
                resolved_input_neurons.append(neuron)

        if len(resolved_input_neurons) == 1 and input_to_resolve.many == None:
            # Acceptable condition.
            pass
        elif len(resolved_input_neurons) == 0 and input_to_resolve.query != None:
            # We specified a query, but did not get any resolved input.
            self.error(
                f"""
                Input: '{input_to_resolve.name}' resolved to no neurons despite having a query
                '{input_to_resolve.query}' specified.
            """
            )
        elif len(resolved_input_neurons) > 1 and input_to_resolve.many == None:
            self.error(
                f"""
                Input: {input_to_resolve} resolved to multiple input neurons: {resolved_input_neurons}
                but was not marked as "many". If you intended to resolve to many neurons, mark the input
                with "many=True". If this was not intended, check that your query will only resolve
                to a single input neuron.
            """
            )
        elif input_to_resolve.many != "infinite" and (
            input_to_resolve.many < len(resolved_input_neurons)
        ):
            self.error(
                f"""
                Input: {input_to_resolve} only expected to resolve up to {input_to_resolve.many} neurons.
                It instead resolved to {len(resolved_input_neurons)} neurons: {resolved_input_neurons}.
            """
            )

        input_to_resolve._resolved_neurons = resolved_input_neurons

    def overview(self):
        return f"""
        {super().overview()}
        Dispatch: {self.dispatch}
        Multi-Cycle: {self.multi_cycle}
        """
