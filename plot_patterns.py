import matplotlib.pyplot as plot
import numpy
import pickle

mode = 'trained'
mode = 'random'

a_file = open('raw_data/a_'+mode+'_pattern.txt', 'r')
b_file = open('raw_data/b_'+mode+'_pattern.txt', 'r')

a_pattern = pickle.load(a_file)
b_pattern = pickle.load(b_file)
a_pattern = [i/2.0 for i in a_pattern]
b_pattern = [i/2.0 for i in b_pattern]

x = list(range(len(a_pattern)))

plot.plot(x, a_pattern, '.-', x, b_pattern, '.-')
plot.show()

