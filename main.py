import Geometry 
import matplotlib.pyplot as plt
import numpy as np
import bemt
import aero
from sweep_functions import find_crit_sec
import aux_functs as af
# Test case according to data from naca report No. 339 "FULL SCALE WIND TUNNEL TESTS WITH A SERIES OF PROPELLERS OF DIFFERENT DIAMETERS ON A SINGLE FUSELAGE"  
# by F. E. Weick (1931)  


# INPUT DATA
R     = 1.52            # Blade radius (m)
R_hub = 0.291           # Hub radius (m)  
N     = 3               # Number of blades
RPM   = 1000            # revolutions per minute

# stations along the blade (r/R)
r_R_known  = [ 0.19,0.2,0.292857143,0.398214286,0.498214286,0.598214286,0.698214286,0.798214286,0.898214286,0.946428571,0.99 ]
# thickness distribution   (t/c)
t_c_known  = [ 0.160065253,0.160065253,0.19954323,0.25050571,0.295008157,0.31725938,0.302903752,0.264143556,0.203132137,0.160783034,0.117 ]
# chord distribution   (c/R)
c_R_known  = [ 0.345550265,0.345550265,0.220717781,0.110538336,0.065676998,0.047732463,0.039836868,0.036247961,0.034094617,0.033376835,0.0329 ]
# pitch distribution measured from the chord (deg)
beta_known = [ 58.87349081,58.87349081,52.22635514,45.74073153,40.27287413,35.7188407,31.84678,28.77653408,26.09130417,25.00543118,24.22 ]

# sweep distribution measured at c/4
sweep_known = []
sweep_known.append( [ 0,0,0,0,0,0,0,0,0,0,0 ] )
#sweep_known.append( [ 40,40,40,40,40,40,40,40,40,40,40,40 ] )
#pitch angle imposed at 75% along the blade (deg)
beta75 = 30   

# airfoils along the blade: NACA 4 and 5-digits or 'custom'
airfoil_known = [ 'custom','custom','custom', 'custom',  'custom', 'custom','custom','custom', 'custom','custom','custom' ]

pitch       = 0.0                                                                     # measured from nominal pitch (deg)
v_J         = np.linspace(0.152, 0.856, 80)                                           # range of J=V/nD
interp_kind = 'cubic'
dx          = 0.0254                                                                     # new spacing between the stations used in numerical integration (m)
z           = 0                                                                          # altitude (km)

CT_1  = []
CP_1  = []
ETA_1 = []

CT_2  = []
CP_2  = []
ETA_2 = []

CT_3  = []
CP_3  = []
ETA_3 = []

#g = Geometry.Geometry( R, R_hub, N, RPM, r_R_known, c_R_known, beta_known, sweep_known, beta75, airfoil_known, pitch,interp_kind )
xrot_params = {
    'alpha_0_lift': np.deg2rad(-3.3),
    'Cl_alpha': 6.28*0.815,
    'Cl_alpha_stall': 0.1,
    'Cl_max': 1.5,
    'Cl_min': -0.5,
    'Cl_incr_to_stall': 0.5,
    'Cd_min': 0.013, 
    'Cl_at_cd_min': 0.5,  
    'dCd_dCl2': 0.004,
    'Mach_crit': 0.8,
    'Re_scaling_exp': -0.4,
    'Cd' : 0.001
 }
Aero = aero.Aerodynamics( 2, True, True, xrot_params )

af.calc_sects( [ xrot_params['alpha_0_lift'], ( xrot_params['Cl_max']/xrot_params['Cl_alpha'] + xrot_params['alpha_0_lift'] )*10.5],Aero,5e6,0.001 )

res_J = []


for sweep in sweep_known:
    g = Geometry.Geometry( R, R_hub, N, RPM, r_R_known, c_R_known, beta_known, sweep, beta75, airfoil_known, pitch,interp_kind )

    for J in v_J:
        #Computing C_T, C_P and eta and storing them in a vector
        #ct_1, cp_1=bemt.BEMT_timp(z, J, dx, g, Aero, False, False, False)

        #CT_1.append(ct_1)
        #CP_1.append(cp_1)
        #if ct_1 >= 0:
        #    ETA_1.append(J*ct_1/cp_1)
        #else:
        #    ETA_1.append(np.nan)

        #ct_2, cp_2=bemt.BEMT_tvorpd(z, J, dx, g, Aero, True, False)

        #CT_2.append(ct_2)
        #CP_2.append(cp_2)
        #if ct_2 >= 0:
        #    ETA_2.append(J*ct_2/cp_2)
        #else:
        #    ETA_2.append(np.nan)

        ct_3, cp_3, sects = bemt.BEMT_tvor(z, J, dx, g, Aero, True, False)
        
        # --------------------------- Data Storage --------------------------- #
        res_J[0].append( J*RPM/60*g.R*2 )                           # V_infty
        res_J[1].append( find_crit_sec( x,sects[4],sects[5] ) )     # r/R critical
        res_J[2].append(ct_3)                                       # Ct
        res_J[3].append(cp_3)                                       # Cp
        res_J[6].append(sects)                                      # 

        #CT_3.append(ct_3)
        #CP_3.append(cp_3)
        if ct_3 >= 0:
            #ETA_3.append(J*ct_3/cp_3)
            res_J[4].append( J*ct_3/cp_3 )
        else:
            #ETA_3.append(np.nan)
            res_J[4].append( np.nan )
        res_J[5].append( J )
    rests[iS].append( res_J ) 
# --------------------------- Plots --------------------------- # 
# Array conversion
#Ct_1  = np.array(CT_1)
#Cp_1  = np.array(CP_1)
#Eta_1 = np.array(ETA_1)

#Ct_2=np.array(CT_2)
#Cp_2=np.array(CP_2)
#Eta_2=np.array(ETA_2)

#Ct_3=np.array(CT_3)
#Cp_3=np.array(CP_3)
#Eta_3=np.array(ETA_3)


'''
# #####################################################
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

#Plot

plt.figure(figsize=(5, 6))
#plt.plot(v_J, Ct_1, '--', label='Ct: timp', color='k')
#plt.plot(v_J, Ct_2, '-.', label='Ct: tvorpd', color='k')
plt.plot(v_J, , '-', label='Ct: tvor', color='k')
#plt.plot(v_J, Cp_1, '--', label='Cp: timp', color='r')
#plt.plot(v_J, Cp_2, '-.', label='Cp: tvorpd', color='r')
plt.plot(v_J, , '-', label='Cp: tvor', color='r')
#plt.plot(J_Weick, Ct_Weick, 'o', markersize=5 , label='Ct: Weick', color='b')
#plt.plot(J_Weick, Cp_Weick, 'o', markersize=5, label='Cp: Weick', color='m')
plt.xlabel('J=V/nD')
plt.legend()
plt.grid(True)


plt.figure(figsize=(5,6))
#plt.plot(v_J, Eta_1, '--', label='$\eta$: timp', color='k')
#plt.plot(v_J, Eta_2, '-.', label='$\eta$: tvorpd', color='k')
plt.plot(v_J, Eta_3, '-', label='$\eta$: tvor', color='k')
#plt.plot(J_Weick, Eta_Weick, 'o', markersize=5, label='$\eta$: Weick', color='b')
plt.xlabel('J=V/nD')
plt.legend()
plt.grid(True)
plt.show()
'''