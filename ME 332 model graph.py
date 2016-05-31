#ME 332 Centrifugal Pump - Model

import numpy as np
import matplotlib.pyplot as plt

#pump diameter = 8 in
#pump speed = 40pi rad/second

#Q is volumetric flow rate in ft^3/s
#dP is pressure rise across pump
#Raw Data
"""
0.17, 6.62
0.35, 6.65
0.61, 6.59
0.88, 6.30
1.11, 5.88
1.31, 5.36
1.51, 4.85
1.76, 3.93
1.96, 3.08
"""
pi=np.pi
"""-------------------------------------------------------------------------
                        Model Pump
-------------------------------------------------------------------------"""
Q1_raw=np.array([0.17, 0.35, 0.61, 0.88, 1.11, 1.31, 1.51, 1.76, 1.96 ])
dP1_raw=np.array([6.62, 6.65, 6.59, 6.30, 5.88, 5.36, 4.85, 3.93, 3.08])
w1= 40*pi          #radians/second
d1= 8.0/12.0             #feet
# fit a curve
z1=np.polyfit(Q1_raw, dP1_raw, 2)
y1=np.poly1d(z1)
#get curve points
Q1=np.linspace(0, 3, 100)
dP1=y1(Q1)

"""-------------------------------------------------------------------------
                        Prototype Pump
-------------------------------------------------------------------------"""
w2= 60*pi          #radians/second
d2= 1             #feet

Q2= Q1*(w2/w1)*((d2/d1)**3)
dP2= dP1*((w2/w1)**2)*((d2/d1)**2)





"plot visuals"
plt.axis([0, 14.0, 0, 35])
plt.title('Centrifugal Pump - Model')
plt.xlabel('Q (ft^3/s)')
plt.ylabel('dP (psi)')
plt.grid(True)

"plot the data"
plt.plot(Q1_raw, dP1_raw, 'ko ')
plt.plot(Q1, dP1, lw=2, label='model pump')
plt.plot(Q2, dP2, 'k', lw=2, label='prototype pump')
plt.legend()
plt.show()

#given flow rate, want to know dP
#print(y(.5))

#given change in pressure, want to know flow rate
#print(np.roots(4 - y))
