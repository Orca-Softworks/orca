from ..node import Node
from ..neuron import Neuron
import time


class Network(Node):
    """
    A Network is a type that may have many inputs and many outputs.
    It consists of collections of neuorons and other networks.

    Args:
        Node (_type_): _description_
    """

    def __init__(
        self,
        name,
        # https://peps.python.org/pep-0484/#forward-references
        parts: list["Neuron|Network"],
        multi_cycle: bool = False,
        dispatch_rate = None,
        **kwargs,
    ):
        """_summary_

        Args:
            neurons (list[Neuron]): _description_
            networks (list[Network], optional): _description_. Defaults to [].
            multi_cycle (bool, optional): _description_. Defaults to False.
        """
        Node.__init__(self, name, **kwargs)

        self.parts = parts
        self.multi_cycle = multi_cycle
        self.dispatch_rate = dispatch_rate

        self._unresolved_inputs = []
        self._registry = {}
        self._execution = []

        # need to collect inputs from all neurons that are not resolved.
        for part in self.parts:
            self._unresolved_inputs.extend(part._unresolved_inputs)

        # register all unresolved inputs with the network
        # attempt to resolve each neuron against the registry
        # iterate over each neuron that is not already resolved,

    def attempt_to_resolve_query(self, query):
        pass

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

    def compute(self):
        time.sleep(self.dispatch_rate)
        for part in self._execution:
            part.compute()
