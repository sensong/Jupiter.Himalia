import pickle
from pylab import * 
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable 
import numpy as np 



fig = figure(1, figsize=(4, 6))
ax1 = plt.subplot2grid((3,2), (0,0), colspan=2)
ax2 = plt.subplot2grid((3,2), (1,0))
divider2 = make_axes_locatable(ax2) 
ax2b = divider2.append_axes("bottom", size="100%", pad=0.05, sharex=ax2)
ax3 = plt.subplot2grid((3,2), (1,1))
divider3 = make_axes_locatable(ax3) 
ax3b = divider3.append_axes("bottom", size="100%", pad=0.05, sharex=ax3)
ax4 = plt.subplot2grid((3,2), (2,0))
divider4 = make_axes_locatable(ax4) 
ax4b = divider4.append_axes("bottom", size="100%", pad=0.05, sharex=ax4)
ax5 = plt.subplot2grid((3,2), (2,1))

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('font', family='sans-serif')

plt.subplots_adjust(wspace=.6, hspace=.6)

plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax3.get_xticklabels(), visible=False)
plt.setp(ax4.get_xticklabels(), visible=False)

plt.figtext(0.028, 0.9, 'A', fontsize=20, zorder=1)
plt.figtext(0.028, 0.60, 'B', fontsize=20, zorder=1)
plt.figtext(0.5, 0.60, 'C', fontsize=20, zorder=1)
plt.figtext(0.028, 0.30, 'D', fontsize=20, zorder=1)
plt.figtext(0.5, 0.30, 'E', fontsize=20, zorder=1)


plt.figtext(0.8, 0.84, 'Total=99', fontsize=8, zorder=1)
plt.figtext(0.8, 0.78, 'Total=99', fontsize=8, zorder=1)
plt.figtext(0.8, 0.72, 'Total=801', fontsize=8, zorder=1)

timeline_subplots = [ax2, ax2b, ax3, ax3b, ax4, ax4b]
a_timeline_subplots = [ax2, ax3, ax4]
axis_labelsize = 9
for i in timeline_subplots:
    i.set_xlim(0, 800)
    i.set_ylim(0, 15)
    i.set_xticklabels([0, 400, 800])
    i.xaxis.set_major_locator(MaxNLocator(2))
    i.yaxis.set_major_locator(MaxNLocator(1))
    i.set_yticks([0.5, 14.5])
    i.set_yticklabels([1, 15])
    if i in a_timeline_subplots:
        i.yaxis.set_label_text('A', fontsize=axis_labelsize)
    else:
        i.yaxis.set_label_text('B', fontsize=axis_labelsize)
    i.xaxis.set_label_text('Time (ms)', fontsize=axis_labelsize)
    for tick in i.xaxis.get_major_ticks():
        tick.label.set_fontsize(6) 
    for tick in i.yaxis.get_major_ticks():
        tick.label.set_fontsize(6) 

ax2.set_title('No Inhibition', )
ax3.set_title('Random Inhibition')
ax4.set_title('Trained Inhibition')
for i in a_timeline_subplots:
    i.title.set_fontsize(9)

#plot 1: setup
ax1.set_ylim(0, 3)
ax1.set_xlim(0, 10)
ax1.yaxis.set_major_locator(MaxNLocator(4))
ax1.xaxis.set_major_locator(MaxNLocator(1))
ax1.set_yticks([.5, 1.5, 2.5])
ax1.set_yticklabels(['GC', 'MC', 'Stim'])
for tick in ax1.yaxis.get_major_ticks():
    tick.label.set_fontsize(9) 
for tick in ax1.xaxis.get_major_ticks():
    tick.set_visible(False)

ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.spines['bottom'].set_visible(False)

gc_x = [i+0.5 for i in list(range(0, 10))]
gc_y = [0.5]*10
ax1.plot(gc_x, gc_y, 'wo', zorder=2)

x_mc = [2, 5, 8]
y_mc = [1.5]*3
ax1.plot(x_mc, y_mc, 'wo', zorder=2)

x_stim = x_mc 
y_stim = [2.5]*3
ax1.plot(x_stim, y_stim, 'wo', zorder=2)

ax1.quiver(x_stim, y_stim, [0]*3, [-0.9]*3, color='k', scale_units='xy', angles='xy', scale=1, width=0.002, headwidth=5, headlength=10, zorder=1)

f = open('gc2mc.txt', 'r')
gc2mc = pickle.load(f)
for (i, j) in zip(gc_x, gc2mc):
    for t in range(2):
        dx = j[t] - i - .5
        dy = 1.0
        k_angle = math.atan(dy/dx)
        #dx = dx - math.cos(k_angle)
        dy = dy - .1
        ax1.quiver([i], [.5], [dx], [dy], color='k', scale_units='xy', angles='xy', scale=1, width=0.002, headwidth=5, headlength=10, zorder=1)
        ax1.quiver([j[t]-.5], [1.5], [-dx], [-dy], color='k', scale_units='xy', angles='xy', scale=1, width=0.002, headwidth=5, headlength=10, zorder=1)

ax1.yaxis.grid(color='gray', zorder=0)
ax1.set_axisbelow(True)


#plot 2: no inhibition spikes timeline
def convert_scale(raw_list, index):
    new_list = []
    for i in raw_list:
        scale = (float(i) + 70.0) / 70.0 *0.85 + float(index)
        new_list.append(scale)
    return new_list

lineweight = 0.3
duration = 800
line_number = 15

trains = []
for i in range(line_number):
    raw_list = [float(line) for line in open('spikes_record/'+str(i)+'a_off_off.txt', 'r')][:duration]
    trains.append(convert_scale(raw_list, i))

x = list(range(len(trains[0])))
for i in range(line_number):
    ax2.plot(x, trains[i], 'black', linewidth=lineweight)

trains = []
for i in range(line_number):
    raw_list = [float(line) for line in open('spikes_record/'+str(i)+'b_off_off.txt', 'r')][:duration]
    trains.append(convert_scale(raw_list, i))

x = list(range(len(trains[0])))
for i in range(line_number):
    ax2b.plot(x, trains[i], 'black', linewidth=lineweight)

#plot 3: random inhibition spikes timeline
trains = []
for i in range(line_number):
    raw_list = [float(line) for line in open('spikes_record/'+str(i)+'a_on_random.txt', 'r')][:duration]
    trains.append(convert_scale(raw_list, i))

x = list(range(len(trains[0])))
for i in range(line_number):
    ax3.plot(x, trains[i], 'black', linewidth=lineweight)


trains = []
for i in range(line_number):
    raw_list = [float(line) for line in open('spikes_record/'+str(i)+'b_on_random.txt', 'r')][:duration]
    trains.append(convert_scale(raw_list, i))

x = list(range(len(trains[0])))
for i in range(line_number):
    ax3b.plot(x, trains[i], 'black', linewidth=lineweight)

#plot 4: trained inhibition spikes timeline
trains = []
for i in range(line_number):
    raw_list = [float(line) for line in open('spikes_record/'+str(i)+'a_on_trained.txt', 'r')][:duration]
    trains.append(convert_scale(raw_list, i))

x = list(range(len(trains[0])))
for i in range(line_number):
    ax4.plot(x, trains[i], 'black', linewidth=lineweight)

trains = []
for i in range(line_number):
    raw_list = [float(line) for line in open('spikes_record/'+str(i)+'b_on_trained.txt', 'r')][:duration]
    trains.append(convert_scale(raw_list, i))

x = list(range(len(trains[0])))
for i in range(line_number):
    ax4b.plot(x, trains[i], 'black', linewidth=lineweight)
#plot 5: statistics of decorrelation

p5file = open('final_result.txt', 'r')
p5lines = p5file.readlines()
p5raw = []
for str in p5lines:
    p5raw.append([float(number) for number in str.split()])

ax5.set_xlim(0, 4)
ax5.set_ylim(-0.2, 1)
ax5.xaxis.set_major_locator(MaxNLocator(4))
ax5.yaxis.set_major_locator(MaxNLocator(8))
ax5.set_xticklabels(['', 'NI', 'RI', 'TI'])
ax5.set_yticks([-0.2, 0, 0.2, .4, .6, .8, 1.0])
ax5.set_yticklabels(['-0.2', 0, 0.2, 0.4, 0.6, 0.8, 1])
for tick in ax5.xaxis.get_major_ticks():
    tick.label.set_fontsize(9) 
for tick in ax5.yaxis.get_major_ticks():
    tick.label.set_fontsize(6) 
x = [1, 2, 3]
for i in p5raw:
    ax5.plot(x, i, 'black', linewidth=0.5, zorder=0.8)
    ax5.plot([x[0]], [i[0]], 'w^', zorder=0.4)
    ax5.plot([x[1]], [i[1]], 'ws', zorder=0.4)
    ax5.plot([x[2]], [i[2]], 'wo', zorder=0.4)
avg_bar = [0.398660584, 0.319721684, 0.236385816]
x_offset = [i-0.2 for i in x]
avg_offset = [i-0.02 for i in avg_bar]
for (i, j) in zip(x_offset, avg_offset):
    ax5.add_patch(mpl.patches.Rectangle((i, j), 0.4, 0.04, color='black'))

ax5.yaxis.set_label_text('Correlation', fontsize=axis_labelsize)


savefig("pylab_example.svg", dpi=800)          # save as SVG
show()




