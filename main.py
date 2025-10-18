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

# INPUT DATA
R     = 1.976#1.9852                                        # Blade radius (m)
R_hub = 0.291*0+R*0.19                                       # Hub radius (m)  
N     = 4                                           # Number of blades
RPM   = 1212                                        # revolutions per minute
omega = RPM*2*np.pi/60

pitch       = 0.0                                   # measured from nominal pitch (deg)
v_J         = np.linspace(0.10,2.60,95)#0.8,1.4,75) ##0.75,1.25,75) #0.10,2.60,75) #0.152, 2.90, 50)          # range of J=V/nD
beta_sweep  = np.linspace(0,60,7)
# v_J         = np.linspace(2.40,2.60,2)
interp_kind = 'akima'
dx          = 0.0154                                # new spacing between the stations used in numerical integration (m)
z           = 6.5                                     # altitude (km)
V_cruise    = 440/3.6                               # Design Cruise Speed [m/s]
a_sound     = Atmosphere(z*1000).speed_of_sound
rho         = Atmosphere(z*1000).density

# GEOMETRY
r_R_known  = [ 0.117967332,0.162068966,0.196370236,0.224137931,0.299274047,0.398911071,0.501814882,0.601451906,0.701088929,0.802359347,0.903629764,0.95753176,0.999 ]    # stations along the blade (r/R)
t_c_known  = [  ]   # thickness distribution   (t/c)   
c_R_known  = [ 0.06313933,0.100176367,0.11957672,0.132627866,0.150617284,0.159435626,0.161904762,0.159082892,0.154144621,0.14638448,0.131216931,0.114285714,0.097852667 ]    # chord distribution   (c/R)  
beta_known = [ 52.24204489,49.32742423,47.06049705,45.22536553,40.47175086,34.74795595,29.57228842,25.23636476,21.71415465,18.29862236,15.39211506,13.78026732,12.52187264 ]       # pitch distribution measured from the chord (deg)   
sweep_known = [0 for i in r_R_known]        # sweep at sections
airfoil_known = [ 'custom' for i in r_R_known]  
# PROFILE DATA
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
    'Mach_crit': 0.6,
    'Re_scaling_exp': -0.4,
    'Cd' : 0.01
 }
Aero = aero.Aerodynamics( 1, True, True, xrot_params )

#af.calc_sects( [ xrot_params['alpha_0_lift'], ( xrot_params['Cl_max']/xrot_params['Cl_alpha'] + xrot_params['alpha_0_lift'] )*1.2],Aero,1e6,0.65 )

beta_res = []
# Blades Plot
nsweep = len( sweep_known )
fig,ax_b = plt.subplots( nsweep,1,constrained_layout = True )

# --------------------------- Calculations --------------------------- # 
# 
'''
res,res_status = [],[]

g = Geometry.Geometry( R, R_hub, N, RPM, r_R_known, c_R_known, beta_known, sweep_known, 0, airfoil_known, pitch,interp_kind )
temp0,temp = find_P_n( z,g,Aero,rho,omega,V_cruise,dx )
res.append(temp)
res_status.append(temp0)
plot_CT_CP(res,g.R,rho,V_cruise,14000)
'''
for ibeta,beta75 in enumerate(beta_sweep):
    rests = []
    g = Geometry.Geometry( R, R_hub, N, RPM, r_R_known, c_R_known, beta_known, sweep_known, beta75, airfoil_known, pitch,interp_kind )
    
    res_J = [ [],[],[],[],[],[],[] ] # V_ifty,r@Mcrit,Ct,Cp,eta,J,[sec],[sweep(deg)]
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
        #try:
        ct_3, cp_3, sects, roR = bemt.BEMT_timp(z, J, dx, g, Aero, True, True)
        #except:
        #    ct_3 = np.nan
        #    cp_3 = np.nan
        #    sects = np.full( (len(roR),12),np.nan )

        # --------------------------- Data Storage --------------------------- #
        res_J[0].append(beta75)
        res_J[1].append(J)
        res_J[2].append(J*RPM/60*g.R*2)                             # V_infty
        res_J[3].append( ct_3 )                                       # Ct
        res_J[4].append( cp_3 )                                       # Cp
        res_J[6].append( sects )                                      # 

        #CT_3.append(ct_3)
        #CP_3.append(cp_3)
        if ct_3 >= 0:
            #ETA_3.append(J*ct_3/cp_3)
            res_J[5].append( J*ct_3/cp_3 )
        else:
            #ETA_3.append(np.nan)
            res_J[5].append( np.nan )
        rests.append( res_J )

    beta_res.append(rests)
    a = 1
def write_list_to_txt(file_name, data):
    HDR = ["Theta","J","CT","CP","Eta"]
    with open(file_name, mode='w', encoding='utf-8') as file:
        for item in data:
            file.write(f"{item}\n")  # Scrive ogni valore su una nuova riga