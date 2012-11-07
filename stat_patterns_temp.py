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

a_noinh = []
b_noinh = []


for i in range(99):
    raw_a_noinh=[float(line) for line in open('spikes_record/'+str(i)+'a_off_off.txt', 'r')]
    raw_b_noinh=[float(line) for line in open('spikes_record/'+str(i)+'b_off_off.txt', 'r')]

    a_noinh.append(count_spike(raw_a_noinh))
    b_noinh.append(count_spike(raw_b_noinh))
    
        
corr_noinh = pearsonr(a_noinh, b_noinh)

a_noinh_file = open('raw_data/a_noinh_pattern.txt','w')
b_noinh_file = open('raw_data/b_noinh_pattern.txt','w')
pickle.dump(a_noinh,a_noinh_file)
pickle.dump(b_noinh,b_noinh_file)


print(corr_noinh)


