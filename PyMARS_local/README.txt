Currently, only .xml files are supported.

1.	To get started make sure the .xml file is in the same directory. 
	An example gri30.xml file is also provided

2.	Pass in the xml file from terminal by calling
	python -c "execfile('file_extension_func.py'); readin('data file')"
	where 'data_file' is the xml file
	
	an example is: python -c "execfile('file_extension_func.py'); readin('gri30.xml')"
	a demo species-exclude list is also included

3. a new xml data file is created in the same directory, and titled "output.xml"
