import math
from itertools import imap
a_ni = [line.split() for line in open("a_noinh_pattern.txt", 'r').readlines()[10:80]]
a_ri = [line.split() for line in open("a_random_pattern.txt", 'r').readlines()[10:80]]
a_ti = [line.split() for line in open("a_trained_pattern.txt", 'r').readlines()[10:80]]
b_ni = [line.split() for line in open("b_noinh_pattern.txt", 'r').readlines()[10:80]]
b_ri = [line.split() for line in open("b_random_pattern.txt", 'r').readlines()[10:80]]
b_ti = [line.split() for line in open("b_trained_pattern.txt", 'r').readlines()[10:80]]
for i in range(70):
    for j in range(99):
        a_ni[i][j] = float(a_ni[i][j])
        a_ri[i][j] = float(a_ri[i][j])
        a_ti[i][j] = float(a_ti[i][j])
        b_ni[i][j] = float(b_ni[i][j])
        b_ri[i][j] = float(b_ri[i][j])
        b_ti[i][j] = float(b_ti[i][j])

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



corrs = []
for i in range(70):
    corr = []
    corr.append(pearsonr(a_ni[i], b_ni[i]))
    corr.append(pearsonr(a_ri[i], b_ri[i]))
    corr.append(pearsonr(a_ti[i], b_ti[i]))
    corrs.append(corr)

best = []
random =[]
for i in [(i-1.0)/10.0 for i in range(11)]:
    best_value = 0
    best_index = -1
    random_list = []
    for j in range(70):
        if i<=corrs[j][0]<=i+0.1:
            random_list.append(j)
            if corrs[j][2]-corrs[j][0] < best_value:
                best_value = corrs[j][2]-corrs[j][0] 
                best_index = j
    random_index = random_list[0]
    if random_index == best_index:
        random_index = random_list[1]
    best.append([best_index, random_index])

finalt = []
for i in best:
    finalt += i

final = []
for i in finalt:
    if i!=6 and i!=1:
        final.append(i)

print(final)

def sparsityr(vector):
    mean = float(sum(vector))/float(len(vector))
    sqrmean = [i**2 for i in vector]
    sqrmean = float(sum(sqrmean))/float(len(vector))
    sparsity = mean**2/sqrmean
    return sparsity


spars = []
for f in final:
    spars.append([sparsityr(a_ni[f]), sparsityr(a_ri[f]), sparsityr(a_ti[f]), sparsityr(b_ti[f])])



correlation_file = open('sparsity.txt', 'w')
for i in spars:
    for j in range(4):
        correlation_file.write(str(i[j])+' ')
    correlation_file.write('\n')


for i in range(4):
    temp = [x[i] for x in spars]
    s = sum(temp) / (len(temp)+0.0)
    print(s)





