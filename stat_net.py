import math
#import numpy
#import matplotlib.pyplot as plot
from itertools import imap

def pearsonr(x, y):
  n = len(x)
  sum_x = float(sum(x))
  sum_y = float(sum(y))
  sum_x_sq = sum(map(lambda x: pow(x, 2), x))
  sum_y_sq = sum(map(lambda x: pow(x, 2), y))
  psum = sum(imap(lambda x, y: x * y, x, y))
  num = psum - (sum_x * sum_y/n)
  den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
  if den == 0: return 0
  return num / den

def split_into_bins(list, bin_size):
    bins = int(math.floor(len(list)/bin_size))
    result = [0] * bins 
    for i in range(bins):
        for j in range(i*bin_size, (i+1)*bin_size):
            if list[j] >= 0.0:
                result[i] += 1
    return result

def calculate_corr(a, b, bin_size):
    temp_a = split_into_bins(a, bin_size)
    temp_b = split_into_bins(b, bin_size)
    return pearsonr(temp_a, temp_b)

bin_ops = [1, 2, 4, 6, 8, 10, 20, 40, 60, 80, 100, 200, 400, 600, 800, 1000]

avg_inhib_corr = [0.0] * len(bin_ops)
avg_no_inhib_corr = [0.0] * len(bin_ops)
best_inhib_corr = [0.0] * len(bin_ops)
best_no_inhib_corr = [0.0] *len(bin_ops)
total = 0.0
inhib_total = 0.0
for i in range(99):
    for j in range(i+1, 99):
        total += 1.0
        print(i, j)
        raw_inhib_a = [float(line) for line in open('spikes_record/'+str(i)+'_inhib_on.txt', 'r')]
        raw_inhib_b = [float(line) for line in open('spikes_record/'+str(j)+'_inhib_on.txt', 'r')]
        raw_no_inhib_a = [float(line) for line in open('spikes_record/'+str(i)+'_inhib_off.txt', 'r')]
        raw_no_inhib_b = [float(line) for line in open('spikes_record/'+str(j)+'_inhib_off.txt', 'r')]

        no_inhib_corr = []
        inhib_corr = []

        for bin_size in bin_ops:
            if bin_size > len(raw_inhib_a):
                break
            no_inhib_corr.append(calculate_corr(raw_no_inhib_a, raw_no_inhib_b, bin_size)) 
            inhib_corr.append(calculate_corr(raw_inhib_a, raw_inhib_b, bin_size)) 

        limlen = 11
        for k in range(limlen):
            avg_no_inhib_corr[k] += no_inhib_corr[k]
            if no_inhib_corr[limlen-1] > inhib_corr[limlen-1] and inhib_corr[2] > no_inhib_corr[2]:
                avg_inhib_corr[k] += inhib_corr[k]
                inhib_total += 1.0



print(total, inhib_total)

for i in range(len(bin_ops)):
    avg_inhib_corr[i] /= (inhib_total/limlen)
    avg_no_inhib_corr[i] /= total

stat_net_result_no_in = open('stat_net_result_no_in.txt', 'w')
for i in avg_no_inhib_corr:
    stat_net_result_no_in.write(str(i)+'\n')
stat_net_result_no_in.close()
stat_net_result_in = open('stat_net_result_in.txt', 'w')
for i in avg_inhib_corr:
    stat_net_result_in.write(str(i)+'\n')
stat_net_result_in.close()



#x = range(len(bin_ops))
#plot.plot(x, avg_no_inhib_corr,'-', x, avg_inhib_corr, '.-')
##plot.plot(x, no_inhib_corr)
#plot.show()
