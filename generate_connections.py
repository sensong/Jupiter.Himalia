import pickle
import random
import copy

connections_file = open('connection_list.txt', 'w')
source_pattern1_file = open('source_pattern_a.txt', 'w')
source_pattern2_file = open('source_pattern_b.txt', 'w')


mc = [i for i in range(99)]
gc = [i for i in range(801)]
each_gc_connects_to_how_many_mc = 20

connection_list = []

for i in gc:
    connection_list.append(random.sample(mc, each_gc_connects_to_how_many_mc))

pickle.dump(connection_list, connections_file)

pattern_a = []
for i in mc:
    pattern_a.append(20.0+10.0*random.random())
pickle.dump(pattern_a, source_pattern1_file)

pattern_b = copy.deepcopy(pattern_a)
for i in random.sample(mc, 4):
    pattern_b[i] = 20.0 + 10.0*random.random()
pickle.dump(pattern_b, source_pattern2_file)
