import pickle
import numpy
import random
from matplotlib import pyplot
from matplotlib import cm

a_ni_file = open('rate_ni_a.txt', 'r')
a_ti_file = open('rate_ti_a.txt', 'r')
a_ri_file = open('rate_ri_a.txt', 'r')
a_ni = pickle.load(a_ni_file)
a_ti = pickle.load(a_ti_file)
a_ri = pickle.load(a_ri_file)
b_ni_file = open('rate_ni_b.txt', 'r')
b_ti_file = open('rate_ti_b.txt', 'r')
b_ri_file = open('rate_ri_b.txt', 'r')
b_ni = pickle.load(b_ni_file)
b_ti = pickle.load(b_ti_file)
b_ri = pickle.load(b_ri_file)

fig = pyplot.figure()
ax1 = fig.add_subplot(231)
ax2 = fig.add_subplot(232)
ax3 = fig.add_subplot(233)
ax4 = fig.add_subplot(234)
ax5 = fig.add_subplot(235)
ax6 = fig.add_subplot(236)
#ax1 = fig.add_subplot(131)
#ax2 = fig.add_subplot(132)
#ax3 = fig.add_subplot(133)

cmap = cm.get_cmap('rainbow', 1000) # jet doesn't have white color
cmap.set_bad('w') # default value is 'k'

ax1.imshow(a_ni, interpolation="nearest", cmap=cmap)
ax1.grid(True)
ax2.imshow(a_ri, interpolation="nearest", cmap=cmap)
ax2.grid(True)
ax3.imshow(a_ti, interpolation="nearest", cmap=cmap)
ax3.grid(True)
ax4.imshow(b_ni, interpolation="nearest", cmap=cmap)
ax4.grid(True)
ax5.imshow(b_ri, interpolation="nearest", cmap=cmap)
ax5.grid(True)
ax6.imshow(b_ti, interpolation="nearest", cmap=cmap)
ax6.grid(True)

pyplot.show()
