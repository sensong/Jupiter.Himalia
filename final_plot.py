import pickle
from pylab import * 
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable 
import numpy as np 
import random



fig = figure(1, figsize=(4, 8))
ax1 = plt.subplot2grid((4,2), (0,0), colspan=2)
ax2 = plt.subplot2grid((4,2), (1,0))
divider2 = make_axes_locatable(ax2) 
ax2b = divider2.append_axes("bottom", size="100%", pad=0.05)
ax3 = plt.subplot2grid((4,2), (1,1))
divider3 = make_axes_locatable(ax3) 
ax3b = divider3.append_axes("bottom", size="100%", pad=0.05)
ax4 = plt.subplot2grid((4,2), (2,0))
divider4 = make_axes_locatable(ax4) 
ax4b = divider4.append_axes("bottom", size="100%", pad=0.05)
ax5 = plt.subplot2grid((4,2), (2,1))
divider5 = make_axes_locatable(ax5) 
ax5b = divider5.append_axes("bottom", size="100%", pad=0.05)
ax6 = plt.subplot2grid((4,2), (3,0))
ax7 = plt.subplot2grid((4,2), (3,1))

rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('font', family='sans-serif')

plt.subplots_adjust(wspace=.6, hspace=.6)

plt.setp(ax1.get_xticklabels(), visible=False)
plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax3.get_xticklabels(), visible=False)
plt.setp(ax4.get_xticklabels(), visible=False)

plt.figtext(0.028, 0.91, 'A', fontsize=20, zorder=1)
plt.figtext(0.028, 0.68, 'B', fontsize=20, zorder=1)
plt.figtext(0.5, 0.68, 'C', fontsize=20, zorder=1)
plt.figtext(0.028, 0.46, 'D', fontsize=20, zorder=1)
plt.figtext(0.5, 0.46, 'E', fontsize=20, zorder=1)
plt.figtext(0.028, 0.24, 'F', fontsize=20, zorder=1)
plt.figtext(0.5, 0.24, 'G', fontsize=20, zorder=1)


plt.figtext(0.8, 0.86, 'Total=99', fontsize=8, zorder=1)
plt.figtext(0.8, 0.82, 'Total=99', fontsize=8, zorder=1)
plt.figtext(0.8, 0.77, 'Total=801', fontsize=8, zorder=1)

a_timeline_subplots = [ax2b, ax3b, ax4b, ax5b]
a_heatmap_subplots = [ax2, ax3, ax4, ax5]
timeline_subplots = a_timeline_subplots + a_heatmap_subplots
axis_labelsize = 9

timeline_duration = 1000
line_number = 9

for i in timeline_subplots:
    if i in a_timeline_subplots:
        i.set_xlim(0, timeline_duration)
        i.set_ylim(0, line_number)
        i.set_xticklabels([0, timeline_duration/2, timeline_duration])
        i.xaxis.set_major_locator(MaxNLocator(2))
        i.yaxis.set_major_locator(MaxNLocator(1))
        i.set_yticks([0.5, line_number-0.5])
        i.set_yticklabels([1, line_number])
        i.yaxis.set_label_text('                 Familiar', fontsize=axis_labelsize)
        for tick in i.xaxis.get_major_ticks():
            tick.label.set_fontsize(6) 
        for tick in i.yaxis.get_major_ticks():
            tick.label.set_fontsize(6) 
    if i in a_heatmap_subplots:
        i.yaxis.set_visible(False)
        i.xaxis.set_visible(False)
        i.set_xlim(-0.5, 10.5)
        i.set_ylim(-0.5, 8.5)
ax4b.yaxis.set_label_text('                Novel', fontsize=axis_labelsize)

ax2.set_title('No Inhibition', )
ax3.set_title('Random Inhibition')
ax4.set_title('Trained Inhibition')
ax5.set_title('Trained Inhibition')
for i in a_heatmap_subplots:
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

ax1.quiver(x_stim, y_stim, [0]*3, [-0.9]*3, color='g', scale_units='xy', angles='xy', scale=1, width=0.002, headwidth=5, headlength=10, zorder=1)

f = open('gc2mc.txt', 'r')
gc2mc = pickle.load(f)
for (i, j) in zip(gc_x, gc2mc):
    for t in range(2):
        dx = j[t] - i - .5
        dy = 1.0
        k_angle = math.atan(dy/dx)
        #dx = dx - math.cos(k_angle)
        dy = dy - .1
        ax1.quiver([i], [.5], [dx], [dy], color='r', scale_units='xy', angles='xy', scale=1, width=0.002, headwidth=5, headlength=10, zorder=1)
        ax1.quiver([j[t]-.5], [1.5], [-dx], [-dy], color='g', scale_units='xy', angles='xy', scale=1, width=0.002, headwidth=5, headlength=10, zorder=1)

ax1.yaxis.grid(color='gray', zorder=0)
ax1.set_axisbelow(True)

cmap = cm.get_cmap('coolwarm', 1000) # jet doesn't have white color
cmap.set_bad('w') # default value is 'k'
def list_to_9_11_matrix(a_list):
    matrix = []
    p = 0
    for i in range(11):
        row = []
        for j in range(9):
            row.append(a_list[p])
            p += 1
        matrix.append(row)
    t_matrix = [[r[col] for r in matrix] for col in range(len(matrix[0]))]
    return t_matrix

#plot 2: no inhibition spikes timeline
def convert_scale(raw_list, index):
    new_list = []
    for i in raw_list:
        scale = (float(i) + 70.0) / 70.0 *0.85 + float(index)
        new_list.append(scale)
    return new_list

lineweight = 0.3
duration = 1000
line_number = 9

xxx = list(range(99))
random.shuffle(xxx)
xxx = list_to_9_11_matrix(xxx)
cax2 = ax2.imshow(xxx, aspect='auto', interpolation="nearest", cmap=cmap)
ax2.grid(True)

#ccax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
#ax2cbar = fig.colorbar(cax2, cax=ccax)
#ax2cbar.ax.set_yticklabels(['<', '', '>'])

trains = []
for i in range(line_number):
    raw_list = [float(line) for line in open('spikes_record/'+str(i)+'b_off_off.txt', 'r')][:duration]
    trains.append(convert_scale(raw_list, i))

x = list(range(len(trains[0])))
for i in range(line_number):
    ax2b.plot(x, trains[i], 'black', linewidth=lineweight)

#plot 3: random inhibition spikes timeline
xxx = list(range(99))
random.shuffle(xxx)
xxx = list_to_9_11_matrix(xxx)
ax3.imshow(xxx, aspect='auto', interpolation="nearest", cmap=cmap)
ax3.grid(True)

trains = []
for i in range(line_number):
    raw_list = [float(line) for line in open('spikes_record/'+str(i)+'b_on_random.txt', 'r')][:duration]
    trains.append(convert_scale(raw_list, i))

x = list(range(len(trains[0])))
for i in range(line_number):
    ax3b.plot(x, trains[i], 'black', linewidth=lineweight)

#plot 4: trained inhibition spikes timeline (Novel)
xxx = list(range(99))
random.shuffle(xxx)
xxx = list_to_9_11_matrix(xxx)
ax4.imshow(xxx, aspect='auto', interpolation="nearest", cmap=cmap)
ax4.grid(True)

trains = []
for i in range(line_number):
    raw_list = [float(line) for line in open('spikes_record/'+str(i)+'b_on_trained.txt', 'r')][:duration]
    trains.append(convert_scale(raw_list, i))

x = list(range(len(trains[0])))
for i in range(line_number):
    ax4b.plot(x, trains[i], 'black', linewidth=lineweight)

#plot 5: trained inhibition spikes timeline (Familiar)
xxx = list(range(99))
random.shuffle(xxx)
xxx = list_to_9_11_matrix(xxx)
ax5.imshow(xxx, aspect='auto', interpolation="nearest", cmap=cmap)
ax5.grid(True)

trains = []
for i in range(line_number):
    raw_list = [float(line) for line in open('spikes_record/'+str(i)+'b_on_trained.txt', 'r')][:duration]
    trains.append(convert_scale(raw_list, i))

x = list(range(len(trains[0])))
for i in range(line_number):
    ax5b.plot(x, trains[i], 'black', linewidth=lineweight)


#plot 6: Sparsity
p6file = open('final_result.txt', 'r')
p6raw = []
for str in p6file.readlines():
    p6raw.append([float(number) for number in str.split()])

colors_order = []
for i in range(len(p6raw)):
    random_color = []
    for i in range(3):
        random_color.append(random.random())
    colors_order.append(random_color)

ax6.set_xlim(0, 5)
ax6.set_ylim(-0.2, 1)
ax6.xaxis.set_major_locator(MaxNLocator(5))
ax6.yaxis.set_major_locator(MaxNLocator(8))
ax6.set_xticklabels(['', 'NI', 'RI', 'TI\n(F)', 'TI\n(N)'])
ax6.set_yticks([-0.2, 0, 0.2, .4, .6, .8, 1.0])
ax6.set_yticklabels(['-0.2', 0, 0.2, 0.4, 0.6, 0.8, 1])
for tick in ax6.xaxis.get_major_ticks():
    tick.label.set_fontsize(9) 
for tick in ax6.yaxis.get_major_ticks():
    tick.label.set_fontsize(6) 
x = [1, 2, 3]
co = 0
for i in p6raw:
    ax6.plot(x, i, color=colors_order[co], linewidth=0.5, zorder=0.8)
    ax6.plot([x[0]], [i[0]], '^', color=colors_order[co], zorder=0.4)
    ax6.plot([x[1]], [i[1]], 's', color=colors_order[co], zorder=0.4)
    ax6.plot([x[2]], [i[2]], 'o', color=colors_order[co], zorder=0.4)
    co += 1
avg_bar = [0.398660584, 0.319721684, 0.236385816]
x_offset = [i-0.3 for i in x]
avg_offset = [i-0.02 for i in avg_bar]
for (i, j) in zip(x_offset, avg_offset):
    ax6.add_patch(mpl.patches.Rectangle((i, j), 0.6, 0.04, color='black'))

ax6.yaxis.set_label_text('Sparsity', fontsize=axis_labelsize)

#plot 7: statistics of decorrelation

p7file = open('final_result.txt', 'r')
p7raw = []
for str in p7file.readlines():
    p7raw.append([float(number) for number in str.split()])
p7file.close()

ax7.set_xlim(0, 4)
ax7.set_ylim(-0.2, 1)
ax7.xaxis.set_major_locator(MaxNLocator(4))
ax7.yaxis.set_major_locator(MaxNLocator(8))
ax7.set_xticklabels(['', 'NI', 'RI', 'TI'])
ax7.set_yticks([-0.2, 0, 0.2, .4, .6, .8, 1.0])
ax7.set_yticklabels(['-0.2', 0, 0.2, 0.4, 0.6, 0.8, 1])
for tick in ax7.xaxis.get_major_ticks():
    tick.label.set_fontsize(9) 
for tick in ax7.yaxis.get_major_ticks():
    tick.label.set_fontsize(6) 
x = [1, 2, 3]
co = 0
for i in p6raw:
    ax7.plot(x, i, color=colors_order[co], linewidth=0.5, zorder=0.8)
    ax7.plot([x[0]], [i[0]], '^', color=colors_order[co], zorder=0.4)
    ax7.plot([x[1]], [i[1]], 's', color=colors_order[co], zorder=0.4)
    ax7.plot([x[2]], [i[2]], 'o', color=colors_order[co], zorder=0.4)
    co += 1
avg_bar = [0.398660584, 0.319721684, 0.236385816]
x_offset = [i-0.3 for i in x]
avg_offset = [i-0.02 for i in avg_bar]
for (i, j) in zip(x_offset, avg_offset):
    ax7.add_patch(mpl.patches.Rectangle((i, j), 0.6, 0.04, color='black'))

ax7.yaxis.set_label_text('Correlation', fontsize=axis_labelsize)


savefig("pylab_example.svg", dpi=800)          # save as SVG
show()




