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
settings['threshold'] = -54
settings['left_window_constant'] = 20#(t+)
settings['right_window_constant'] = 20#(t-)
settings['learning_rate'] = 0.05# (A+)
settings['stability'] = 1.05# (B)
settings['weight_ceiling'] = 1.0
c = 0.7
unshared_pool_settings = {'alpha':2.5, 'k':1, 'a':0.4, 'b':30, 'c':c, 'd':-3.5}
shared_pool_settings = {'alpha':2.5, 'k':1, 'a':0.75, 'b':65, 'c':1-c, 'd':-5}
inhibitory_intensy = 8.2
noise_intensy = 8.2

pool_a = Inhibitory_Pool('pool', 0, -inhibitory_intensy, 3.0, unshared_pool_settings)
pool_b = Inhibitory_Pool('pool', 1, -inhibitory_intensy, 3.0, unshared_pool_settings)
shared_pool = Inhibitory_Pool('pool', 2, -inhibitory_intensy, 3.0, shared_pool_settings)
current_a = Current('current', 0, 'current', 20.7)
current_b = Current('current', 1, 'current', 21.5)
neuron_a = Neuron('neuron', 0, settings, 'off')
neuron_b = Neuron('neuron', 1, settings, 'off')
noise_a_pos = Noise('noise', 0, 100, noise_intensy, 3.0)
noise_a_neg = Noise('noise', 1, 100, -noise_intensy, 3.0)
noise_b_pos = Noise('noise', 2, 100, noise_intensy, 3.0)
noise_b_neg = Noise('noise', 3, 100, -noise_intensy, 3.0)

set = [pool_a, pool_b, shared_pool, current_a, current_b, neuron_a, neuron_b, noise_a_pos, noise_a_neg, noise_b_pos, noise_b_neg]

#pool_a.connect(neuron_a)
#neuron_a.connect(pool_a)
#pool_b.connect(neuron_b)
#neuron_b.connect(pool_b)
#shared_pool.connect(neuron_a)
#shared_pool.connect(neuron_b)
#neuron_a.connect(shared_pool)
#neuron_b.connect(shared_pool)

current_a.connect(neuron_a)
current_b.connect(neuron_b)

noise_a_pos.connect(neuron_a)
noise_a_neg.connect(neuron_a)
noise_b_pos.connect(neuron_b)
noise_b_neg.connect(neuron_b)

for i in range(10000):
    for neuron in set:
        event = Event(name = 'update')
        simpy.activate(event, event.update(neuron), delay = i)

simpy.simulate(until = 10000.0)

print(len(neuron_a.spikes_record), len(neuron_b.spikes_record))
outfile_a = open('no_inhib_a.txt', 'w')
#outfile_a = open('inhib_a.txt', 'w')
for i in neuron_a.spikes_record:
    outfile_a.write(str(i)+'\n')

outfile_b = open('no_inhib_b.txt', 'w')
#outfile_b = open('inhib_b.txt', 'w')
for i in neuron_b.spikes_record:
    outfile_b.write(str(i)+'\n')
    
#x = list(range(len(neuron_a.spikes_record)))
#plot.plot(x, neuron_a.spikes_record, x, neuron_b.spikes_record)
#plot.plot(x, shared_pool.spikes_record)
#plot.show()




