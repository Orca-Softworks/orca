from ..base import *


def delayed_output_neuron(
    output: Neuron,
    variable_delay: Neuron = None,
    constant_delay: str = None,
    delay_unit: str = "ms",
):
    # if variable_delay != None and constant_delay != None:
    #     raise Exception("Cannot set both variable_delay and constant_delay.")

    delay_input = None

    if variable_delay:
        delay_input = Input(
            "delay", types=f"u16_{delay_unit}", connect_to=variable_delay
        )

    if constant_delay:
        delay_input = Input("delay", types=f"u16_{delay_unit}", constant=constant_delay)

    if delay_input == None:
        raise Exception("Did not create any sort of delay time input!")

    return Neuron(
        f"{output.name}_delayed",
        output.output_type,
        [
            Input("output_to_delay", output.output_type, connect_to=output),
            delay_input,
        ],
        implementation="delayed_output.rs/delayed_output",
        track_change=True,
        multi_cycle=True,
    )


def delayed_output_network(output, delay):
    pass
