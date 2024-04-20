from orca import Machine, Neuron, Input


def custom_machine(name):
    pass


# these starting_* Neurons will form the base Inputs of the Machine
# we specify initial values since we dont know how the Machine will
# be hooked together.
starting_1 = Neuron(
    "starting_1",
    "u32",
    "example_machine.rs/starting_1",
    Input("data_1", "u32", constant=True, initial_value=10),
    Input("data_2", "u32", initial_value=1),
)

starting_2 = Neuron(
    "starting_2",
    "u32",
    "example_machine.rs/starting_2",
    Input("data_1", "u32", constant=True, initial_value=5),
    Input("data_2", "u32", initial_value=1),
    # Neurons can have small instances of Machines inside that they can use to
    # do calculation. TODO How do I wire up with it?
    # machines=[
    #     custom_machine(
    #         "some_machine_instance",
    #     )
    # ],
)


# Typical for people to inherit and write custom behavior for
# neurons.
class MyNeuron(Neuron):
    def __init__(self, start_value):
        Neuron.__init__(
            self,
            f"intermediate_{start_value}",
            "u32",
            "example_machine.rs/intermediate",
            Input("starting_1", "u32", query=".starting_1"),
            Input("starting_2", "u32", query=".starting_2"),
            Input("internal", "u32", initial_value=start_value),
            Input("feedback_1", "u32", query=".output_1", feedback=True),
        )


many_neurons = [MyNeuron(i) for i in range(0, 10)]


output_1 = Neuron(
    "output_1",
    "u32",
    "example_machine.rs/output_1",
    # TODO actually make this query match
    Input("many_into_one", "u32", many=10, query=".intermediate_*"),
)

# Machines can have many outputs, the Machine fires altogether.
example_machine = Machine(
    "example_machine",
    starting_1,
    starting_2,
    output_1,
    *many_neurons,
)
