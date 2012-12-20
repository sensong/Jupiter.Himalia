import pickle
import numpy
import random
from matplotlib import pyplot
from matplotlib import cm

ni_file = open('matrix_ni_200.txt', 'r')
ti_file = open('matrix_ti_200.txt', 'r')
ri_file = open('matrix_ri_200.txt', 'r')
ni = pickle.load(ni_file)
ti = pickle.load(ti_file)
ri = pickle.load(ri_file)


fig = pyplot.figure()
ax1 = fig.add_subplot(131)
ax2 = fig.add_subplot(132)
ax3 = fig.add_subplot(133)
cmap = cm.get_cmap('rainbow', 1000) # jet doesn't have white color
cmap.set_bad('w') # default value is 'k'
ax1.imshow(ni, interpolation="nearest", cmap=cmap)
ax1.grid(True)
ax2.imshow(ri, interpolation="nearest", cmap=cmap)
ax2.grid(True)
ax3.imshow(ti, interpolation="nearest", cmap=cmap)
ax3.grid(True)
pyplot.show()
