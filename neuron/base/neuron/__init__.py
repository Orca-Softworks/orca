from ..node import Node
import time

class Neuron(Node):
    """_summary_

    Args:
        Node (_type_): _description_
    """

    def __init__(
        self,
        name: str,
        output_type: str,
        implementation: str = None,
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
        # if theres no dispatch rate, change re-compute always
        dispatch_rate=None,
        **kwargs,
    ):
        """_summary_

        Args:
            name (_type_): _description_

            data_type (String|): Data type is very special. It allows for a string type of data,
            which would be one of the primitives. It allows for a list of strings, of which
            these are enumerations. It TODO can also use a Network shape as its output,
            essentially encoding the network shape into a data stream. Its very common
            to then buffer this data shape into a "big" output. Man, idk if this the right
            way to construct this.

            implementation (_type_, optional): _description_. Defaults to None.
            inputs (list, optional): _description_. Defaults to [].
            networks (list, optional): _description_. Defaults to [].
            multi_cycle (bool, optional): _description_. Defaults to False.
            big (bool, optional): _description_. Defaults to False.
            per_cycle_transmit (_type_, optional): _description_. Defaults to None.
            rate_limit_output (_type_, optional): _description_. Defaults to None.
            allow_heap (bool, optional): _description_. Defaults to False.
            allow_spawning_networks (bool, optional): _description_. Defaults to False.
            memoize (bool, optional): _description_. Defaults to False.
            connect_inputs (bool, optional): _description_. Defaults to False.
        """
        Node.__init__(self, name, **kwargs)

        self.output_type = output_type
        self.inputs = inputs
        self.implementation = implementation
        self.networks = networks
        self.multi_cycle = multi_cycle
        self.big = big
        self.per_cycle_transmit = per_cycle_transmit
        self.rate_limit_output = rate_limit_output
        self.allow_heap = allow_heap
        self.allow_spawning_networks = allow_spawning_networks
        self.memoize = memoize
        self.connect_inputs = connect_inputs
        self.output = None
        self.dispatch_rate = dispatch_rate

        self._unresolved_inputs = [
            input for input in self.inputs if not input.get_resolved()
        ]

        self._resolved_inputs = [input for input in self.inputs if input.get_resolved()]

    def get_resolved(self):
        return all(input.get_resolved() for input in self.inputs)

    def overview(self):
        return f"""{super().overview()}type: {self.output_type}
        implementation: {self.implementation}
        inputs: {self.inputs}
        networks: {self.networks}
        multi_cycle: {self.multi_cycle}
        visibility: {self.visibility}\n"""

    def compute(self):
        if self.dispatch_rate:

        self.implementation(self, self.inputs)
