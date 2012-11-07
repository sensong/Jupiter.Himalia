import matplotlib.pyplot as plot
import numpy
import pickle
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


mode = 'trained'
mode = 'random'
#mode = 'noinh'
a_file = open('raw_data/a_'+mode+'_pattern.txt', 'r')
b_file = open('raw_data/b_'+mode+'_pattern.txt', 'r')

#a_file = open('raw_data/source_pattern_a.txt', 'r')
#b_file = open('raw_data/source_pattern_b.txt', 'r')
a_pattern = pickle.load(a_file)
b_pattern = pickle.load(b_file)

print(pearsonr(a_pattern, b_pattern))

a_pattern = [i*0.5 for i in a_pattern]
b_pattern = [i*0.5 for i in b_pattern]

x = list(range(len(a_pattern)))

plot.plot(x, a_pattern, '.-', x, b_pattern, '.-')
plot.show()

