from .. node import Node


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

