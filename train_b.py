from Stimulator import Constant_Stimulator as ConstantNeuron
from Stimulator import Current_Poisson_Stimulator as PoissonNeuron
from Stimulator import Regular_Stimulator as RegNeuron
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
ex_settings['output_current_peak'] = 40.0 

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
in_settings['output_current_peak'] = -5.0


pattern_index = 'b'
inhi = 'on'
is_trained = 'off'


if len(sys.argv)>1:
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
    source_producing = PoissonNeuron('source', i, pattern[i], 70.0, 3.0) 
    source.append(source_producing)
    noise_pos = PoissonNeuron('noise', i, 100, noise_intensy, 3.0)
    noise_neg = PoissonNeuron('noise', i, 100, -noise_intensy, 3.0)
    noise.append(noise_pos)
    noise.append(noise_neg)
    neuron_producing = Neuron('mc', i, ex_settings, 'right_only')
    neuron_producing.stim_source = source_producing
    mc.append(neuron_producing)
    source_producing.connect(neuron_producing)
#    noise_pos.connect(neuron_producing)
#    noise_neg.connect(neuron_producing)


for i in range(801):
    neuron_producing = Neuron('gc', i, in_settings, 'off')
    gc.append(neuron_producing)
    for inhibitee in connections_list[i]:
        mc[inhibitee].connect(neuron_producing)
        neuron_producing.connect(mc[inhibitee], 0.0, 0.3) #for trained synapses

weights_file_r = open('trained_weights.txt', 'r')
setting_weights = pickle.load(weights_file_r)
for i in range(99):
    for g in mc[i].dendrites.keys():
        if g in gc:
            mc[i].dendrites[g] = setting_weights[i][gc.index(g)]
weights_file_r.close()

stim_weights_file_r = open('trained_stim_weights.txt', 'r')
stim_weights = pickle.load(stim_weights_file_r)
for i in range(99):
    mc[i].dendrites[mc[i].stim_source] = stim_weights[i]
stim_weights_file_r.close()


all_neuron = source + mc + gc
if os.path.isfile('mac'):
    duration = 10
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

total = 0.0
avg = 0.0
trained_weights_file = open('trained_weights.txt', 'w')
trained_weights = []
for m in mc:
    temp_weights = [0]*801
    for g in m.dendrites.keys():
        if g in gc:
            temp_weights[gc.index(g)] = (m.dendrites[g])
        total+=1.0
        avg += m.dendrites[g]
    trained_weights.append(temp_weights)
pickle.dump(trained_weights, trained_weights_file)
print('GC average weight:', avg/total)



total = 0.0
avg = 0.0
trained_stim_weights_file = open('trained_stim_weights.txt', 'w')
trained_stim_weights = []
for m in mc:
    temp = m.dendrites[m.stim_source]
    trained_stim_weights.append(temp)
    total += 1.0
    avg += temp
pickle.dump(trained_stim_weights, trained_stim_weights_file)
print('Stim average weight:', avg/total)

exit()
x = list(range(len(mc[1].value_record)))

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
plot.plot(x, gc[1].spikes_record, '+')



plot.show()


