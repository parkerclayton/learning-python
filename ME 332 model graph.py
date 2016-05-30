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

Q=np.array([0.17, 0.35, 0.61, 0.88, 1.11, 1.31, 1.51, 1.76, 1.96 ])

dP=np.array([6.62, 6.65, 6.59, 6.30, 5.88, 5.36, 4.85, 3.93, 3.08])

# fit a curve
z=np.polyfit(Q, dP, 2)
y=np.poly1d(z)
#get curve points
zp=np.linspace(0, 2, 100)
yp=y(zp)


"plot visuals"
plt.axis([0, 2.0, 0, 8])
plt.title('Centrifugal Pump - Model')
plt.xlabel('Q (ft^3/s)')
plt.ylabel('dP (psi)')
plt.grid(True)

"plot the data"
plt.plot(Q, dP, 'ko ')
plt.plot(zp, yp)
#plt.show()

#given flow rate, want to know dP
#print(y(.5))

#given change in pressure, want to know flow rate
#print(np.roots(4 - y))
