#1 usr/bin/python

import cantera as ct 
import cantera.ctml_writer as ctw
import numpy as np
import matplotlib.pyplot as mplt


#ask user for input
response = raw_input("Enter Species names separated by spaces: ")

species = response.split(" ")
print(species)

#some acceptable species are H2 H O O2 OH H2O HO2 H2O2 C CH
#              CH2 CH2(S) CH3 CH4 CO CO2 HCO CH2O CH2OH CH3O
 #             CH3OH C2H C2H2 C2H3 C2H4 C2H5 C2H6 HCCO CH2CO HCCOH
  #            N NH NH2 NH3 NNH NO NO2 N2O HNO CN
   #           HCN H2CN HCNN HCNO HOCN HNCO NCO N2 AR C3H7
    #          C3H8 CH2CHO CH3CHO """ 
              
	


"""<!-- species CH2(S) (this information should be read in from a text file)    -->
    <species name="CH2(S)">
      <atomArray>H:2 C:1 </atomArray>
      <note>L S/93</note>
      <thermo>
        <NASA Tmax="1000.0" Tmin="200.0" P0="100000.0">
           <floatArray name="coeffs" size="7">
             4.198604110E+00,  -2.366614190E-03,   8.232962200E-06,  -6.688159810E-09, 
             1.943147370E-12,   5.049681630E+04,  -7.691189670E-01</floatArray>
        </NASA>
        <NASA Tmax="3500.0" Tmin="1000.0" P0="100000.0">
           <floatArray name="coeffs" size="7">
             2.292038420E+00,   4.655886370E-03,  -2.011919470E-06,   4.179060000E-10, 
             -3.397163650E-14,   5.092599970E+04,   8.626501690E+00</floatArray>
        </NASA>
      </thermo>
      <transport model="gas_transport">
        <string title="geometry">linear</string>
        <LJ_welldepth units="K">144.000</LJ_welldepth>
        <LJ_diameter units="A">3.800</LJ_diameter>
        <dipoleMoment units="Debye">0.000</dipoleMoment>
        <polarizability units="A3">0.000</polarizability>
        <rotRelax>0.000</rotRelax>
      </transport>
    </species>
    """




