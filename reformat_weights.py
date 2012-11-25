import pickle

trained_weights_file = open('trained_weights.txt', 'r')
trained_weights = pickle.load(trained_weights_file)
#i = 0
#for m in mc:
    #j = 0
    #for g in m.dendrites.keys():
        #m.dendrites[g] = trained_weights[i][j]

avg = 0.0
total = 0.0
maxi = 0.0
mini = 1.0

excel = open('excel.csv', 'w')
for h in trained_weights:
    for k in h:
        excel.write(str(k)+'\n')
        avg += k
        total += 1.0
        if k>maxi:
            maxi = k
        if k<mini:
            mini = k
print(total, mini, avg/total, maxi)



