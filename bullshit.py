import time

class Neuron:
    def __init__(self, name, init_1=0, init_2=1, init_3=False):
        self.name = name
        self.init_1 = init_1
        self.init_2 = init_2
        self.init_3 = init_3

    def output(self):
        self.init_1 = self.init_1 + self.init_2

        self.init_2 = self.init_1 / 2

        if self.init_2 > 10000:
            self.init_3 = not self.init_3
            self.init_1 = 0

        return self.init_2

    def compute_if(self):
        return True


neuron_1 = Neuron("neuron_1", init_1=1)
neuron_2 = Neuron("neuron_2", init_2=4)

class TimerNeuron:
    def __init__(self):
        self.start_time = time.time()

    def output(self):
        o = time.time() - self.start_time

        print(o)

        return o

    def compute_if(self):
        return True

timer_neuron = TimerNeuron()

class Network:
    def __init__(self, timer_neuron, *neurons):
        self.diff_time = 0
        self.timer_neuron = timer_neuron
        self.neurons = neurons

    def output(self):

        print(self.diff_time)

        for neuron in self.neurons:
            if neuron.compute_if():
                output = neuron.output()
                print(f"{neuron.name} output: {output}")

    def compute_if(self):
        self.diff_time = self.timer_neuron.output() - self.diff_time
        if self.diff_time > 1.0:
            self.diff_time = 0
            return True
        else:
            return False

network_1 = Network(timer_neuron, neuron_1, neuron_2)

network_1.output()
while True:
    if network_1.compute_if():
        network_1.output()
