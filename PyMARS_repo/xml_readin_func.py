#function to read in an xml file and print out species names

import cantera as ct
import xml.etree.ElementTree as ET


def xmlreadin(data_file, exclusion_list):
	print("xmlreadin function running...") 					#prints a status, and then reads in the list of Species from the xml file using cantera
	

	tree=ET.parse(data_file) 								#this reads in the data from the xml file
	root=tree.getroot()										#identifies the root of the xml file and prints it
	print('the root is %s') % root.tag
	for child in root:										#iterates over all the subElements
		if child.tag == "speciesData":  					#finds SpeciesData subElement and compiles to list
			Species_List=[]									#starts a blank list
			for Species in child:
				Species_List.append(Species.attrib['name']) #.attrib get the attribute for the Species Element, which in this case is 'name' and then ['name'] calls the string assigned to namein the dictionary. list.append then adds them to a list
			print(Species_List)
	for val in exclusion_list:
		if val in Species_List:								
			Species_List.remove(val)						#removes any strings found in the exclusion list from the Species_List
	print(Species_List)	

			



#calling the function
#list to exclude
SPexc=['H2', 'H'];

xmlreadin("gri30.xml", SPexc)





			
	

#ignore everything below -----------------------------------------------------

	#compare-list to be used later
"""for val in exclusion_list:
		if val in Species:
			Species.remove(val)
	print(Species)"""



#Species= ct.Species.listFromFile(data_file)
	#print(Species)  



#old reference...commented out for now.
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
