from neuron.base import Neuron, Input, Network
from neuron.delay_bank import delay_bank

def valve(i, o):
    i.some_const

valves = [
    Neuron(
        f"valve_{i}",
        "bool",
        implementation=f"delay_bank.rs/outputs",
        inputs=[
            Input(f"some_variable", "u32", f"blah_{i}"),
            Input("some_const", "u32", "local", constant=i),
            Input(
                "banked_output",
                "bool",
                f"valve_{i}_output",
                feedback=True,
            ),
        ],
    )
    for i in range(0, 4)
]

delayed_valve_network = Network(
    "delayed_valve_network",
    # a network can contain other networks, or neurons
    valves,
    # TODO decide how to hook in
    networks=[delay_bank("delayed_valve_outputs", valves, 50)],
)
