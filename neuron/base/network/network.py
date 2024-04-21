
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
