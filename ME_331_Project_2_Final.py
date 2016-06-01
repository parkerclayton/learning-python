# ME 332 reynolds number calculation

import numpy as np
import matplotlib.pyplot as plt


"""----------------------------------------------------------------------------
                            Constants
----------------------------------------------------------------------------"""

pi=np.pi
#gravity
g=32.17
#specific gravity of water
SG=1
#viscosity of water at room temp (68F)
u=2.09e-5                                                       #slug/ft*s
#density of water
rho= 62.427961                                                  #lb/ft^3
#Kinematic viscosity of water at room temp (68F) pronounced "nu"
#1 cst= 10^-6 m^2/s
v=1.01                                                          #cst
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
def func(x, c, a, b):
    return a*np.exp(-c*x) + b
    #first number is steepness guess, second is translation guess, third is
    #vertical translation

#gate valve data from p. 382 Table 6.5
gvDraw=[1, 2, 4, 8, 20]                                            # inches
gvKraw=[.8, .35, .16, .07, .03]                                    #K

gvD_points=np.linspace(.01, 24, 100)
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
d1i=d1*12                                                      #in inches
#average velocity of flow
V1=(4*Q1)/(pi*(d1**2))
#Reynolds number
Re1=7745.8*((V1*d1i)/v)
#friction factor (need to modify so either Re or d is only one value)
f1= (1/(-1.8*np.log((6.9/Re1) + (((e/d1)/3.7)**1.11))))**2

k1_elbow = func(d1i, .4, .45, .21)
k1_valve = func(d1i, .6, 1.4, .05)

#head loss
k1_total=k_sharp + 4*k1_elbow + k1_valve

h1_l= ((V1**2)/(2*g))*( ((f1*L)/d1) + k1_total)

#energy eq for pump head
h_p1= (dy + h1_l)*.433*SG
state_1_q=np.ones(100)*Q1



"""----------------------------------------------------------------------------
                            State 2 (Q=8 ft^3/s)
----------------------------------------------------------------------------"""

Q2= 8.0                                                           #ft^3/s
#reynolds number for second flow rate vs pipe diameter
Re2=[]
d2=np.linspace(.5, 2, 100)                                     #feet
d2i=d2*12                                                       #inches

#average velocity of flow
V2=(4*Q2)/(pi*(d2**2))
#Reynolds number
Re2=7745.8*((V2*d2i)/v)
#friction factor (need to modify so either Re or d is only one value)
f2= (1/(-1.8*np.log((6.9/Re2) + (((e/d2)/3.7)**1.11))))**2

k2_elbow = func(d2i, .4, .45, .21)
k2_valve = func(d2i, .6, 1.4, .05)

#head loss
k2_total=k_sharp + 4*k2_elbow + k2_valve

h2_l= ((V2**2)/(2*g))*( ((f2*L)/d2) + k2_total)

#energy eq for pump head
h_p2= (dy + h2_l)*.433*SG

state_2_q=np.ones(100)*Q2


"""-------------------------------------------------------------------------
                        Model Pump
-------------------------------------------------------------------------"""
Q1_raw=np.array([0.17, 0.35, 0.61, 0.88, 1.11, 1.31, 1.51, 1.76, 1.96 ])
dP1_raw=np.array([6.62, 6.65, 6.59, 6.30, 5.88, 5.36, 4.85, 3.93, 3.08])
w1= 40*pi          #radians/second
d1_pump= 8.0/12.0             #feet
# fit a curve
z1=np.polyfit(Q1_raw, dP1_raw, 2)
y1=np.poly1d(z1)
#get curve points
Q1_pump=np.linspace(0, 3, 100)
dP1=y1(Q1_pump)

"""-------------------------------------------------------------------------
                        Prototype Pump
-------------------------------------------------------------------------"""
w2= 60*pi          #radians/second
d2_pump= 1             #feet

Q2_pump= Q1_pump*(w2/w1)*((d2_pump/d1_pump)**3)
dP2= dP1*((w2/w1)**2)*((d2_pump/d1_pump)**2)





"""----------------------------------------------------------------------------
                            PLOTTING
----------------------------------------------------------------------------"""

plot_type="head_curve"

if plot_type == "head_curve":
    "plot model and prototype pump visuals"
    plt.axis([0, 14.0, 0, 35])
    plt.title('Centrifugal Pump - Model')
    plt.xlabel('Q (ft^3/s)')
    plt.ylabel('dP (psi)')
    plt.grid(True)
    plt.plot(Q1_raw, dP1_raw, 'ko ')
    plt.plot(Q1_pump, dP1, lw=2, label='model pump')
    plt.plot(Q2_pump, dP2, 'k', lw=2, label='prototype pump')
    "plot pump head on pump head graph"
    plt.plot(state_1_q, h_p1, label ='6 ft^3/s')
    plt.plot(state_2_q, h_p2, label = '8 ft^3/s')
    plt.legend()

if plot_type =="DvRe":
    #plot pipe diameter vs reynolds number
    plt.plot(d1i, Re1, 'r', label='6 ft^3/s', lw=2)
    plt.plot(d2i, Re2, 'k', label='8 ft^3/s', lw=2)
    #plot turbulent flow boundary
    plt.plot((6, 24), (2300, 2300), 'g', label='laminar flow boundary', lw=2)
    plt.plot((6, 24), (4000, 4000), 'b', label='turbulent flow boundary', lw=2)
    plt.legend()
    plt.xlabel('pipe diameter (in)')
    plt.ylabel('Reynolds number (Re)')
    plt.grid(True)
    plt.axis([6, 24, 0, 1000000])

if plot_type == "DvV":
    #plot pipe diameter vs average velocity of flow
    plt.plot(d1i, V1, 'r', label='6 ft^3/s', lw=2)
    plt.plot(d2i, V2, 'k', label= '8 ft^3/s', lw=2)
    plt.legend()
    plt.xlabel('pipe diameter (in)')
    plt.ylabel('Average Velocity (ft/s)')
    plt.grid(True)
    plt.axis([6, 24, 0, 45])

if plot_type =="DvFf":
    #plots friction factor vs pipe diameter
    plt.plot(d1i, f1, 'r', label='6 ft^3/s')
    plt.plot(d2i, f2, 'k', label= '8 ft^3/s')
    plt.legend()
    plt.xlabel('pipe diameter (in)')
    plt.ylabel('Friction factor (ft)')
    plt.grid(True)
    #plt.axis([0, 12, 0, 200])

if plot_type =="gate_valve":
    #plots gate valve data
    plt.plot(gvDraw, gvKraw, 'rx', ms=5, mew=2)
    plt.plot(gvD_points,gvKn, lw=2)
    plt.xlabel('pipe diameter (in)')
    plt.ylabel('Resistance coefficient (k)')
    plt.grid(True)
    plt.axis([0, 24, 0, 1])

if plot_type =="elbow_valve":
    plt.plot(eDraw, eKraw, 'rx')
    plt.plot(eD_points, eKn, lw=2)
    plt.xlabel('pipe diameter (in)')
    plt.ylabel('Resistance coefficient (k)')
    plt.grid(True)
    plt.axis([0, 24, 0, 1])

plt.show()
