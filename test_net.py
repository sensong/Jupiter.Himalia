from Stimulator import Constant_Stimulator as ConstantNeuron
from Stimulator import Current_Poisson_Stimulator as PoissonNeuron
from LIF_STDP_Neuron import LIF_STDP_Neuron as Neuron
from LIF_STDP_Neuron import Event
import SimPy.Simulation as simpy
import random
import pickle
#import matplotlib.pyplot as plot
#import numpy
import os.path
import sys

ex_settings = {}
ex_settings['reset_potential'] = -70.0
ex_settings['spike_potential'] = 0
ex_settings['threshold'] = -54.0
ex_settings['refactory_period'] = 5.0
ex_settings['left_window_constant'] = 5#(t+)
ex_settings['right_window_constant'] = 5#(t-)
ex_settings['learning_rate'] = 0.0015# (A+)
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
in_settings['output_current_peak'] = -1.5


pattern_index = sys.argv[1]
inhi = sys.argv[2]
is_trained = sys.argv[3]

noise_intensy = 8.2

all_neuron = []
mc = []
gc = []
noise = []
source = []

connections_list = pickle.load(open('connection_list.txt', 'r'))
pattern = pickle.load(open('source_pattern_'+pattern_index+'.txt', 'r'))

for i in range(99):
    source_producing = ConstantNeuron('source', i, 'current', pattern[i]) 
    source.append(source_producing)
    noise_pos = PoissonNeuron('noise', i, 100, noise_intensy, 3.0)
    noise_neg = PoissonNeuron('noise', i, 100, -noise_intensy, 3.0)
    noise.append(noise_pos)
    noise.append(noise_neg)
    neuron_producing = Neuron('mc', i, ex_settings, 'off')
    mc.append(neuron_producing)
    source_producing.connect(neuron_producing)
#    noise_pos.connect(neuron_producing)
#    noise_neg.connect(neuron_producing)


for i in range(801):
    if inhi == 'on':
        neuron_producing = Neuron('gc', i, in_settings, 'off')
        gc.append(neuron_producing)
        for inhibitee in connections_list[i]:
            mc[inhibitee].connect(neuron_producing)
            neuron_producing.connect(mc[inhibitee])

if inhi == 'on':
    if is_trained == 'trained':
        weights_file = open('trained_weights.txt', 'r')
    elif is_trained == 'random':
        weights_file = open('random_weights.txt', 'r')
        setting_weights = pickle.load(weights_file)
        i = 0
        for m in mc:
            j = 0
            for g in m.dendrites.keys():
                m.dendrites[g] = setting_weights[i][j]


all_neuron = mc + gc + noise
if os.path.isfile('mac'):
    duration = 5
elif os.path.isfile('cluster'):
    duration = 2000


for i in range(duration):
    for neuron in all_neuron:
        event = Event(name = 'update')
        simpy.activate(event, event.update(neuron), delay = i)
print("simulation scheduled.")

simpy.simulate(until = duration+0.0)
print("simulation done.")

file_op = 'w'
for i in range(99):
    outfile = open('spikes_record/'+str(i)+pattern_index+'_'+inhi+'_'+is_trained+'.txt', file_op)
    #source_outfile = open('spikes_record/source'+str(i)+pattern_index+'_'+inhi+'_'+is_trained+'.txt', file_op)
    #for j in source[i].spikes_record:
        #source_outfile.write(str(j)+'\n')
    for j in mc[i].spikes_record:
        outfile.write(str(j)+'\n')
    outfile.close()
    #source_outfile.close()




exit()
#x = list(range(len(mc[1].value_record)))

#valen = len(gc[1].value_record)
#va = [0.0] * valen 
#for inh in mc[1].dendrites.keys():
    #if inh in gc:
        #for i in range(valen):
            #va[i] += inh.value_record[i]

#plot.plot(x, va, '+')
#plot.plot(x, mc_a[1].value_record)
plot.plot(x, source[1].spikes_record, '-')
plot.plot(x, mc[1].spikes_record, '.-')
#plot.plot(x, gc[1].spikes_record, '+')



plot.show()



