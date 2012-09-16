import SimPy.Simulation as Simpy
from Single_Perceptron import Single_Perceptron

import random
import math

exp_mode = 'SS-II-decay'



max_weight = 0.012
if exp_mode[6:12] == 'stable':
    stability = 1.05
elif exp_mode[6:11] == 'decay':
    stability = 1.75
else:
    print('stability flag ERROR')
    exit()

neuron_settings = {}
neuron_settings['rest_potential'] = 0
neuron_settings['action_potential'] = 1
neuron_settings['threshold'] = 0.3
neuron_settings['left_window_constant'] = 20
neuron_settings['right_window_constant'] = 20
neuron_settings['learning_rate'] = 0.005
neuron_settings['stability'] = stability
neuron_settings['max_weight'] = max_weight

out = open("plot_data.txt", "w")
mmm = open("mmm","w")
mmm.write("a")

inputs = 98
duration = 3000

group_label_A = 'Group A (40Hz, '
group_label_B = 'Group B (50Hz, '

if exp_mode[3:5] == 'II':
    init_weights = [0.0065] * inputs
    group_label_A += 'Self-induced, '
    group_label_B += 'Self-induced, '
elif exp_mode[3:5] == 'IN':
    init_weights = [0.0065] * 49
    init_weights = init_weights + ([0.0025] * 49)
    group_label_A += 'Self-induced, '
    group_label_B += 'Not self-induced, '
elif exp_mode[3:5] == 'NI':
    init_weights = [0.0025] * 49
    init_weights = init_weights + ([0.0065] * 49)
    group_label_A += 'Not self-induced, '
    group_label_B += 'Self-induced, '
elif exp_mode[3:5] == 'NN':
    init_weights = [0.0025] * inputs
    group_label_A += 'Not self-induced, '
    group_label_B += 'Not self-induced, '
else:
    print('self-induced flag ERROR')
    exit()


middle_weights = [max_weight / 2] * inputs

a = Single_Perceptron("single_perceptron", 0, inputs, 
        neuron_settings, 
        initial_weights = init_weights, 
        STDP = 'on')
b = Single_Perceptron("single_perceptron", 0, 49, 
        neuron_settings, 
        initial_weights = init_weights[:49], 
        STDP = 'on')
c = Single_Perceptron("single_perceptron", 0, 49, 
        neuron_settings, 
        initial_weights = init_weights[49:], 
        STDP = 'on')
Simpy.initialize()

current_time = 0

if exp_mode[0] == 'S':
    a.stimulate(range(0, 49), current_time, duration, 40)
    b.stimulate(range(0, 49), current_time, duration, 40)
    group_label_A += 'Sync)'
elif exp_mode[0] == 'A':
    a.stimulate(range(0, 49), current_time, duration, 40, init_phase = "random")
    b.stimulate(range(0, 49), current_time, duration, 40, init_phase = "random")
    group_label_A += 'Async)'
else:
    print('input mode flag ERROR')
    exit()

if exp_mode[1] == 'S':
    a.stimulate(range(49, inputs), current_time, duration, 50)
    c.stimulate(range(0, 49), current_time, duration, 50)
    group_label_B += 'Sync)'
elif exp_mode[1] == 'A':
    a.stimulate(range(49, inputs), current_time, duration, 50, init_phase = "random")
    c.stimulate(range(0, 49), current_time, duration, 50, init_phase = "random")
    group_label_B += 'Async)'
else:
    print('input mode flag ERROR')
    exit()
print('!')
Simpy.simulate(until = duration)
print('!')
resultA = a.report_weights_trend(0, 49)
resultB = a.report_weights_trend(49, inputs)
baseA = b.report_weights_trend(0, 49)
baseB = c.report_weights_trend(0, 49)
print('!')
STD_data = a.report_spikes_timeline(0, 300)

### Plotting ==========================================
out.write("# name: bx\n# type: matrix\n# rows: 1\n# columns: " + str(len(baseA)) + "\n")
for i in baseA:
    out.write(" "+str(i[0]))
out.write("\n\n\n")
out.write("# name: by\n# type: matrix\n# rows: 1\n# columns: " + str(len(baseA)) + "\n")
for i in baseA:
    out.write(" "+str(i[1]))
out.write("\n\n\n")
out.write("# name: bu\n# type: matrix\n# rows: 1\n# columns: " + str(len(baseB)) + "\n")
for i in baseB:
    out.write(" "+str(i[0]))
out.write("\n\n\n")
out.write("# name: bv\n# type: matrix\n# rows: 1\n# columns: " + str(len(baseB)) + "\n")
for i in baseB:
    out.write(" "+str(i[1]))
out.write("\n\n\n")

out.write("# name: x\n# type: matrix\n# rows: 1\n# columns: " + str(len(resultA)) + "\n")
for i in resultA:
    out.write(" "+str(i[0]))
out.write("\n\n\n")
out.write("# name: y\n# type: matrix\n# rows: 1\n# columns: " + str(len(resultA)) + "\n")
for i in resultA:
    out.write(" "+str(i[1]))
out.write("\n\n\n")
out.write("# name: u\n# type: matrix\n# rows: 1\n# columns: " + str(len(resultB)) + "\n")
for i in resultB:
    out.write(" "+str(i[0]))
out.write("\n\n\n")
out.write("# name: v\n# type: matrix\n# rows: 1\n# columns: " + str(len(resultB)) + "\n")
for i in resultB:
    out.write(" "+str(i[1]))
out.write("\n\n\n")

index = 0
for line in STD_data:
    out.write("# name: l" + str(index) + "x\n# type: matrix\n# rows: 1\n# columns: " + str(len(line)) + "\n")
    for i in line:
        out.write(" "+str(i[0]))
        out.write("\n\n\n")
    out.write("# name: l"+ str(index)+ "y\n# type: matrix\n# rows: 1\n# columns: " + str(len(line)) + "\n")
    for i in line:
        out.write(" "+str(i[1]))
        out.write("\n\n\n")
    index += 1

scriptfile = open("plot_script.m", "w")
scriptfile.write("load 'plot_data.txt'\n")

scriptfile.write("plot(bx, by, bu, bv)\n")
scriptfile.write("axis([0 1 0 " + str(max_weight) + "],'autox')\n")
scriptfile.write("xlabel('time(ms)')\n")
scriptfile.write("ylabel('average weight')\n")
scriptfile.write("title('"+ exp_mode + "(independent)')\n")
scriptfile.write("text ("+str(baseA[len(baseA)//2][0])+", "+str(baseA[len(baseA)//2][1])+", 'A')\n")
scriptfile.write("text ("+str(baseB[len(baseB)//2][0])+", "+str(baseB[len(baseB)//2][1])+", 'B')\n")
scriptfile.write("legend ('" + group_label_A + "','" + group_label_B + "','location','northwest')\n")
scriptfile.write("print -dpng '-S900,400' figure\\" + exp_mode +"-bwt\n")

scriptfile.write("plot(x, y, u, v)\n")
scriptfile.write("axis([0 1 0 " + str(max_weight) + "],'autox')\n")
scriptfile.write("xlabel('time(ms)')\n")
scriptfile.write("ylabel('average weight')\n")
scriptfile.write("title('"+ exp_mode + "(interfering)')\n")
scriptfile.write("text ("+str(resultA[len(resultA)//2][0])+", "+str(resultA[len(resultA)//2][1])+", 'A')\n")
scriptfile.write("text ("+str(resultB[len(resultB)//2][0])+", "+str(resultB[len(resultB)//2][1])+", 'B')\n")
scriptfile.write("legend ('" + group_label_A + "','" + group_label_B + "','location','northwest')\n")
scriptfile.write("print -dpng '-S900,400' figure\\" + exp_mode +"-wt\n")

scriptfile.write("plot(")
for i in range(0, inputs):
    scriptfile.write("l" + str(i) + "x, l" + str(i) +"y, 'b', ")
scriptfile.write("l"+str(inputs)+"x, l" + str(inputs)+"y, 'r')\n")
scriptfile.write("xlabel('time(ms)')\n")
scriptfile.write("ylabel('input index')\n")
scriptfile.write("title('"+ exp_mode + "')\n")
scriptfile.write("print -dpng '-S900,400' figure\\" + exp_mode +"-std\n")

