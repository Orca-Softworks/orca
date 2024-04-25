from ..base import Neuron

class SecondNanosecondNeuron(Neuron):
    def __init__(self, *args, **kwargs):
        super().__init__(args.name, "u64.unit(second)&u32.unit(attosecond)", *args, **kwargs)

second_attosecond = Neuron(
    "second_attosecond",
    "(u64, u64)",
    "", # TODO, how do we want to handle putting impls to these?
)


SECOND_NANOSECOND_TIME_TYPE = "(u64, u32)"
ACCURATE_TIME_TYPE = "(u64, u64)"

time = Neuron("time", "(u64, u32)" "seconds", "nanos")
