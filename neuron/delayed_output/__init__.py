from ..base import *


def delayed_output_neuron(output, delay_value, delay_unit="ms"):
    return Neuron(
        f"{output.name}_delayed",
        output.output_type,
        [
            Input("prior_output", output.output_type, connect_to=output),
            # TODO does type constriction need a query language? Should it just be custom
            # behavior?
            Input("delay", types=f"u16,{delay_unit}", constant=delay_value),
        ],
        # TODO impl is not required for certain things like validating the network
        implementation="delayed_output.rs/delayed_output",
        track_change=True,
        multi_cycle=True,
    )


def delayed_output_network(output, delay):
    pass
