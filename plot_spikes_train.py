import matplotlib.pyplot as plot
import numpy

def convert_scale(raw_list, index):
    new_list = []
    for i in raw_list:
        scale = (float(i) + 70.0) / 70.0 + float(index)
        new_list.append(scale)
    return new_list

line_number = 99
trains = []
for i in range(line_number):
    raw_list = [float(line) for line in open('spikes_record/'+str(i)+'a_on_random.txt', 'r')]
    trains.append(convert_scale(raw_list, i))

x = list(range(len(trains[0])))
for i in range(line_number):
    plot.plot(x, trains[i], 'black')
plot.show()

