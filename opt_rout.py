# Optimization

from scipy.optimize import minimize,Bounds
from bemt import BEMT_timp
from Geometry import Geometry
from math import pi
import numpy as np

Treq = 14000

def rosen_with_args(x, a, b):

    """The Rosenbrock function with additional arguments"""

    return sum(a*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0) + b

def find_P(z,g,Aero,rho,omega,dx):
    x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])
    #res = minimize(rosen_with_args, x0, method='nelder-mead',
    #           args=(0.5, 1.), options={'xatol': 1e-8, 'disp': True})
    def sect_calc(J,beta75):
        g.update_cal(beta75)
        #V_ifty = J*omega*g.R*pi
        #g = Geometry( R, R_hub, N, RPM, r_R_known, c_R_known, beta_known, sweep, beta75, airfoil_known, pitch,interp_kind )
        ct, cp, sects, roR = BEMT_timp( z, J, dx, g, Aero, True, False)
        return ct,cp,sects,roR
    def obj_fun(x):
        J,beta75 = x[0],x[1]
        ct,temp,temp,temp = sect_calc(J,beta75)
        T = (omega*g.R/pi)**2*rho*(2*g.R)**2*ct
        return abs( 1-T/Treq )
    
    # Bounds
    bounds = Bounds([0, 1.5], [10, 40])
    met = "Nelder-Mead"
    x0  = np.array([1.0,30])
    res = minimize( obj_fun,x0,method = met,bounds = bounds, options={'xatol': 1e-8, 'disp': True} )
    res_out = res['final_simplex'][0][0]
    ct, cp, sects, roR = sect_calc( res_out[0],res_out[1] ) 
    res_out = [ res_out[0],res_out[1],ct,cp,sects ]
    return res,res_out

def find_P_n(z,g,Aero,rho,omega,Vifty,dx):
    ''' Find Treq for fixed Vifty '''
    x0 = np.array([1.3, 0.7, 0.8, 1.9, 1.2])
    #res = minimize(rosen_with_args, x0, method='nelder-mead',
    #           args=(0.5, 1.), options={'xatol': 1e-8, 'disp': True})
    def sect_calc(J,beta75):
        g.update_cal(beta75)
        g.RPM = Vifty*np.pi/(J*g.R)*30/pi
        #V_ifty = J*omega*g.R*pi
        #g = Geometry( R, R_hub, N, RPM, r_R_known, c_R_known, beta_known, sweep, beta75, airfoil_known, pitch,interp_kind )
        ct, cp, sects, roR = BEMT_timp(z, J, dx, g, Aero, True, False)
        return ct,cp,sects,roR
    def obj_fun(x):
        J,beta75 = x[0],x[1]
        ct,temp,temp,temp = sect_calc(J,beta75)
        omg = g.RPM*pi/30#Vifty*np.pi/(J*g.R)
        T   = (omg*g.R/pi)**2*rho*(2*g.R)**2*ct
        return abs( 1-T/Treq )
    
    # Bounds
    bounds = Bounds([0, 1.1], [10, 40])
    met = "Nelder-Mead"
    x0  = np.array( [Vifty/(g.R*omega)*np.pi,30] )
    res = minimize( obj_fun,x0,method = met,bounds = bounds, options={'xatol': 1e-8, 'disp': True} )
    res_out = res['final_simplex'][0][0]
    ct, cp, sects, roR = sect_calc( res_out[0],res_out[1] ) 
    res_out = [ res_out[0],res_out[1],Vifty*np.pi/(res_out[0]*g.R),ct,cp,sects ]
    return res,res_out