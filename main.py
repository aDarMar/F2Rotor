import Geometry 
import matplotlib.pyplot as plt
import numpy as np
import bemt
import aero
from sweep_functions import find_crit_sec, sweep_sample
import aux_functs as af
from ambiance import Atmosphere 
from plot_funcs import plot_blade,plot_CT_CP
from opt_rout import find_P,find_P_n
# Test case according to data from naca report No. 339 "FULL SCALE WIND TUNNEL TESTS WITH A SERIES OF PROPELLERS OF DIFFERENT DIAMETERS ON A SINGLE FUSELAGE"  
# by F. E. Weick (1931)  


# INPUT DATA
R     = 2.10#1.9852                                        # Blade radius (m)
R_hub = 0.291*0+R*0.19                                       # Hub radius (m)  
N     = 4                                           # Number of blades
RPM   = 1012                                        # revolutions per minute
omega = RPM*2*np.pi/60

pitch       = 0.0                                   # measured from nominal pitch (deg)
v_J         = np.linspace(0.10,2.60,95)#0.8,1.4,75) ##0.75,1.25,75) #0.10,2.60,75) #0.152, 2.90, 50)          # range of J=V/nD
beta_sweep  = np.linspace(0,60,7)
# v_J         = np.linspace(2.40,2.60,2)
interp_kind = 'akima'
dx          = 0.0154                                # new spacing between the stations used in numerical integration (m)
z           = 0.                                     # altitude (km)
V_cruise    = 440/3.6                               # Design Cruise Speed [m/s]
a_sound     = Atmosphere(z*1000).speed_of_sound
rho         = Atmosphere(z*1000).density
# sweep distribution measured at c/4
sweep_known = []
#sweep_known.append( [ 0,0,0,0,0,0,0,0,0,0,0 ] )
#sweep_known.append( [ 40,40,40,40,40,40,40,40,40,40,40,40 ] )
#pitch angle imposed at 75% along the blade (deg)
#beta75 = 30  
# airfoils along the blade: NACA 4 and 5-digits or 'custom'


Mcr = 0.6 # Airfoil crtical Mach number


DEBUG = True
if DEBUG:
    # stations along the blade (r/R)
    # r_R_known = [ 0.0940,  0.1587,    0.1905,    0.2857,    0.3810,    0.4762,  0.5714,    0.6667,    0.7619,    0.8571,    0.9524,    1.0000]
    r_R_known = [0.094,0.144,0.194,0.244,0.294,0.344,0.394,0.444,0.494,0.544,0.594,0.619,0.644,0.669,0.694,0.719,0.744,0.769,0.794,0.819,0.829,0.839,0.849,0.859,0.869,0.879,0.889,0.899,0.909,0.919,0.929,0.939,0.949,0.959,0.969,0.979,0.989,0.999]
    # chord distribution   (c/R)
    #c_R_known = [ 0.0615, 0.1106,    0.1168,    0.1283 ,   0.1335,    0.1338,    0.1297,  0.1195,    0.1037,    0.0827,    0.0594,       0.02]
    c_R_known = [ 0.0615,0.104547335,0.117252959,0.123857898,0.128960435,0.132138718,0.133777338,0.134141257,0.133410954,0.13141466,0.127882575,0.125411148,0.122496046,0.119179841,0.115563108,0.11161142,0.107203603,0.10223066,0.096856067,0.09127661,0.089019242,0.086760873,0.084510581,0.082276206,0.080019604,0.077718584,0.075372418,0.072980375,0.070541723,0.068055733,0.065521674,0.062938814,0.060306425,0.056910319,0.050703895,0.042195533,0.032096672,0.02111875 ]
    # pitch distribution measured from the chord (deg)
    # beta_known = [42.4,   42.4,      39.1,      35.1,      30.2,      26.7,      23.9,   21.75,     20.01,     18.8,      17.3,      16] 
    beta_known = [ 42.4,43.10506517,38.93722607,36.89950224,34.68028526,32.00441773,29.65205146,27.76682377,26.13719001,24.6325548,23.34730729,22.76793505,22.22060225,21.70358004,21.20615757,20.73148673,20.29343542,19.90621594,19.57653946,19.27664897,19.15740799,19.03530792,18.90817021,18.77391665,18.63446124,18.49117961,18.3438369,18.19219824,18.03602879,17.87509369,17.70915807,17.53798708,17.36134586,17.16921111,16.93301582,16.65894784,16.35596985,16.03304457 ]
    #sweep = [0,   0,      0,      0,      0,      0,      0,   0,     0,     0,      0,      0]
    #sweep_known.append(sweep)

    airfoil_known = [ 'custom' for i in range( len(beta_known) )]

    # sweep distribution measured at c/4
    CHS  = [ 3,1,2,3 ]
    ipt1 = [ 0,R,R,40 ]
    ipt2 = [ 1,RPM*2*np.pi/60,RPM*2*np.pi/60,0.6 ]
    ipt3 = [ 0,z,z,0 ]
    ipt4 = [ 0,0,V_cruise,0 ]
    ipt5 = [ Mcr,Mcr,0.6,0 ]
    for iC,swp_tp in enumerate(CHS):
         sweep_known.append( sweep_sample( r_R_known,swp_tp,ipt1[iC],ipt5[iC],ipt2[iC],ipt3[iC],ipt4[iC] ) )
    
    # Pitch Angle
    beta75_plot = beta_sweep[4]
else:
    # stations along the blade (r/R)
    r_R_known  = [ 0.19,0.2,0.292857143,0.398214286,0.498214286,0.598214286,0.698214286,0.798214286,0.898214286,0.946428571,0.99 ]
    # thickness distribution   (t/c)
    t_c_known  = [ 0.160065253,0.160065253,0.19954323,0.25050571,0.295008157,0.31725938,0.302903752,0.264143556,0.203132137,0.160783034,0.117 ]
    # chord distribution   (c/R)
    c_R_known  = [ 0.345550265,0.345550265,0.220717781,0.110538336,0.065676998,0.047732463,0.039836868,0.036247961,0.034094617,0.033376835,0.0329 ]
    # pitch distribution measured from the chord (deg)
    beta_known = [ 58.87349081,58.87349081,52.22635514,45.74073153,40.27287413,35.7188407,31.84678,28.77653408,26.09130417,25.00543118,24.22 ]
    # beta75 = 28.0
    # sweep distribution measured at c/4
    CHS  = [ 3,1,2,3 ]
    ipt1 = [ 0,R,R,50 ]
    ipt2 = [ 1,RPM*2*np.pi/60,RPM*2*np.pi/60,R_hub/R ]
    ipt3 = [ 0,z,z,0 ]
    ipt4 = [ 0,0,V_cruise,0 ]
    for iC,swp_tp in enumerate(CHS):
         sweep_known.append( sweep_sample( r_R_known,swp_tp,ipt1[iC],Mcr,ipt2[iC],ipt3[iC],ipt4[iC] ) )
    
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
    'Mach_crit': Mcr,
    'Re_scaling_exp': -0.4,
    'Cd' : 0.01
 }
Aero = aero.Aerodynamics( 1, True, True, xrot_params )

#af.calc_sects( [ xrot_params['alpha_0_lift'], ( xrot_params['Cl_max']/xrot_params['Cl_alpha'] + xrot_params['alpha_0_lift'] )*1.2],Aero,1e6,0.65 )

beta_res = []
#grid_flg = [False,False,False,True]
# rests    = []
# Blades Plot
nsweep = len( sweep_known )
fig,ax_b = plt.subplots( nsweep,1,constrained_layout = True )

# --------------------------- Calculations --------------------------- # 
# 
res,res_status = [],[]
for iS,sweep in enumerate(sweep_known):
    g = Geometry.Geometry( R, R_hub, N, RPM, r_R_known, c_R_known, beta_known, sweep, 0, airfoil_known, pitch,interp_kind )
    temp0,temp = find_P_n( z,g,Aero,rho,omega,V_cruise,dx )
    res.append(temp)
    res_status.append(temp0)
plot_CT_CP(res,g.R,rho,V_cruise,14000)
for ibeta,beta75 in enumerate(beta_sweep):
    rests = []
    for iS,sweep in enumerate(sweep_known):
        g = Geometry.Geometry( R, R_hub, N, RPM, r_R_known, c_R_known, beta_known, sweep, beta75, airfoil_known, pitch,interp_kind )
        
        res_J = [ [],[],[],[],[],[],[],[] ] # V_ifty,r@Mcrit,Ct,Cp,eta,J,[sec],[sweep(deg)]
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
            try:
                ct_3, cp_3, sects, roR = bemt.BEMT_timp(z, J, dx, g, Aero, True, False)
            except:
                ct_3 = np.nan
                cp_3 = np.nan
                sects = np.full( (len(roR),12),np.nan )

            # --------------------------- Data Storage --------------------------- #
            res_J[0].append( J*RPM/60*g.R*2 )                             # V_infty
            res_J[1].append(-1) #res_J[1].append( find_crit_sec( x,sects[4],sects[5] ) )    # r/R critical
            res_J[2].append( ct_3 )                                       # Ct
            res_J[3].append( cp_3 )                                       # Cp
            res_J[6].append( sects )                                      # 

            #CT_3.append(ct_3)
            #CP_3.append(cp_3)
            if ct_3 >= 0:
                #ETA_3.append(J*ct_3/cp_3)
                res_J[4].append( J*ct_3/cp_3 )
            else:
                #ETA_3.append(np.nan)
                res_J[4].append( np.nan )
            res_J[5].append( J )
        res_J[7] = g.fs(roR) 
        rests.append( res_J )
        if ibeta == 0:
            grid_flg = True
            if iS == len(sweep_known) - 1:
                grid_flg = False
            plot_blade( g,ax_b[iS],grid_flg ) 
    beta_res.append(rests)
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
#af.beta_plots( res_beta,g,roR,RPM*2*np.pi/60,a_sound )
# Plot for Fixed Beta
ibeta = np.where(beta_sweep == beta75_plot)[0][0]#beta_sweep.index( beta75_plot )
af.plot_data( beta_res,g,roR,RPM*2*np.pi/60,a_sound,ibeta,beta75_plot,beta_sweep )
# af.prop_plot( rests[0] )
'''
# CASO 2
# Max Cp for straight blade
for iB,res_b in enumerate( beta_res ):
    temp = max( res_b[0][2] )
    if temp > max_cp:
        max_cp = temp
        idx  = res_b[0][2].index(max_cp)
        jmax = res_b[0][5][idx]
        ibetamax = iB
max_cp,jmax,ibetamax = find_max_cp( beta_res,0 )
Preq = max_cp*(2*R)**5*rho*(RPM/60)**3

beta_temp = []

while err > tol:
    for ibeta,beta75 in enumerate(beta_sweep):
        g = Geometry.Geometry( R, R_hub, N, RPM, r_R_known, c_R_known, beta_known, sweep_known[2], beta75, airfoil_known, pitch,interp_kind )
        res_J = [ [],[],[],[],[],[],[],[] ] # V_ifty,r@Mcrit,Ct,Cp,eta,J,[sec],[sweep(deg)]
        for J in v_J:
            try:
                ct_3, cp_3, sects, roR = bemt.BEMT_timp(z, J, dx, g, Aero, True, False)
            except:
                ct_3 = np.nan
                cp_3 = np.nan
                sects = np.full( (len(roR),12),np.nan )
            # --------------------------- Data Storage --------------------------- #
            res_J[0].append( J*RPM/60*g.R*2 )                             # V_infty
            res_J[1].append(-1) #res_J[1].append( find_crit_sec( x,sects[4],sects[5] ) )    # r/R critical
            res_J[2].append( ct_3 )                                       # Ct
            res_J[3].append( cp_3 )                                       # Cp
            res_J[6].append( sects )                                      # 
            if ct_3 >= 0:
                #ETA_3.append(J*ct_3/cp_3)
                res_J[4].append( J*ct_3/cp_3 )
            else:
                #ETA_3.append(np.nan)
                res_J[4].append( np.nan )
            res_J[5].append( J )
        res_J[7] = g.fs(roR) 
        rests.append( res_J )
        if ibeta == 3:
            plot_blade( g,ax_b[iS] ) 
    beta_temp.append(rests)
    max_cp_new = find_max_cp( beta_temp,0 )
    Pnew = max_cp*(2*R)**5*rho*(RPM/60)**3
    err = abs( 1-)


def find_max_cp( beta_res,iS ):
    for iB,res_b in enumerate( beta_res ):
    temp = max( res_b[iS][2] )
    if temp > max_cp:
        max_cp = temp
        idx  = res_b[iS][2].index(max_cp)
        jmax = res_b[iS][5][idx]
        ibetamax = iB
    return max_cp,jmax,ibetamax
'''
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