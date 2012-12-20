import math
import numpy
import pickle
import os.path
from itertools import imap


def number_spikes(list):
    result = 0 
    for i in list:
        if i >= 0.0:
            result += 1
    return result/2.0


a_ni = []
a_ri = []
a_ti = []
b_ni = []
b_ri = []
b_ti = []

for i in range(99):
    raw_ti = [float(line) for line in open('spikes_record/'+str(i)+'a_on_trained.txt', 'r')]
    raw_ri = [float(line) for line in open('spikes_record/'+str(i)+'a_on_random.txt', 'r')]
    raw_ni = [float(line) for line in open('spikes_record/'+str(i)+'a_off_off.txt', 'r')]

    raw_ti_b = [float(line) for line in open('spikes_record/'+str(i)+'b_on_trained.txt', 'r')]
    raw_ri_b = [float(line) for line in open('spikes_record/'+str(i)+'b_on_random.txt', 'r')]
    raw_ni_b = [float(line) for line in open('spikes_record/'+str(i)+'b_off_off.txt', 'r')]


    a_ni.append(number_spikes(raw_ni))
    a_ri.append(number_spikes(raw_ri))
    a_ti.append(number_spikes(raw_ti))
    b_ni.append(number_spikes(raw_ni_b))
    b_ri.append(number_spikes(raw_ri_b))
    b_ti.append(number_spikes(raw_ti_b))
        
a_ni = [(i-min(a_ni))/(max(a_ni)-min(a_ni)) for i in a_ni]
a_ri = [(i-min(a_ri))/(max(a_ri)-min(a_ri)) for i in a_ri]
a_ti = [(i-min(a_ti))/(max(a_ti)-min(a_ti)) for i in a_ti]
b_ni = [(i-min(b_ni))/(max(b_ni)-min(b_ni)) for i in b_ni]
b_ri = [(i-min(b_ri))/(max(b_ri)-min(b_ri)) for i in b_ri]
b_ti = [(i-min(b_ti))/(max(b_ti)-min(b_ti)) for i in b_ti]

a_ni = numpy.reshape(a_ni+[0], (10, 10))
a_ri = numpy.reshape(a_ri+[0], (10, 10))
a_ti = numpy.reshape(a_ti+[0], (10, 10))
b_ni = numpy.reshape(b_ni+[0], (10, 10))
b_ri = numpy.reshape(b_ri+[0], (10, 10))
b_ti = numpy.reshape(b_ti+[0], (10, 10))

pickle.dump(a_ni, open('rate_ni_a.txt', 'w'))
pickle.dump(a_ri, open('rate_ri_a.txt', 'w'))
pickle.dump(a_ti, open('rate_ti_a.txt', 'w'))
pickle.dump(b_ni, open('rate_ni_b.txt', 'w'))
pickle.dump(b_ri, open('rate_ri_b.txt', 'w'))
pickle.dump(b_ti, open('rate_ti_b.txt', 'w'))


#print(sum(a_ti)/len(a_ti))
