import pickle
import numpy
import matplotlib.pyplot as plot


source_a_file = open('source_pattern_a.txt', 'r')
stim_weights_file = open('trained_stim_weights.txt', 'r')

source_a = pickle.load(source_a_file)
stim_weights = pickle.load(stim_weights_file)

min = 1
max = 0
avg = 0
for i in stim_weights:
    if i < min:
        min = i
    if i > max:
        max = i
    avg += i
print(min, avg/99.0, max)

x = list(range(99))
plot.plot(x, source_a)
plot.plot(x, [i*100+50 for i in stim_weights])
plot.show()
