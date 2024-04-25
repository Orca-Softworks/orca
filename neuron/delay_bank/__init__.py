from neuron.core import *


def delay_bank(name, outputs, delay):
    output_states = [output.name for output in outputs]

    bank_controller = Neuron(
        f"{name}_bank_controller",
        # we say that this controller emits a string that is in this list. essentially an enum
        output_states,
        "delay_bank.rs/bank_controller",
        [
            # we decide to query the names directly.
            Input("valves", "bool", output_states, many=True),
            # We can use small data types to represent this date. We are very efficient this way.
            # TODO(lets see if we can improve the unit syntax there)
            Input("delay", "u8.unit(ms)", "local", constant=delay),
        ],
        networks=[],
        multi_cycle=True,
    )

    delayed_outputs = [
        Neuron(
            f"{output.name}_delayed",
            "bool",
            "delay_bank.rs/delayed",
            # you are allowed to use a neuron directly for a query
            Input("valve_input", "bool", output),
            Input("bank_allow", output_states, f"{name}_bank_controller"),
            multi_cycle=True,
        )
        for output in outputs
    ]

    return Network(
        f"{name}_delay_bank", [*delayed_outputs, bank_controller, *outputs], multi_cycle=True
    )
