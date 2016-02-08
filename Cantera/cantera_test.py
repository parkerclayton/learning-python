#1 usr/bin/python

import cantera as ct 
import cantera.ctml_writer as ctw
import numpy as np
import matplotlib.pyplot as mplt


#ask user for input
response = raw_input("Enter Species names separated by spaces: ")
print(response)
response = response.split(" ")
print(response)

A=ctw.species(name='response[1]')
print(A)




