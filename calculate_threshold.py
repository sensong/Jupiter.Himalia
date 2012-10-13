from Stimulator import Constant_Stimulator as Current
from Stimulator import Current_Poisson_Stimulator as Noise
from Stimulator import Current_Poisson_Pool as Inhibitory_Pool
from LIF_STDP_Neuron import LIF_STDP_Neuron as Neuron
from LIF_STDP_Neuron import Event
import SimPy.Simulation as simpy
#import matplotlib.pyplot as plot
import random
import numpy
import matplotlib.pyplot as plot

settings = {}
settings['reset_potential'] = -70
settings['spike_potential'] = 0
settings['threshold'] = -66.6
settings['left_window_constant'] = 20#(t+)
settings['right_window_constant'] = 20#(t-)
settings['learning_rate'] = 0.05# (A+)
settings['stability'] = 1.05# (B)
settings['weight_ceiling'] = 1.0

current_a = Current('current', 0, 'current', 26.6, 3.0)
neuron_a = Neuron('neuron', 0, settings, 'off')

set = [current_a, neuron_a]
current_a.connect(neuron_a)

for i in range(20):
    for neuron in set:
        event = Event(name = 'update')
        simpy.activate(event, event.update(neuron), delay = i)

simpy.simulate(until = 20.0)
    
x = list(range(len(neuron_a.spikes_record)))
plot.plot(x, neuron_a.spikes_record)
plot.show()




