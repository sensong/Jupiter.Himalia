import pickle
import numpy
from matplotlib import pyplot
from matplotlib import cm

matrix = pickle.load(open('decorr_matrix_in.txt', 'r'))
#A = numpy.random.randint(10, 100, 100).reshape(10, 10)
A = numpy.array(matrix)
#mask =  numpy.tri(A.shape[0], k=-1)
#A = numpy.ma.array(A, mask=mask) # mask out the lower triangle
fig = pyplot.figure()
ax1 = fig.add_subplot(111)
cmap = cm.get_cmap('rainbow', 1000) # jet doesn't have white color
cmap.set_bad('w') # default value is 'k'
ax1.imshow(A, interpolation="nearest", cmap=cmap)
ax1.grid(True)
pyplot.show()
