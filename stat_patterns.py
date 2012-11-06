import math
import pickle
import os.path
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

def count_spike(list):
    result = 0
    for j in list:
        if j >= 0.0:
            result += 1
    return result

def calculate_corr(a, b, bin_size):
    temp_a = split_into_bins(a, bin_size)
    temp_b = split_into_bins(b, bin_size)
    return pearsonr(temp_a, temp_b)

if os.path.isfile('mac'):
    bin_ops = [1, 2, 4, 6, 8, 10, 20, 40, 60, 80, 100, 200]
elif os.path.isfile('cluster'):
    bin_ops = [1, 2, 4, 6, 8, 10, 20, 40, 60, 80, 100, 200, 400, 600, 800, 1000]

a_random = []
a_trained = []
b_random = []
b_trained = []


for i in range(99):
    raw_a_random = [float(line) for line in open('spikes_record/'+str(i)+'a_inhib_random.txt', 'r')]
    raw_a_trained=[float(line) for line in open('spikes_record/'+str(i)+'a_inhib_trained.txt', 'r')]
    raw_b_random = [float(line) for line in open('spikes_record/'+str(i)+'b_inhib_random.txt', 'r')]
    raw_b_trained=[float(line) for line in open('spikes_record/'+str(i)+'b_inhib_trained.txt', 'r')]

    a_random.append(count_spike(raw_a_random))
    a_trained.append(count_spike(raw_a_trained))
    b_random.append(count_spike(raw_b_random))
    b_trained.append(count_spike(raw_b_trained))
    
        

corr_random = pearsonr(a_random, b_random)
corr_trained = pearsonr(a_trained, b_trained)

print(corr_random, corr_trained)



