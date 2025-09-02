from math import sqrt
from os import path
import re
from math import pi
from numpy import linspace

def max_Vifty( V_bounds,x,omega,a_sound,geom,aero ):
    '''
    Function that finds the maximum allowable freestream speed
    '''
    V_ifty = linspace( V_bounds[0],V_bounds[1],V_bounds[2] )


    Mach_calc( x, V, omega,a_sound, geom, aero )

    for iV,V in enumerate( V_ifty ):
        rests[iV].append( Mach_calc( x, V, omega,a_sound, geom, aero ) )
        if Mach_check(V):
            V_max = V
            break


def Mach_calc( x,V_ifty,omega,a_sound,geom,aero,wt = 0,wa = 0 ):
    '''
    Function that checks if a section of the propeller has a mach greater than critical mach number
    '''
    #stall_flg = False
    for rovR in x:
        k = 0, res[k].append( sqrt( V_ifty**2 + (omega*x*geom.R)**2 )/a_sound )    # Local Mac speed
        k = 1, res[k].append( aero.aero_params[ 'Mach_crit' ]  )                   # Section Critical Mach
        #if res[0][-1] > res[1][-1]:
        #    stall_flg = True

def find_crit_sec( x,Mvec,Mcrit ):
    stall_flg = False
    for iM,M in enumerate(Mvec):
        if M > Mcrit[iM]:
            return x[iM]

#   <------------------------- IMPORT/EXPORT ------------------------->   #

def read_input(file_path):
    iptpth = path.join(path.dirname(path.realpath(__file__)), f"\\input\\{file_path}") # It makes sure that the file is taken from the absolute path since the working path can be different
    with open(iptpth) as ipt:
        # Output Variables
        dts_s = []
        dts   = [[],[]]
        idxp  = []
        # Skips File Header
        next(ipt)
        #Reads Project Name
        line = ipt.readline()
        idx  = line.find('#')
        dts_s.append( line[ :idx ].rstrip('\t') ) 
        # Skips delimiter
        next(ipt)
        # Reads blade element input file 
        delim = 'GENERAL DATA\n'
        line = ipt.readline()
        idx  = line.find('#')
        while line != delim:
            dts_s.append( line[ :idx ].rstrip('\t') ) 
            line = ipt.readline()
            idx  = line.find('#')
        # Skips Delimiter
        #next(ipt)
        # Document delimeter
        docP  = 0                   # Documet part counter
        delim = "INTERVAL DATA\n"   # Delimeter keyword
        # Reads Numerical Data
        #try:
        for k,line in enumerate(ipt):
            idx = line.find('#')
            idx2 = line.find(',')
            if line != delim and docP == 0:
                # Reads the first part of input .txt file
                dts[docP].append( float(line[:idx]) )
            elif docP == 0:
                # Reads the document part delimiter
                docP += 1
            else:
                # Reads the document's second part
                lin_aux = line
                while idx2 > -1 and idx2 < idx:  # checks if there are other numbers to be read taht are not commented out (in that case idx2>idx)
                    dts[docP].append( float(lin_aux[:min(idx,idx2)]) )
                    lin_aux = lin_aux[idx2+1:]
                    idx2    = lin_aux.find(',')
                    idx     = lin_aux.find('#')
                dts[docP].append( float(lin_aux[:idx]) )
                dts[docP].append(-1)
        #except:
            #print('Could not read input file')
            #for i, val in enumerate(line.split('#')):
                #print(i)
                #print(val)
    return dts,dts_s