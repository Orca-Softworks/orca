from orca.orca import Network, Neuron, Input


def custom_network(name):
    pass


# these starting_* Neurons will form the base Inputs of the Network
# we specify initial values since we dont know how the Network will
# be hooked together.
starting_1 = Neuron(
    "starting_1",
    "u32",
    "example_network.rs/starting_1",
    Input("data_1", "u32", constant=True, initial_value=10),
    Input("data_2", "u32", initial_value=1),
)

starting_2 = Neuron(
    "starting_2",
    "u32",
    "example_network.rs/starting_2",
    Input("data_1", "u32", constant=True, initial_value=5),
    Input("data_2", "u32", initial_value=1),
    # Neurons can have small instances of Networks inside that they can use to
    # do calculation. TODO How do I wire up with it?
    networks=[
        custom_network(
            "some_network_instance",
        )
    ],
)


# Typical for people to inherit and write custom behavior for
# neurons.
class MyNeuron(Neuron):
    def __init__(self, start_value):
        Neuron.__init__(
            self,
            f"intermediate_{start_value}",
            "u32",
            "example_network.rs/intermediate",
            Input("starting_1", "u32", query=".starting_1", dispatch_on="on_change"),
            # can also specify via query
            Input("starting_2", "u32", query=query(".starting_2")),
            Input("internal", "u32", initial_value=start_value),
            Input("feedback_1", "u32", query=".output_1", feedback=True),
            Input("feedback_1", ["one", "two" "three"]),
            # we can use the set of names from our input neurons in order to form
            # the set of words for our output.
            Input("type_based_on_inputs", [neuron.name for neuron in query(".starting_*")])
        )


many_neurons = [MyNeuron(i) for i in range(0, 10)]


output_1 = Neuron(
    "output_1",
    "u32",
    "example_network.rs/output_1",
    # TODO actually make this query match
    Input("many_into_one", "u32", many=10, query=".intermediate_*"),
)

# Networks can have many outputs, the Network fires altogether.
example_network = Network(
    "example_network",
    starting_1,
    starting_2,
    output_1,
    *many_neurons,
)
