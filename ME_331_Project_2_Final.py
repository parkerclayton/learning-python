# ME 332 reynolds number calculation

import numpy as np
import matplotlib.pyplot as plt


"""----------------------------------------------------------------------------
                            Constants
----------------------------------------------------------------------------"""

pi=np.pi
#gravity
g=32.17                                                     #ft/s^2
#specific gravity of water
SG=1
#pump efficencty
eta=.75
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
dy=32.8084                                                  #feet


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

gvD_points=np.linspace(.01, 24, 100)                  #pipe diameter in inches
gvKn=func(gvD_points, .6, 1.4, .05)

#90 degree elbow data from p. 382 Table 6.5
eDraw=[1, 2, 4, 8, 20]                              #pipe diameter in inches
eKraw=[.5, .39, .3, .26, .21]                       #K values

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
V1=(4*Q1)/(pi*(d1**2))                                          #ft/s
#Reynolds number
Re1=7745.8*((V1*d1i)/v)
#friction factor (need to modify so either Re or d is only one value)
f1= (1/(-1.8*np.log((6.9/Re1) + (((e/d1)/3.7)**1.11))))**2

k1_elbow = func(d1i, .4, .45, .21)
k1_valve = func(d1i, .6, 1.4, .05)

#head loss
k1_total=k_sharp + 4*k1_elbow + k1_valve

h1_l= ((V1**2)/(2*g))*( ((f1*L)/d1) + k1_total)                    #feet
h1_l_mod= ((V1**2)/(2*g))*( ((f1*L)/d1) )

#energy eq for pump head
h_p1= (dy + h1_l)*.433*SG                                       #PSI
state_1_q=np.ones(100)*Q1

#pump power required
Power1=(SG*h1_l*(Q1*448.831)/(3960*eta)) #where 448 converts from ft^3/s to gal/min



"""----------------------------------------------------------------------------
                            State 2 (Q=8 ft^3/s)
----------------------------------------------------------------------------"""

Q2= 8.0                                                           #ft^3/s
#reynolds number for second flow rate vs pipe diameter
Re2=[]
d2=np.linspace(.5, 2, 100)                                     #feet
d2i=d2*12                                                       #inches

#average velocity of flow
V2=(4*Q2)/(pi*(d2**2))                                         #ft/s
#Reynolds number
Re2=7745.8*((V2*d2i)/v)
#friction factor (need to modify so either Re or d is only one value)
f2= (1/(-1.8*np.log((6.9/Re2) + (((e/d2)/3.7)**1.11))))**2

k2_elbow = func(d2i, .4, .45, .21)
k2_valve = func(d2i, .6, 1.4, .05)

#head loss
k2_total=k_sharp + 4*k2_elbow + k2_valve

h2_l= ((V2**2)/(2*g))*( ((f2*L)/d2) + k2_total)                 #feet
h2_l_mod= ((V2**2)/(2*g))*( ((f2*L)/d2) )

#energy eq for pump head
h_p2= (dy + h2_l)*.433*SG                                       #PSI

state_2_q=np.ones(100)*Q2

#pump power required
Power2=(SG*h2_l*(Q2*448.831)/(3960*eta)) #where 448 converts from ft^3/s to gal/min
                                                                #Hp


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
"""-------------------------------------------------------------------------
                        Optimization
-------------------------------------------------------------------------"""
#enumerate, first is index, 2nd is val

#val = np.isclose(h_p1[i], dP2[i], atol=.1)

#state 1----------------------------------------------
#get dP on head curve line for 6 ft^3/s
for i, k in enumerate(Q2_pump):
    val= np.isclose(k, 6, atol=.1)
    if val == True:
        dP1_max=dP2[i]
        ix1=i
# get hp_p1 (point on vertical line)
for i, k in enumerate(h_p1):
    val= np.isclose(k, dP1_max, atol=.4)
    if val == True:
        h_p1_max=h_p1[i]
        i1=i
#use i1 (index) to get the rest of the values

k1_elbow_max = func(d1i[i1], .4, .45, .21)
k1_valve_max = func(d1i[i1], .6, 1.4, .05)
h1_l_max=h1_l[i1]
f1_max= f1[i1]
V1_max=V1[i1]
Re1_max=Re1[i1]
d1_max=d1i[i1]
Power1_max= Power1[i1]

#print('State 1 Max: kElbow, kValve, Hl, f, Re, d ')
#print(k1_elbow_max, k1_valve_max, h1_l_max, f1_max, Re1_max, d1_max)



#state 2--------------------------------------------
#get dP on head curve line for 8 ft^3/s
for i, k in enumerate(Q2_pump):
    val= np.isclose(k, 8, atol=.1)
    if val == True:
        dP2_max=dP2[i]
        ix2=i

# get hp_p2 (point on vertical line)
for i, k in enumerate(h_p2):
    val= np.isclose(k, dP2_max, atol=.2)
    if val == True:
        h_p2_max=h_p2[i]
        i2=i
#use i2 (index) to get the rest of the values

k2_elbow_max = func(d2i[i2], .4, .45, .21)
k2_valve_max = func(d2i[i2], .6, 1.4, .05)
h2_l_max=h2_l[i2]
f2_max= f2[i2]
V2_max=V2[i2]
Re2_max=Re2[i2]
d2_max=d2i[i2]
Power2_max=Power2[i2]

#print('State 2 Max: kElbow, kValve, Hl, f, Re, d ')
#print(k2_elbow_max, k2_valve_max, h2_l_max, f2_max, Re2_max, d2_max)

"""----------------------------------------------------------------------------
                            PLOTTING
----------------------------------------------------------------------------"""

plot_type="PWRvV"

if plot_type == "head_curve":
    "plot model and prototype pump visuals"
    plt.axis([0, 14.0, 0, 35])
    plt.title('Pump Head Curve')
    plt.xlabel('Q (ft^3/s)')
    plt.ylabel('dP (psi)')
    plt.grid(True)
    plt.plot(Q1_raw, dP1_raw, 'ko ')
    plt.plot(Q1_pump, dP1, lw=2, label='model pump')
    plt.plot(Q2_pump, dP2, 'k', lw=2, label='prototype pump')
    "plot pump head on pump head graph"
    plt.plot(state_1_q, h_p1, label ='6 ft^3/s', color='g', lw=1.5)
    plt.plot(state_2_q, h_p2, label = '8 ft^3/s', color='c', lw=1.5)
    "plot max values"
    plt.plot(Q2_pump[ix1], h_p1_max, 'rx', mew=2, ms=10)
    plt.plot(Q2_pump[ix2], h_p2_max, 'rx', mew=2, ms=10)
    plt.legend()
    print("H1Max=" + str(h_p1_max) + ' PSI')
    print("D1Max = " + str(d1_max) + ' Inches')
    print("V1Max = " + str(V1_max) + ' ft/s')
    print("State 1 Power Required= " + str(Power1_max) + " Hp")
    print("Re1Max = " + str(Re1_max)+'\n\n')


    print("H2Max=" + str(h_p2_max) + ' PSI')
    print("D2Max = " + str(d2_max) + ' Inches')
    print("V2Max = " + str(V2_max) + ' ft/s')
    print("Re2Max = " + str(Re2_max))
    print("State 2 Power Required= " + str(Power2_max) + " Hp")

if plot_type =="DvRe":
    #plot pipe diameter vs reynolds number
    plt.title('Diameter vs Reynolds Number')
    plt.plot(d1i, Re1, 'r', label='6 ft^3/s', lw=1.5)
    plt.plot(d2i, Re2, 'k', label='8 ft^3/s', lw=1.5)
    #plot turbulent flow boundary
    plt.plot((6, 24), (2300, 2300), 'g', label='laminar flow boundary', lw=1.5)
    plt.plot((6, 24), (4000, 4000), 'b', label='turbulent flow boundary', lw=1.5)
    plt.legend()
    plt.xlabel('pipe diameter (in)')
    plt.ylabel('Reynolds number (Re)')
    plt.grid(True)
    plt.axis([6, 24, 0, 1500000])
    "plot max values"
    plt.plot(d1_max, Re1_max, 'kx', ms=8, mew=2 )
    plt.plot(d2_max, Re2_max, 'kx', ms=8, mew=2)
    print("D1Max = " + str(d1_max) + ' Inches')
    print("D2Max = " + str(d2_max)+ ' Inches')
    print("Re1Max = " + str(Re1_max))
    print("Re2Max = " + str(Re2_max))

if plot_type == "DvV":
    #plot pipe diameter vs average velocity of flow
    plt.title('Diameter vs Average Velocity')
    plt.plot(d1i, V1, 'r', label='6 ft^3/s', lw=1.5)
    plt.plot(d2i, V2, 'k', label= '8 ft^3/s', lw=1.5)
    plt.legend()
    plt.xlabel('pipe diameter (in)')
    plt.ylabel('Average Velocity (ft/s)')
    plt.grid(True)
    plt.axis([6, 24, 0, 45])
    plt.plot(d1_max, V1_max, 'kx', ms=8, mew=2 )
    plt.plot(d2_max, V2_max, 'kx', ms=8, mew=2 )
    print("D1Max = " + str(d1_max) + ' Inches')
    print("D2Max = " + str(d2_max)+ ' Inches')
    print("V1Max = " + str(V1_max) + ' ft/s')
    print("V2Max = " + str(V2_max) + ' ft/s')

if plot_type =="DvFf":
    #plots friction factor vs pipe diameter
    plt.title('Diameter vs Friction Factor')
    plt.plot(d1i, f1, 'r', label='6 ft^3/s', lw=1.5)
    plt.plot(d2i, f2, 'k', label= '8 ft^3/s', lw=1.5)
    plt.legend()
    plt.xlabel('pipe diameter (in)')
    plt.ylabel('Friction factor (f)')
    plt.grid(True)
    plt.plot(d1_max, f1_max, 'kx', ms=8, mew=2)
    plt.plot(d2_max, f2_max, 'kx', ms=8, mew=2)
    print("D1Max = " + str(d1_max) + ' Inches')
    print("D2Max = " + str(d2_max) + ' Inches')
    print("f1Max = " + str(f1_max))
    print("f2Max = " + str(f2_max))
    #plt.axis([0, 12, 0, 200])

if plot_type =="gate_valve":
    #plots gate valve data
    plt.title('Gate Valve Data - Diameter vs Resistance Coefficient')
    plt.plot(gvDraw, gvKraw, 'rx', ms=7, mew=2)
    plt.plot(gvD_points,gvKn, lw=1.5)
    plt.xlabel('pipe diameter (in)')
    plt.ylabel('Resistance coefficient (k)')
    plt.grid(True)
    plt.axis([0, 24, 0, 1])
    plt.plot(d1_max, k1_valve_max, 'gx', ms=7, mew=2, label= '6ft^3/s')
    plt.plot(d2_max, k2_valve_max, 'kx', ms=7, mew=2, label= '8ft^3/s')
    plt.legend()
    print("D1Max = " + str(d1_max) + ' Inches')
    print("D2Max = " + str(d2_max) + ' Inches')
    print("k1Max = " + str(k1_valve_max))
    print("k2Max = " + str(k2_valve_max))

if plot_type =="elbow_valve":
    plt.title('Elbow Fitting Data - Diameter vs Resistance Coefficient')
    plt.plot(eDraw, eKraw, 'rx', ms=7, mew=2,)
    plt.plot(eD_points, eKn, lw=2)
    plt.xlabel('pipe diameter (in)')
    plt.ylabel('Resistance coefficient (k)')
    plt.grid(True)
    plt.axis([0, 24, 0, 1])
    plt.plot(d1_max, k1_elbow_max, 'gx', ms=7, mew=2, label= '6ft^3/s')
    plt.plot(d2_max, k2_elbow_max, 'kx', ms=7, mew=2, label= '8ft^3/s')
    plt.legend()
    print("D1Max = " + str(d1_max) + ' Inches')
    print("D2Max = " + str(d2_max) + ' Inches')
    print("k1Max = " + str(k1_elbow_max))
    print("k2Max = " + str(k2_elbow_max))

if plot_type =="PWRvD":
    plt.title('Diameter vs Pump Power Required')
    plt.plot(d1i, Power1, 'r', lw=1.5, label='6 ft^3/s')
    plt.plot(d2i, Power2, 'k', lw=1.5,  label='8 ft^3/s')
    plt.grid(True)
    plt.legend()
    plt.plot(d1_max, Power1_max, 'kx', ms=7, mew=2)
    plt.plot(d2_max, Power2_max, 'kx', ms=7, mew=2)
    plt.xlabel('pipe diameter (in)')
    plt.ylabel('Required Power (Hp)')
    print("D1Max = " + str(d1_max) + ' Inches')
    print("D2Max = " + str(d2_max) + ' Inches')
    print("State 1 Power Required= " + str(Power1_max) + " Hp")
    print("State 2 Power Required= " + str(Power2_max) + " Hp")

if plot_type =="PWRvV":
    plt.title('Velocity vs Pump Power Required')
    plt.plot(V1, Power1, 'r', lw=1.5, label='6 ft^3/s')
    plt.plot(V2, Power2, 'k', lw=1.5,  label='8 ft^3/s')
    plt.grid(True)
    plt.legend()
    plt.plot(V1_max, Power1_max, 'kx', ms=7, mew=2)
    plt.plot(V2_max, Power2_max, 'kx', ms=7, mew=2)
    plt.xlabel('Average velocity (ft/s)')
    plt.ylabel('Required Pump Horsepower')
    print("V1Max = " + str(V1_max) + ' ft/s')
    print("V2Max = " + str(V2_max) + ' ft/s')
    print("State 1 Power Required= " + str(Power1_max) + " Hp")
    print("State 2 Power Required= " + str(Power2_max) + " Hp")

plt.show()
