
#imports numpy module
import numpy

# imports info from data file and stores it in a matrix labeled 'data'
data = numpy.loadtxt(fname='python-novice-inflammation/data/inflammation-01.csv', delimiter=',')

#import matplotlib pyplot module and renames it to 'mplt'

import matplotlib.pyplot as mplt

#this populates a matrix with the data, and stores it in an image variable
image =mplt.imshow(data)
mplt.title('Heatmap of data')
#this plots the matrix
mplt.show(image)
mplt.title('Average Inflammation over Time')

#looking at the averages of inflammation over time

ave_inflammation = data.mean(axis=0)
ave_plot = mplt.plot(ave_inflammation)
mplt.show(ave_plot)
mplt.title('Maximum Value Along 1st Axis')

# looking at the average per day across all patients
max_plot = mplt.plot(data.max(axis=0))
mplt.show(max_plot)
mplt.title('Minimum Value Along 1st Axis')









