# imports numpy Library
import numpy
# import matplotlib pyplot Library and renames it to 'mplt'
import matplotlib.pyplot as mplt

# imports info from data file and stores it in a matrix labeled 'data'
data = numpy.loadtxt(fname='python-novice-inflammation/data/inflammation-01.csv', delimiter=',')

# creates a 10 x 3 max matrix of graphs
fig = mplt.figure(figsize=(10.0, 3.0))

# establishes names for each individual graph
axes1 = fig.add_subplot(1, 3, 1)
axes2 = fig.add_subplot(1, 3, 2)
axes3 = fig.add_subplot(1, 3, 3)

# sets graph 1 axes label, and provides data
axes1.set_ylabel('average')
axes1.plot(data.mean(axis=0))

# sets graph 2 axes label, and provides data
axes2.set_ylabel('max')
axes2.plot(data.max(axis=0))

# sets graph 3 axes label, and provides data
axes3.set_ylabel('min')
axes3.plot(data.min(axis=0))

# squeeze graphs closer together
fig.tight_layout()
# plots graph
mplt.show(fig)
