import pickle
import random
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

source_a = pickle.load(open('source_pattern_a.txt', 'r'))
source_b = []
difference = 0.2
for i in source_a:
    if random.random() < difference:
        source_b.append(100.0)
    else:
        source_b.append(i)



bfile = open('source_pattern_c.txt', 'w')
pickle.dump(source_b, bfile)
bfile.close()
source_b = pickle.load(open('source_pattern_b.txt', 'r'))
print(pearsonr(source_a, source_b))
