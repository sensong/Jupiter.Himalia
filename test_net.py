from Stimulator import Constant_Stimulator as Current
from Stimulator import Current_Poisson_Stimulator as Noise
from Stimulator import Current_Poisson_Pool as Inhibitory_Pool
from LIF_STDP_Neuron import LIF_STDP_Neuron as Neuron
from LIF_STDP_Neuron import Event
import SimPy.SimulationTrace as simpy
import random
#import matplotlib.pyplot as plot
#import numpy
import os.path

ex_settings = {}
ex_settings['reset_potential'] = -70.0
ex_settings['spike_potential'] = 0
ex_settings['threshold'] = -54.0
ex_settings['refactory_period'] = 5.0
ex_settings['left_window_constant'] = 20#(t+)
ex_settings['right_window_constant'] = 20#(t-)
ex_settings['learning_rate'] = 0.05# (A+)
ex_settings['stability'] = 1.05# (B)
ex_settings['weight_ceiling'] = 1.0
ex_settings['type'] = 'current'
ex_settings['output_current_decay'] = 3.0
ex_settings['output_current_peak'] = 20.7 

in_settings = {}
in_settings['reset_potential'] = -70.0
in_settings['spike_potential'] = 0
in_settings['threshold'] = -54.0
in_settings['refactory_period'] = 0.0
in_settings['left_window_constant'] = 20#(t+)
in_settings['right_window_constant'] = 20#(t-)
in_settings['learning_rate'] = 0.05# (A+)
in_settings['stability'] = 1.05# (B)
in_settings['weight_ceiling'] = 1.0
in_settings['type'] = 'current'
in_settings['output_current_decay'] = 3.0
in_settings['output_current_peak'] = -5.4

ds_settings = {}
ds_settings['reset_potential'] = -70.0
ds_settings['spike_potential'] = 0
ds_settings['threshold'] = -54.0
ds_settings['refactory_period'] = 0.0
ds_settings['left_window_constant'] = 20#(t+)
ds_settings['right_window_constant'] = 20#(t-)
ds_settings['learning_rate'] = 0.05# (A+)
ds_settings['stability'] = 1.05# (B)
ds_settings['weight_ceiling'] = 1.0
ds_settings['type'] = 'voltage'

inhi = 'on'
if os.path.isfile('no_inhi.tmp'):
    inhi = 'off'

noise_intensy = 8.2

all_neuron = []
excitatory_a = []
excitatory_b = []
observer_a = []
observer_b = []
inhibitory = []
noise = []
downstream = []

source_a = Current('source', 0, 'current', 20.7)
source_b = Current('source', 1, 'current', 21.5)



for i in range(99):
    neuron_producing = Neuron('excitatory', i, ex_settings, 'off')
    noise_pos = Noise('noise', i, 100, noise_intensy, 3.0)
    noise_neg = Noise('noise', i, 100, -noise_intensy, 3.0)
    noise.append(noise_pos)
    noise.append(noise_neg)
    noise_pos.connect(neuron_producing)
    noise_neg.connect(neuron_producing)

    if random.random() < 0.5:
        excitatory_a.append(neuron_producing)
        source_a.connect(neuron_producing)
    else:
        excitatory_b.append(neuron_producing)
        source_b.connect(neuron_producing)
    if random.random() < 0.5:
        observer_a.append(neuron_producing)
    else:
        observer_b.append(neuron_producing)

#for i in range(99):
    #neuron_producing = Neuron('downstream', i, ds_settings, 'off')
    #downstream.append(neuron_producing)
    #for observee in random.sample(excitatory_a+excitatory_b, 20):
        #observee.connect(neuron_producing)

for i in range(801):
    neuron_producing = Neuron('inhibitory', i, in_settings, 'off')
    if inhi == 'on':
        inhibitory.append(neuron_producing)
        for inhibitee in random.sample(excitatory_a+excitatory_b, 20):
            inhibitee.connect(neuron_producing)
            neuron_producing.connect(inhibitee)


all_neuron = excitatory_a + excitatory_b + inhibitory + downstream + noise
duration = 600


for i in range(duration):
    for neuron in all_neuron:
        event = Event(name = 'update')
        simpy.activate(event, event.update(neuron), delay = i)
print("simulation scheduled.")

simpy.simulate(until = duration+0.0)
print("simulation done.")

#ex_spikes_number = 0.0
#for i in excitatory_a+excitatory_b:
    #ex_spikes_number += i.spikes_number

#ds_spikes_number = 0.0
#for i in downstream:
    #ds_spikes_number += i.spikes_number

#print ds_spikes_number/ex_spikes_number

is_continue = os.path.isfile('continue.tmp')
file_op = 'w'
if is_continue:
    file_op = 'a'


for i in range(99):
    outfile = open('spikes_record/'+str(i)+'_inhib_'+inhi+'.txt', file_op)
    for j in (excitatory_a+excitatory_b)[i].spikes_record:
        outfile.write(str(j)+'\n')
    outfile.close()

continue_file = open('continue.tmp', 'w')
continue_file.write('!')
continue_file.close()

#for i in excitatory_a+excitatory_b+inhibitory:
    #continue_file.write(str(i)+'\n')
#continue_file.close()

exit()
x = list(range(len(excitatory_a[1].value_record)))

valen = len(inhibitory[1].value_record)
va = [0.0] * valen 
for inh in (excitatory_a+excitatory_b)[1].dendrites.keys():
    if inh in inhibitory:
        for i in range(valen):
            va[i] += inh.value_record[i]

plot.plot(x, va)
#plot.plot(x, excitatory_a[1].value_record)
plot.plot(x, excitatory_a[1].spikes_record, '.-')
plot.plot(x, inhibitory[1].spikes_record, '+')



plot.show()



