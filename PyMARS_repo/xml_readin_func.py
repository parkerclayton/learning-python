#this function reads in species from a .xml file and prints them out

import cantera as ct

def xmlreadin(data_file):
	spec= ct.Species.listFromFile(data_file)
	print(spec)

