# this function reads in the data file, and determines what type of file it is


import cantera as ct
import os

def readin(data_file):
	if data_file.endswith(".xml"):
		print("This is an Cantera xml file")
		from xml_readin_func import xmlreadin
		xmlreadin(data_file)
	elif data_file.endswith(".inp"):
		print("This is a Chemkin inp file")
	elif data_file.endswith(".cti"):
		print("This is a Cantera cti file")
	else:
		print("File type not supported")
		


readin("gri30.xml")