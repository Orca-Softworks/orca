from neuron.base import *


def shared(self, i):
    self.output = i.input


one = Neuron(
    "one",
    "bool",
    shared,
    inputs=[Input("input", "bool", "two", initial_value=False)],
)

two = Neuron(
    "two",
    "bool",
    shared,
    inputs=[Input("input", "bool", "one", feedback=True)],
)

net = Network(
    "network",
    [one, two],
    dispatch_rate=1,
)

net.run()
