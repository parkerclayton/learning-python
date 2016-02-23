# this function reads in the data file , and determines what type of file it is
#it then calls the appropriate function depending on data filetype
#the data file called must be in the same directory


import cantera as ct
import os

#demo species exclusion list
exclusion_list=['H2', 'H']

def readin(data_file):
	if data_file.endswith(".xml"):
		print("This is an Cantera xml file")
		from xml_readin_func import xmlreadin				#imports and calls xml_readin_func
		xmlreadin(data_file, exclusion_list)		
	elif data_file.endswith(".inp"):
		print("This is a Chemkin inp file")
	elif data_file.endswith(".cti"):
		print("This is a Cantera cti file")
	else:
		print("File type not supported")
		


