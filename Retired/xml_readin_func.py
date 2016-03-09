#function to read in an xml file and print out species names

import cantera as ct
import xml.etree.ElementTree as ET
import os

#used when calling the function locally when testing
#exclusion_list=['H2']

def xmlreadin(data_file, exclusion_list):
	print("xmlreadin function running...") 									#prints a status, and then reads in the list of Species from the xml file using cantera

	tree=ET.parse(data_file) 												#this reads in the data from the xml file
	root=tree.getroot()														#identifies the root of the xml file and prints it
	for child in root:														#iterates over all the subElements
		if child.tag == "speciesData":  									#finds SpeciesData subElement and compiles to list
			speciesData=child												#defines the SpeciesData subElement
			Species_List=[]													#starts a blank list								
			for Species in speciesData:
				Species_List.append(Species.attrib['name']) 				# get the name attribute for the Species Element and append to a list
				if Species.attrib['name'] in exclusion_list:				#if the name is in the exclusion list, print it, and remove it from the xml file
					print('Species to Remove: %s') % Species.get('name')
					speciesData.remove(Species)
			#print("Original Species List: %s") % Species_List
	"""for Species in root.iter('speciesArray'):
		print(Species.text)
		for val in exclusion_list:
			if val in Species.text:
				Species.remove(val)
				print(val)"""
				
				
	for val in exclusion_list:												#prints an updated species list
		if val in Species_List:								
			Species_List.remove(val)													
	#print("Reduced Species List: %s") %Species_List	
	tree.write('output.xml')												#writes out xml data to a new file titled "output.xml'
	os.system("open " + 'output.xml')										#opens the new xml file for review


#this is used for calling the function locally when testing
#xmlreadin('gri30.xml', exclusion_list)





			
	

#ignore everything below -----------------------------------------------------


#calling the function
#list to exclude
"""SPexc=['H2', 'H'];

xmlreadin("gri30.xml", SPexc)"""


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
