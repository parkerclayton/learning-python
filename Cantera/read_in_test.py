

#decide what path to take based on file extension type

import os

#gets current working directory
cd=os.getcwd()
print(cd)

#goes up to to parent directory
os.chdir(os.pardir)

#prints current directory
print(os.getcwd())

#lists files in the "Data" directory and then assigns the first one to a variable
#so that I can evaluate its extension
print(os.listdir("Data"))

File=os.listdir("Data")
print(File)

for files in File:
	n=0
	n=n+1
	print(n)
	if files.endswith(".cti"):
		print("Success!") 
	else:
		print("Nein!")
		
		
def readin(fname):
	fname=os.listdir(fname)
	print(fname)
	
readin("Data")
	