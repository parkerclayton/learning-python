# ME 332 reynolds number calculation

import numpy as np
import matplotlib.pyplot as plt
pi=np.pi
"""----------------------------------------------------------------------------
                            Constants
----------------------------------------------------------------------------"""
#gravity
g=32.17
#viscosity of water at room temp (68F)
u=2.09e-5                                                       #slug/ft*s
#density of water
rho= 62.427961                                                  #lb/ft^3
#Kinematic viscosity of water at room temp (68F) pronounced "nu"
v=1.0867e-5                                                     #ft^2/s
#Galvanized Iron absolute roughness (epsilon or curly e)
e=.0005                                                         #feet
#relative roughness is e/diameter

#Reynolds number < 2300 is laminar
#Reynolds number > 2300 is laminar

#total length of pipe system
L=1640.42                                                       #feet

#sharp edge inlet resistance coefficient
k_sharp= .5

#change in elevation
dy=32.8084


"""----------------------------------------------------------------------------
                    Component Resistance Coefficient (K) Data
----------------------------------------------------------------------------"""

#gate valve data from p. 382 Table 6.5
gvDraw=[1, 2, 4, 8, 20]                                            # inches
gvKraw=[.8, .35, .16, .07, .03]                                    #K


gvD_points=np.linspace(.01, 24, 100)

def func(x, c, a, b):
    return a*np.exp(-c*x) + b
    #first number is steepness guess, second is translation guess, third is
    #vertical translation
gvKn=func(gvD_points, .6, 1.4, .05)

#90 degree elbow data from p. 382 Table 6.5
eDraw=[1, 2, 4, 8, 20]
eKraw=[.5, .39, .3, .26, .21]

eD_points=np.linspace(.01, 24, 100)
eKn=func(eD_points, .4, .45, .21)

"""----------------------------------------------------------------------------
                            State 1 (Q=6 ft^3/s)
----------------------------------------------------------------------------"""


Q1= 6                                                           #ft^3/s
#reynolds number for first flow rate vs pipe diameter
Re1=[]
d1=np.linspace( .5, 2, 100)                                    #feet
d1i=d1*12                                                       #in inches
Re1=7745.8*((v*d1)/v)
#average velocity of flow
V1=(4*Q1)/(pi*(d1**2))
#friction factor (need to modify so either Re or d is only one value)
f1= (1/(-1.8*np.log((6.9/Re1) + (((e/d1)/3.7)**1.11))))**2


"""----------------------------------------------------------------------------
                            State 2 (Q=8 ft^3/s)
----------------------------------------------------------------------------"""

Q2= 8                                                           #ft^3/s
#reynolds number for second flow rate vs pipe diameter
Re2=[]
d2=np.linspace(.5, 2, 100)                                     #feet
d2i=d2*12                                                       #inches
Re2=7745.8*((v*d2i)/v)
#average velocity of flow
V2=(4*Q2)/(pi*(d2**2))
#friction factor (need to modify so either Re or d is only one value)
f2= (1/(-1.8*np.log((6.9/Re2) + (((e/d2)/3.7)**1.11))))**2






"""----------------------------------------------------------------------------
                        Steady Flow Energy Equation
----------------------------------------------------------------------------"""
#head loss
#k_total=k_sharp + 4*k_elbow + k_valve

#h_l= ((V**2)/(2*g))*( ((f*L)/d) + k_total)

#energy eq for pump head
#h_p= dy + h_l




"""----------------------------------------------------------------------------
                            PLOTTING
----------------------------------------------------------------------------"""

"""
#plot pipe diameter vs reynolds number
plt.subplot(311)
plt.plot(d1i, Re1, 'r', label='6 ft^3/s', lw=2)
plt.plot(d2i, Re2, 'k', label='8 ft^3/s', lw=2)
#plot turbulent flow boundary
plt.plot((6, 24), (2300, 2300), 'g', label='laminar flow boundary', lw=2)
plt.plot((6, 24), (4000, 4000), 'b', label='turbulent flow boundary', lw=2)
plt.legend()
plt.xlabel('pipe diameter (in)')
plt.ylabel('Reynolds number (Re)')
plt.grid(True)
plt.axis([6, 24, 0, 100000])


#plot pipe diameter vs average velocity of flow
plt.subplot(312)
plt.plot(d1i, V1, 'r', label='6 ft^3/s', lw=2)
plt.plot(d2i, V2, 'k', label= '8 ft^3/s', lw=2)
plt.legend()
plt.xlabel('pipe diameter (in)')
plt.ylabel('Average Velocity (ft/s)')
plt.grid(True)
plt.axis([6, 24, 0, 45])


#plots friction factor vs pipe diameter
plt.subplot(313)
plt.plot(d1i, f1, 'r', label='6 ft^3/s')
plt.plot(d2i, f2, 'k', label= '8 ft^3/s')
plt.legend()
plt.xlabel('pipe diameter (in)')
plt.ylabel('Friction factor (ft)')
plt.grid(True)
#plt.axis([0, 12, 0, 200])


#plots gate valve data
plt.subplot(313)
plt.plot(gvDraw, gvKraw, 'rx', ms=5, mew=2)
plt.plot(gvD_points,gvKn, lw=2)
plt.xlabel('pipe diameter (in)')
plt.ylabel('Resistance coefficient (k)')
plt.grid(True)
plt.axis([0, 24, 0, 1])
"""
plt.subplot(111)
plt.plot(eDraw, eKraw, 'rx')
plt.plot(eD_points, eKn, lw=2)
plt.xlabel('pipe diameter (in)')
plt.ylabel('Resistance coefficient (k)')
plt.grid(True)
plt.axis([0, 24, 0, 1])


plt.show()
