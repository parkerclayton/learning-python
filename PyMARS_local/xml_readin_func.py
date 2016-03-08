#function to read in an xml file and print out species names

import cantera as ct

#used when calling the function locally when testing
#exclusion_list=['H2']

def xmlreadin(data_file, exclusion_list):
	Solution = ct.Solution(data_file)
	
	
	Species = Solution.species_names
	for n in exclusion_list:
		if n in Species:
			Species.remove(n)
	Species	=	[Solution.species(name) for name in Species] #get objects
	
	
	ReactionList 	= 	Solution.reaction_equations()
	ReactionObjects	=	Solution.reaction
	list	=	[]
	for i, Rxn in enumerate(ReactionList):
		Reactants 	= 	ReactionObjects(i).reactants
		Products	= 	ReactionObjects(i).products
		for k in exclusion_list:
			if k not in Reactants and k not in Products:
				list.append(Solution.reaction(i))
				
	ReactionObjects = list


	
	

		

				
				
		

#reactions returns a list of all solution objects
#reaction returns the individual object
#make list of individual objects using Solution.reaction(index)
#read into new solution
			
			
	
#calling the function
#list to exclude
SPexc=['O2'];

xmlreadin("gri30.xml", SPexc)			
			
			
			
			
			
			
			
			
			
			
	

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
