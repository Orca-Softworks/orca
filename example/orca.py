import typing


class OrcaComponent:

    def __init__(self, name, description="", tags=[]):
        self.name = name
        self.description = description
        self.tags = tags

    def overview(self):
        return f"""Name: {self.name}
        Description: {self.description}
        Tags: {self.tags}"""

    def error(self, message):
        raise BaseException(
            f"""
        Bad {self.__class__.__name__}: {message}.
        {self.overview()}
        """
        )


class Input(OrcaComponent):
    def __init__(
        self,
        # The name of this input instance. Used as the variable name inside
        # the neuron implementation.
        name,
        # The type of the input. Can translate (sometimes) one type to
        # another.
        input_type,
        # The output we should listen to somewhere else in the graph.
        query=None,
        # If this input comes from an output somewhere later in the machine.
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
        description="",
        keeparound_duration="10_s",
        unit=None,
        track_disconnect=False,
        report_disconnect=False,
        big=False,
    ):
        OrcaComponent.__init__(self, name, description)

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

        if self.query == None and self.initial_value == None:
            self.error("Cannot set query and initial value together.")

        if self.query != None and self.initial_value != None:
            self.error("Must set an initial value if there is not query.")

        # This input is going to have some set of resolved neurons based on its query.
        self._resolved_neurons = []

    def overview(self):
        return f"""
        {super().overview()}
        Type: {self.input_type}
        Query: {self.query}
        Initial Value: {self.initial_value}
        """


# # you use a many input when you need to condense a list into
# # a single output variable.
# input("many_input", "f64", query="..start_data", many=True),
# # This is a channel where we always use the output from the last calculation.
# input("input_state", "=.**.name()", feedback=True),
# # This is an example of how we can assess
# input(
#     "reverse_many_input", "f64", "=.**.section[name].**.*", feedback=True
# ),
# # we can have inputs that are simply there for us to use. We can write to our
# # internal state, but it is never an output to others.
# input("internal_state", "f32", initial_value=instance_start_value),
# input("internal_state_read_only", "f32", constant=True),


class Neuron(OrcaComponent):
    def __init__(
        self,
        name,
        output_type,
        impl_file,
        *inputs,
        machines=[],
        tags=[],
        description="",
        multi_cycle=False,
        big=False,
        per_cycle_transmit=None,
        rate_limit_output=None,
        allow_heap=False,
        allow_spawning_machines=False,
        # Let anyone see this neuron output.
        visibility="**/*",
        # Memoize will mean not emitting an output signal
        # if the value has not changed.
        memoize=False,
        # if we should check the connection status of our inputs each time
        # we do our calculation. If they are not connected, we can take some
        # action.
        connect_inputs=False,
    ):
        OrcaComponent.__init__(self, name, description)

        self.output_type = output_type
        self.inputs = inputs
        self.impl_file = impl_file
        self.machines = machines
        self.tags = tags
        self.multi_cycle = multi_cycle
        self.big = big
        self.per_cycle_transmit = per_cycle_transmit
        self.rate_limit_output = rate_limit_output
        self.allow_heap = allow_heap
        self.allow_spawning_machines = allow_spawning_machines

    def overview(self):
        return f"""
        {super().overview()}
        Type: {self.output_type}
        Impl: {self.impl_file}
        Inputs: {self.inputs}
        Machines: {self.machines}
        MultiCycle: {self.multi_cycle}
        """


class Machine(OrcaComponent):
    def __init__(
        self,
        name,
        *neurons,
        description="",
        dispatch="follow_inputs",
        multi_cycle=False,
    ):
        OrcaComponent.__init__(self, name, description)

        self.neurons = {neuron.name: neuron for neuron in neurons}
        self.dispatch = dispatch
        self.multi_cycle = multi_cycle

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
