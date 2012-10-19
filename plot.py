import matplotlib.pyplot as plot
import numpy

inhib = [float(line) for line in open('stat_net_result_in.txt', 'r')]
no_inhib = [float(line) for line in open('stat_net_result_no_in.txt', 'r')]

x = range(len(inhib))

plot.plot(x, inhib, '.-', x, no_inhib, '-')
plot.show()
