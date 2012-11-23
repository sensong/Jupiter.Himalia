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
source_a_random = []
a_trained = []
source_a_trained = []
a_noinh = []
source_a_noinh = []
b_random = []
source_b_random = []
b_trained = []
source_b_trained = []
b_noinh = []
source_b_noinh = []


for i in range(99):
    raw_a_random = [float(line) for line in open('spikes_record/'+str(i)+'a_on_random.txt', 'r')]
    source_raw_a_random = [float(line) for line in open('spikes_record/source'+str(i)+'a_on_random.txt', 'r')]
    raw_a_trained=[float(line) for line in open('spikes_record/'+str(i)+'a_on_trained.txt', 'r')]
    source_raw_a_trained=[float(line) for line in open('spikes_record/source'+str(i)+'a_on_trained.txt', 'r')]
    raw_a_noinh=[float(line) for line in open('spikes_record/'+str(i)+'a_off_off.txt', 'r')]
    source_raw_a_noinh=[float(line) for line in open('spikes_record/source'+str(i)+'a_off_off.txt', 'r')]
    raw_b_random = [float(line) for line in open('spikes_record/'+str(i)+'b_on_random.txt', 'r')]
    source_raw_b_random = [float(line) for line in open('spikes_record/source'+str(i)+'b_on_random.txt', 'r')]
    raw_b_trained=[float(line) for line in open('spikes_record/'+str(i)+'b_on_trained.txt', 'r')]
    source_raw_b_trained=[float(line) for line in open('spikes_record/source'+str(i)+'b_on_trained.txt', 'r')]
    raw_b_noinh=[float(line) for line in open('spikes_record/'+str(i)+'b_off_off.txt', 'r')]
    source_raw_b_noinh=[float(line) for line in open('spikes_record/source'+str(i)+'b_off_off.txt', 'r')]

    a_random.append(count_spike(raw_a_random))
    source_a_random.append(count_spike(source_raw_a_random))
    a_trained.append(count_spike(raw_a_trained))
    source_a_trained.append(count_spike(source_raw_a_trained))
    a_noinh.append(count_spike(raw_a_noinh))
    source_a_noinh.append(count_spike(source_raw_a_noinh))
    b_random.append(count_spike(raw_b_random))
    source_b_random.append(count_spike(source_raw_b_random))
    b_trained.append(count_spike(raw_b_trained))
    source_b_trained.append(count_spike(source_raw_b_trained))
    b_noinh.append(count_spike(raw_b_noinh))
    source_b_noinh.append(count_spike(source_raw_b_noinh))
    
        
corr_noinh = pearsonr(a_noinh, b_noinh)
source_corr_noinh = pearsonr(source_a_noinh, source_b_noinh)
corr_random = pearsonr(a_random, b_random)
source_corr_random = pearsonr(source_a_random, source_b_random)
corr_trained = pearsonr(a_trained, b_trained)
source_corr_trained = pearsonr(source_a_trained, source_b_trained)

a_random_file = open('raw_data/a_random_pattern.txt','w')
a_trained_file = open('raw_data/a_trained_pattern.txt','w')
a_noinh_file = open('raw_data/a_noinh_pattern.txt','w')
b_random_file = open('raw_data/b_random_pattern.txt','w')
b_trained_file = open('raw_data/b_trained_pattern.txt','w')
b_noinh_file = open('raw_data/b_noinh_pattern.txt','w')
pickle.dump(a_random,a_random_file)
pickle.dump(a_trained,a_trained_file)
pickle.dump(a_noinh,a_noinh_file)
pickle.dump(b_random,b_random_file)
pickle.dump(b_trained,b_trained_file)
pickle.dump(b_noinh,b_noinh_file)


print(source_corr_noinh, corr_noinh, source_corr_random, corr_random, source_corr_trained, corr_trained)
