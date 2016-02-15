#this function reads in species from a .xml file and prints them out

import cantera as ct
def xmlreadin(data_file):
	spec= ct.Species.listFromFile(data_file)
	print(spec)



	
#dummy list of species
spec=[ 'H4' , 'CO2' , 'C']
exc=[ 'Species H2', 'Species H', 'Species O']
	
#list of species to exclude	
	
#compares two lists of species, and removes the species in the second list from the first
def comparelist( spec, spec_exclude):
	for val in spec_exclude:
		if val in spec:
			spec.remove(val)
			print(spec) 


