import Geometry 
import matplotlib.pyplot as plt
import numpy as np
import bemt
import aero

# Test case according to data from naca report No. 339 "FULL SCALE WIND TUNNEL TESTS WITH A SERIES OF PROPELLERS OF DIFFERENT DIAMETERS ON A SINGLE FUSELAGE"  
# by F. E. Weick (1931)  


# INPUT DATA
R = 1.60         #Blade radius (m)
R_hub = 0.152    #Hub radius (m)  
N = 2            #Number of blades
RPM = 1000       #revolutions per minute

# stations along the blade (r/R)
r_R_known = [ 0.0940,  0.1587,    0.1905,    0.2857,    0.3810,    0.4762,  0.5714,    0.6667,    0.7619,    0.8571,    0.9524,    1.0000]
# chord distribution   (c/R)
c_R_known = [ 0.0615, 0.1106,    0.1168,    0.1283 ,   0.1335,    0.1338,    0.1297,  0.1195,    0.1037,    0.0827,    0.0594,       0.02]
# pitch distribution measured from the chord (deg)
beta_known = [42.4,   42.4,      39.1,      35.1,      30.2,      26.7,      23.9,   21.75,     20.01,     18.8,      17.3,      16] 
sweep_known = [0 for b in beta_known]
beta75 = 15.5    #pitch angle imposed at 75% along the blade (deg)

# airfoils along the blade: NACA 4 and 5-digits or 'custom'
airfoil_known = ['0012','0012', '0012',  '0012', '0012','0012','0012', '0012','0012','0012','0012','0012']

pitch = 0.0      #measured from nominal pitch (deg)
v_J=np.linspace(0.152, 0.856, 80)     #range of J=V/nD
interp_kind = 'cubic'
dx = 0.0254     #new spacing between the stations used in numerical integration (m)
z = 0           #altitude (km)

CT_1 = []
CP_1 = []
ETA_1 = []

CT_2 = []
CP_2 = []
ETA_2 = []

CT_3 = []
CP_3 = []
temp = []
ETA_3 = []

xrot_params = {
    'alpha_0_lift': np.deg2rad(-3.1),
    'Cl_alpha': 6.28,
    'Cl_max': 1.5,
    'Cl_min':-0.5,
    'Cd': 0.01,
    'Ka': 0.87
}

for J in v_J:

    # Class iniziatization
    g = Geometry.Geometry( R, R_hub, N, RPM, r_R_known, c_R_known, beta_known,sweep_known, beta75, airfoil_known, pitch,interp_kind)

    # Defining aerodynamic method: method 1 
    # NOTE: as in aero version 1.1, sweep is implemented only in the aerodynamic method 1



    Aero = aero.Aerodynamics(1, True, True, xrot_params)

    #Computing C_T, C_P and eta and storing them in a vector
    ct_1, cp_1=bemt.BEMT_timp(z, J, dx, g, Aero)

    CT_1.append(ct_1)
    CP_1.append(cp_1)
    if ct_1 >= 0:
        ETA_1.append(J*ct_1/cp_1)
    else:
        ETA_1.append(np.nan)

    ct_2, cp_2=bemt.BEMT_tvorpd(z, J, dx, g, Aero)

    CT_2.append(ct_2)
    CP_2.append(cp_2)
    if ct_2 >= 0:
        ETA_2.append(J*ct_2/cp_2)
    else:
        ETA_2.append(np.nan)

    ct_3, cp_3 =bemt.BEMT_tvor(z, J, dx, g, Aero)

    CT_3.append(ct_3)
    CP_3.append(cp_3)
    if ct_3 >= 0:
        ETA_3.append(J*ct_3/cp_3)
    else:
        ETA_3.append(np.nan)


# Array conversion
Ct_1=np.array(CT_1)
Cp_1=np.array(CP_1)
Eta_1=np.array(ETA_1)

Ct_2=np.array(CT_2)
Cp_2=np.array(CP_2)
Eta_2=np.array(ETA_2)

Ct_3=np.array(CT_3)
Cp_3=np.array(CP_3)
Eta_3=np.array(ETA_3)


#Plot
'''
# Values obtained by Weick
J_Weick =[0.556 , 0.558 , 0.575 , 0.573 , 0.580 , 0.585 ,
0.596 , 0.591 , 0.650 , 0.645 , 0.6725 , 0.706 , 0.725 ,
0.762 , 0.790 , 0.825 , 0.849 , 0.525 , 0.526 , 0.510 ,
0.526 , 0.501 , 0.507 , 0.484 , 0.465 , 0.461 , 0.446 , 0.454 , 0.152 , 0.152]

Ct_Weick =[0.0397 , 0.0383 , 0.0369 , 0.0364 , 0.0358 ,
0.0358 , 0.0343 , 0.0336 , 0.0275 , 0.0274 , 0.0232 ,
0.0194 , 0.0151 , 0.0091 , 0.0051 , 0.0006 ,
-0.0002 ,
0.0427 , 0.0427 , 0.0437 , 0.0447 , 0.0470 , 0.0464 ,
0.0466 , 0.0511 , 0.0514 , 0.0521 , 0.0513 , 0.0850 ,
0.0841]

Cp_Weick =[0.0274 , 0.0270 , 0.0261 , 0.0260 , 0.0260 ,
0.0258 , 0.0252 , 0.0249 , 0.0223 , 0.0220 , 0.0203 ,
0.0183 , 0.0160 , 0.0126 , 0.0102 , 0.0066 , 0.0025 ,
0.0284 , 0.0286 , 0.0291 , 0.0296 , 0.0304 , 0.0300 ,
0.0299 ,
0.0317 , 0.0317 , 0.0314 , 0.0307 , 0.0347 ,
0.0344]

Eta_Weick =[0.806 , 0.791 , 0.811 , 0.804 , 0.800 , 0.806 ,
0.811 , 0.797 , 0.802 , 0.805 , 0.771 , 0.745 , 0.683 ,
0.555 ,0.398 , np.nan , np.nan , 0.790 , 0.796 , 0.766 ,
0.795 , 0.775 , 0.785 , 0.754 , 0.749 , 0.741 , 0.740 ,
0.750 , 0.372 , 0.372]
'''
plt.figure(figsize=(5, 6))
plt.plot(v_J, Ct_1, '--', label='Ct: timp', color='k')
plt.plot(v_J, Ct_2, '-.', label='Ct: tvorpd', color='k')
plt.plot(v_J, Ct_3, '-', label='Ct: tvor', color='k')
plt.plot(v_J, Cp_1, '--', label='Cp: timp', color='r')
plt.plot(v_J, Cp_2, '-.', label='Cp: tvorpd', color='r')
plt.plot(v_J, Cp_3, '-', label='Cp: tvor', color='r')
#plt.plot(J_Weick, Ct_Weick, 'o', markersize=5 , label='Ct: Weick', color='b')
#plt.plot(J_Weick, Cp_Weick, 'o', markersize=5, label='Cp: Weick', color='m')
plt.xlabel('J=V/nD')
plt.legend()
plt.grid(True)


plt.figure(figsize=(5,6))
plt.plot(v_J, Eta_1, '--', label='$\eta$: timp', color='k')
plt.plot(v_J, Eta_2, '-.', label='$\eta$: tvorpd', color='k')
plt.plot(v_J, Eta_3, '-', label='$\eta$: tvor', color='k')
#plt.plot(J_Weick, Eta_Weick, 'o', markersize=5, label='$\eta$: Weick', color='b')
plt.xlabel('J=V/nD')
plt.legend()
plt.grid(True)
plt.show()