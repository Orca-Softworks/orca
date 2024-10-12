from neuron.core import *
from neuron.delayed_output import delayed_output_neuron


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

    delayed_outputs = [delayed_output_neuron(output) for output in outputs]

    return Network(
        f"{name}_delay_bank",
        [*outputs, bank_controller, *delayed_outputs],
        multi_cycle=True,
    )
