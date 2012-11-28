import random
import pickle

mc = [2.5, 5.5, 8.5]
gc = list(range(1, 11))

gc2mc = []
for i in gc:
    gc2mc.append(random.sample(mc, 2))
print(gc2mc)

f = open('gc2mc.txt', 'w')
pickle.dump(gc2mc, f)
