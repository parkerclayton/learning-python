
#imports numpy module
import numpy

# imports info from data file and stores it in a matrix labeled 'data'
data = numpy.loadtxt(fname='python-novice-inflammation/data/inflammation-01.csv', delimiter=',')

#import matplotlib pyplot module#

import matplotlib.pyplot

#this populates a matrix with the data, and stores it in an image variable
image = matplotlib.pyplot.imshow(data)
#this plots the matrix
matplotlib.pyplot.show(image)

#looking at the averages of inflammation over time

ave_inflammation = data.mean(axis=0)
ave_plot = matplotlib.pyplot.plot(ave_inflammation)
matplotlib.pyplot.show(ave_plot)

# looking at the average per day across all patients
max_plot = matplotlib.pyplot.plot(data.max(axis=0))
matplotlib.pyplot.show(max_plot)








