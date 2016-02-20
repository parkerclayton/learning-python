#series of functions to work with Cantera xml file

import cantera as ct
import os



#function to read in an xml file and print out species names
def xmlreadin(data_file):
	spec= ct.Species.listFromFile(data_file)
	print(spec)



#commented out for now. everything above works	
"""#dummy list of species
spec=[ 'H4' , 'CO2' , 'C']	
#list of species to exclude	
exc=[ 'H4', 'H', 'O']


#compares two lists of species, and removes the species in the second list from the first
def comparelist( spec, spec_exclude):
	for val in spec_exclude:
		if val in spec:
			spec.remove(val)
	print(spec) 

#import species from xml (use this to import 
species= ct.Species('gri30:all') 

print(species)"""
