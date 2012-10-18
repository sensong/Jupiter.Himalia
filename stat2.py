import math
import numpy
import matplotlib.pyplot as plot
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

raw_inhib_a = [float(line) for line in open('inhib_a.txt', 'r')]
raw_inhib_b = [float(line) for line in open('inhib_b.txt', 'r')]
raw_no_inhib_a = [float(line) for line in open('no_inhib_a.txt', 'r')]
raw_no_inhib_b = [float(line) for line in open('no_inhib_b.txt', 'r')]

no_inhib_corr = []
inhib_corr = []


bin_ops = [1, 2, 4, 6, 8, 10, 20, 40, 60, 80, 100, 200, 400, 600, 800, 1000]
x = range(len(bin_ops))
for bin_size in bin_ops:
    no_inhib_corr.append(calculate_corr(raw_no_inhib_a, raw_no_inhib_b, bin_size)) 
    inhib_corr.append(calculate_corr(raw_inhib_a, raw_inhib_b, bin_size)) 


plot.plot(x, no_inhib_corr,'-', x, inhib_corr, '.-')
plot.show()
