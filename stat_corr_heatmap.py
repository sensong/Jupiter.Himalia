import math
import pickle
import os.path
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

bin = 200


decorrelation_matrix_ni = [[1.0] * 99 for i in range(99)]
decorrelation_matrix_ri = [[1.0] * 99 for i in range(99)]
decorrelation_matrix_ti = [[1.0] * 99 for i in range(99)]

for i in range(99):
    for j in range(i+1, 99):
        raw_ti = [float(line) for line in open('spikes_record/'+str(i)+'a_on_trained.txt', 'r')]
        raw_ri = [float(line) for line in open('spikes_record/'+str(i)+'a_on_random.txt', 'r')]
        raw_ni = [float(line) for line in open('spikes_record/'+str(i)+'a_off_off.txt', 'r')]

        raw_ti_b = [float(line) for line in open('spikes_record/'+str(j)+'a_on_trained.txt', 'r')]
        raw_ri_b = [float(line) for line in open('spikes_record/'+str(j)+'a_on_random.txt', 'r')]
        raw_ni_b = [float(line) for line in open('spikes_record/'+str(j)+'a_off_off.txt', 'r')]


        ni_corr = (calculate_corr(raw_ni, raw_ni_b, bin)) 
        ti_corr = (calculate_corr(raw_ti, raw_ti_b, bin)) 
        ri_corr = (calculate_corr(raw_ri, raw_ri_b, bin)) 

        decorrelation_matrix_ni[i][j] = ni_corr
        decorrelation_matrix_ni[j][i] = ni_corr
        decorrelation_matrix_ti[i][j] = ti_corr
        decorrelation_matrix_ti[j][i] = ti_corr
        decorrelation_matrix_ri[i][j] = ri_corr
        decorrelation_matrix_ri[j][i] = ri_corr
        


pickle.dump(decorrelation_matrix_ni, open('matrix_ni_'+str(bin)+'.txt', 'w'))
pickle.dump(decorrelation_matrix_ti, open('matrix_ti_'+str(bin)+'.txt', 'w'))
pickle.dump(decorrelation_matrix_ri, open('matrix_ri_'+str(bin)+'.txt', 'w'))

print(decorrelation_matrix_ti)
