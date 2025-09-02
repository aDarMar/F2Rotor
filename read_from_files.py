from os import path
import re
from math import pi

def read_input(file_path):
    iptpth = path.join(path.dirname(path.realpath(__file__)), f"\\input\\{file_path}") # It makes sure that the file is taken from the absolute path since the working path can be different
    with open(iptpth) as ipt:
        # Output Variables
        dts_s = []
        dts = [[],[]]
        idxp = []
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
                    idx2 = lin_aux.find(',')
                    idx  = lin_aux.find('#')
                dts[docP].append( float(lin_aux[:idx]) )
                dts[docP].append(-1)
        #except:
            #print('Could not read input file')
            #for i, val in enumerate(line.split('#')):
                #print(i)
                #print(val)
    return dts,dts_s

def calc_prop(file_path,rot_flg = 0):
    input,input_s = read_input(file_path)
    inp_aux = [ [],[] ]
    k = 0
    for iVar in input[1]:
        if iVar == -1:
            k += 1
        else:
            inp_aux[k].append( iVar )
    PROP = prop( inp_aux[1],input[0][4]*2*pi/60, input[0][3], input[0][0]*2, input_s[0], input_s[1], input_s[2], input[0][7], input_s[3], input[0][2], inp_aux[0], input[0][1], rot_flg, input[0][6] )
# J_vec = J_DEF,            omega                h            D               name_proj   ipt_geom    ipt_drag    dr           interp_type D_hub        teta0_vec   N            rotflag  alpha

