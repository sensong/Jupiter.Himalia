from Stimulator import Constant_Stimulator as Current
from Stimulator import Current_Poisson_Stimulator as Noise
from Stimulator import Current_Poisson_Pool as Inhibitory_Pool
from LIF_STDP_Neuron import LIF_STDP_Neuron as Neuron
from LIF_STDP_Neuron import Event
import SimPy.Simulation as simpy
import matplotlib.pyplot as plot
import random
import numpy

ex_settings = {}
ex_settings['reset_potential'] = -54.5
ex_settings['spike_potential'] = 0
ex_settings['threshold'] = -45.5
ex_settings['left_window_constant'] = 20#(t+)
ex_settings['right_window_constant'] = 20#(t-)
ex_settings['learning_rate'] = 0.05# (A+)
ex_settings['stability'] = 1.05# (B)
ex_settings['weight_ceiling'] = 1.0
ex_settings['type'] = 'current'
ex_settings['output_current_decay'] = 3.0
ex_settings['output_current_peak'] = 0.55

in_settings = {}
in_settings['reset_potential'] = -54.5
in_settings['spike_potential'] = 0
in_settings['threshold'] = -45.5
in_settings['left_window_constant'] = 20#(t+)
in_settings['right_window_constant'] = 20#(t-)
in_settings['learning_rate'] = 0.05# (A+)
in_settings['stability'] = 1.05# (B)
in_settings['weight_ceiling'] = 1.0
in_settings['type'] = 'current'
in_settings['output_current_decay'] = 3.0
in_settings['output_current_peak'] = -0.82

ds_settings = {}
ds_settings['reset_potential'] = -54.5
ds_settings['spike_potential'] = 0
ds_settings['threshold'] = -45.5
ds_settings['left_window_constant'] = 20#(t+)
ds_settings['right_window_constant'] = 20#(t-)
ds_settings['learning_rate'] = 0.05# (A+)
ds_settings['stability'] = 1.05# (B)
ds_settings['weight_ceiling'] = 1.0
ds_settings['type'] = 'voltage'

inhi = 'off'
#inhi = 'on'

noise_intensy = 2.2

all_neuron = []
excitory_a = []
excitory_b = []
observer_a = []
observer_b = []
inhibitory = []
noise = []
downstream = []

source_a = Current('source', 0, 'current', 20.7)
source_b = Current('source', 1, 'current', 21.5)

for i in range(99):
    neuron_producing = Neuron('excitory', i, ex_settings, 'off')
    noise_pos = Noise('noise', i, 100, noise_intensy, 3.0)
    noise_neg = Noise('noise', i, 100, -noise_intensy, 3.0)
    noise.append(noise_pos)
    noise.append(noise_neg)
    noise_pos.connect(neuron_producing)
    noise_neg.connect(neuron_producing)

    if random.random() < 0.5:
        excitory_a.append(neuron_producing)
        source_a.connect(neuron_producing)
    else:
        excitory_b.append(neuron_producing)
        source_b.connect(neuron_producing)
    if random.random() < 0.5:
        observer_a.append(neuron_producing)
    else:
        observer_b.append(neuron_producing)

for i in range(99):
    neuron_producing = Neuron('downstream', i, ds_settings, 'off')
    downstream.append(neuron_producing)
    for observee in random.sample(excitory_a+excitory_b, 20):
        observee.connect(neuron_producing)

for i in range(801):
    neuron_producing = Neuron('inhibitory', i, in_settings, 'off')
    if inhi == 'on':
        inhibitory.append(neuron_producing)
        for inhibitee in random.sample(excitory_a+excitory_b, 20):
            inhibitee.connect(neuron_producing)
            neuron_producing.connect(inhibitee)


all_neuron = excitory_a + excitory_b + inhibitory + downstream + noise
duration = 500


for i in range(duration):
    for neuron in all_neuron:
        event = Event(name = 'update')
        simpy.activate(event, event.update(neuron), delay = i)

simpy.simulate(until = duration+0.0)

ex_spikes_number = 0.0
for i in excitory_a+excitory_b:
    ex_spikes_number += i.spikes_number

ds_spikes_number = 0.0
for i in downstream:
    ds_spikes_number += i.spikes_number

print ds_spikes_number/ex_spikes_number

outfile_a = open('a_inhib_'+inhi+'.txt', 'w')
for i in excitory_a[10].spikes_record:
    outfile_a.write(str(i)+'\n')

outfile_b = open('b_inhib_'+inhi+'.txt', 'w')
for i in excitory_b[20].spikes_record:
    outfile_b.write(str(i)+'\n')


#x = list(range(len(downstream[1].spikes_record)))
#plot.plot(x, downstream[1].spikes_record)
#plot.show()

#x = list(range(len(excitory_a[1].value_record)))
#plot.plot(x, excitory_a[1].value_record)
#plot.show()



