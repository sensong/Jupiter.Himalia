import pickle
import random

trained_weights_file = open('trained_weights.txt', 'r')
random_weights_file = open('random_weights.txt', 'w')

trained_weights = pickle.load(trained_weights_file)

random_weights = []
for i in trained_weights:
    temp = []
    for j in i:
        temp.append(random.random()*0.7+0.3)
    random_weights.append(temp)

pickle.dump(random_weights, random_weights_file)


