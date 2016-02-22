#series of functions to work with Cantera xml file

import cantera as ct
import os   #used to read-in file from directory (possibly no longer necessary)
import xml.etree.ElementTree as ET



#function to read in an xml file and print out species names
def xmlreadin(data_file, exclusion_list):
	#prints a status, and then reads in the list of Species from the xml file
	print("xmlreadin function running...")
	Species= ct.Species.listFromFile(data_file)
	print(Species)  

	tree=ET.parse(data_file) #this reads in the data from the xml file
	root=tree.getroot()		#identifies the root of the xml file and prints it
	print(root.tag)
	for child in root:		#prints out all the children nodes the root Element
		print child.tag
	
	
	
	#compare-list to be used later
	"""for val in exclusion_list:
		if val in Species:
			Species.remove(val)
	print(Species)"""


#list to exclude
SPexc=['Species H2', 'H'];

xmlreadin("gri30.xml", SPexc)












#old reference...commented out for now. everything above works	
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
