from numpy import linspace,array
import matplotlib.pyplot as plt
from math import pi,acos
import plot_funcs
def polar_calc(alphas,Res,Ms):
    Re_v = linspace(Res[0],Res[1],nRe)
    M_v  = linspace(Ms[0],Ms[1],nM)


def calc_sects( alphas,aero,Re,M ):
    Re_ref  = 1e6
    nA,nM   = 300,50
    alpha_v = linspace(alphas[0],alphas[1],nA)
    Mach_v  = linspace(0,0.9,nM)
    Cl      = linspace(0,0,nA)
    Cd      = linspace(0,0,nA)
    Cd2     = linspace(0,0,nM)
    Mcrit   = linspace(0,0,nA)
    Mcrit2  = linspace(0,0,nM)
    for an,aoa in enumerate(alpha_v):
        Cl[an],Cd[an],Mcrit[an] = aero.clcd1( aoa, Re_ref, Re, M )
    ach = 8
    for nM,Mm in enumerate( Mach_v ):
        t,Cd2[nM],Mcrit2[nM]= aero.clcd1( ach, Re_ref, Re, Mm )

    fig,ax = plt.subplots( 1,2,constrained_layout = True )
    ax[0].plot(alpha_v*180/pi,Cl)
    plot_funcs.set_ax( ax[0],[ r"$\alpha$",r'C$_l$'] )
    
    ax[1].plot(Cl,Cd)
    ax[1].set( ylim = (0, 0.1) )
    plot_funcs.set_ax( ax[1],[ r"C$l$",r'C$_d$'] )
    fig.suptitle(f"{r'Profile Chacteristics'}\nM = {round(M,3)}{r' Re'} = {Re}", fontsize=30)

    fig,ax = plt.subplots( 1,1,constrained_layout = True )
    ax2 = ax.twinx()
    p1 = ax.plot(Mach_v,Cd2,label = r'C$_d$',color = 'k')
    p2 = ax2.plot(Mach_v,Mcrit2,label = r'M$_{cr}$')
    p3 = ax2.plot(Mach_v,Mach_v,label = r'M$_{\infty}$',linestyle = ':',color = p2[0].get_color() )
    plot_funcs.set_ax( ax,[ r"M",r'C$_d$'] )
    plot_funcs.set_ax( ax2,[ r"M",r'M$_{cr}$'] )
    ax.set( ylim = (0, 2.25) )
    ax2.tick_params(axis='y', colors=p2[0].get_color())
    ax2.yaxis.label.set_color(p2[0].get_color())
    ax2.set( ylim = (0.3, 0.525) )
    # plt.yticks(  linspace( 0.325,0.5,5 )    )
    fig.suptitle(f"{r'Drag vs Mach'}\n{r"$\alpha$"} = {round(ach,3)}", fontsize=30)
    ax.legend(handles=[p1[0], p2[0], p3[0]],fontsize = 25 )
    plot_fun(Cl,Cd,alpha_v*180/pi)


def plot_fun(Cl,Cd,alpha):
    fig,ax = plt.subplots(2,1)
    ax[0].plot(alpha,Cl)
    ax[1].plot(Cd,Cl)

    plt.show()

# PROPELLER FUNCTIONS

def prop_plot(res_J):
    '''
    This function plots CT,CP,eta vs J curves.

        Input:
        - res_J: list of lists containing all the data for a given sweep;
    '''
    fig,ax = plt.subplots(1,1)
    ax.plot(res_J[5],res_J[2])  # CT vs J
    ax.plot(res_J[5],res_J[3])  # CP vs J
    ax.plot(res_J[5],res_J[4])  # eta vs J
    fig2,ax2 = plt.subplots(3,1)
    prop_sect_plot( res_J,ax2 )
    plt.show()

def prop_sect_plot( res_J,ax ):
    '''
    This function plots CT,CP,eta vs J curves.dCT,dCP,omega*r,Cla,Mloc,Mcrit vs omega*r/V_ifty

        Input:
        - res_J : list of lists containing all the data for a given sweep;
        - ax    : axes object where section data are plotted
    '''
    
    for nJ,J in enumerate(res_J[5]):
        xi = res_J[6][nJ][2]/res_J[0][nJ]  # omega*r/V_ift
        if nJ == 0:
            ax[0].plot( xi,res_J[6][nJ][5],'r-' )           # M_crit vs xi    
        #ax.plot( xi,res_J[6][nJ][3],'x' )           # Cla vs xi
        # Plot 1: M/M_crit vs Xi
        ax[0].plot( xi,res_J[6][nJ][4],'o' )           # M_loc vs xi
        # Plot 2: dCt/dCp vs Xi
        ax[1].plot( xi,res_J[6][nJ][0],'-')     # dCt vs xi
        ax[1].plot( xi,res_J[6][nJ][1],'--')     # dCp vs xi
        # Plot 3: a,a' vs Xi
        ax[2].plot( xi,res_J[6][nJ][6],'-')     # a vs xi
        ax[2].plot( xi,res_J[6][nJ][7],'--')     # a' vs xi

def prop_geom_plot( res_J,geom,ax ):
    '''
    This function plots c,beta,sweep vs r/R

        Input:
        - xxx   : list of lists containing all the data for a given sweep;
        - xxx   : axes object where section data are plotted
    '''

def plot_data( res_beta,geom,roR,omega,a_sound,ibeta = 0,beta = 15,betas = [0,0] ):
    '''

    '''

    plot_funcs.beta_plots( res_beta,geom,roR,omega,a_sound,betas )

    plot_funcs.main_plot( res_beta[ibeta],geom,roR,omega,a_sound,beta )
    '''
    # Section Geometries: c/R and teta
    # We assume that only sweep changes
    fig, ax = plt.subplots(1,2,constrained_layout = True)    # Ax for c/R
    fig.subplots_adjust(right=0.75)
    twin1 = ax[0].twinx() # Ax for beta
    # Plot
    p1,   = ax[0].plot( roR, geom.fc(roR), "C0", label="c/R")
    p2,   = twin1.plot( roR, geom.fb(roR), "C1", label=r"$\theta$")
    # Set Limits
    ax[0].set( ylim = (0, 1),  ylabel= p1.get_label())
    ax[0].tick_params( axis='both', which='major', labelsize=15 )
    ax[0].set_xlabel(  xlabel="r/R",fontsize = 16 )
    ax[0].set_ylabel(  ylabel="c/R",fontsize = 16 )
    #twin1.set(  )
    twin1.tick_params( axis='both', which='major', labelsize=15 )
    twin1.set_ylabel(  ylabel = f"{p2.get_label()}[deg]",fontsize = 16 )
    # y-axis color
    ax[0].yaxis.label.set_color(p1.get_color())
    twin1.yaxis.label.set_color(p2.get_color())
    ax[0].tick_params(axis='y', colors=p1.get_color())
    twin1.tick_params(axis='y', colors=p2.get_color())
    # Grid
    ax[0].grid(True,'major')
    # Title
    ax[0].set_title('Section Geometry',fontsize = 20)
    # Legend
    ax[0].legend(handles=[p1, p2],fontsize = 16 )#, p3])
    ##########################################################################################
    psw = []
    # Define figures and axes
    # INPUT
    Jplot = [24,24] #[10,24,49] # indices of J to be plotted in r/R graphs
    # GRAPHICS
    colors = ['#E41A1C', '#377EB8', '#4DAF4A', '#FF7F00', '#984EA3',
          '#FFFF33', '#A65628', '#F781BF', '#00CED1', '#999999']
    lines = ['-','--','-.']
    # AXES SETUP
    # 1
    figs,axs = [],[]
    temp,temp2 = plt.subplots(1,1,constrained_layout = True)    # Ax for eta,Cp,Ct vs J
    figs.append( temp )
    axs.append( temp2 )
    temp = axs[0].twinx() # Double y-axis for eta
    axs.append(temp)
    p_coeffs,iAx = [ [],[],[] ],[0,0,1]
    labls = [ ["J","r/R",r"$\chi$"],[ r"$C_T$",r"$C_P$",r"\eta",r"M($ \bar{r} $)",r"M$_{crit}( \bar{r} )$",r"a",r"a^'" ] ] # x and y labels
    # 2
    temp,temp2 = plt.subplots(1,2,constrained_layout = True)    # Axes for M(r) vs Xi and dCT/dCP vs Xi
    figs.append( temp )
    axs.append( temp2 )
    # 3
    #temp,temp2 = plt.subplots(1,2,constrained_layout = True)    # Axes for dCT(r)/dCP(r) vs Xi and a/a' vs Xi
    #figs.append( temp )
    #axs.append( temp2 )
    p_sects = [ [ [],[] ] , [ [],[] ] ]
    
    for iS,res_swp in enumerate(results):
        # Cycle for sweep distribution
        psw.append( multi_plot( roR, res_swp[7], ax = ax[1],linecolor = colors[iS] ,lab = f"Sweep Dist.{str(iS+1)}",setax = 'no' ) ) #ax[1].plot( roR,res_swp[7],linecolor = colors[iS] ) ) # plot object containing sweep
        # CP/CT/Eta vs J
        for iP in range(3):
            p_coeffs[iP].append( multi_plot( res_swp[5],res_swp[2+iP],axs[iAx[iP]],lab = labls[1][iP] ,setax = 'no',linecolor = colors[iS],linst = lines[iP] ) ) # CT,CP,eta
        # Section Plots
        for Jsel in Jplot:
            Chi = res_swp[6][Jsel][2]/res_swp[0][Jsel]
            for iP in range(2):
                note = 0
                if iP == 0 and iS == 0:
                    note = f"{str( round(res_swp[5][Jsel],3) )}"
                #p_sects[0][iP].append( multi_plot( Chi,res_swp[6][Jsel][4+iP],ax = axs[2][0],setax = 'no',lab = labls[1][iP+3] ,linecolor = colors[iS],linst = lines[iP],note = note ) )# M(r),Mcrit vs Xi
                p_sects[0][iP].append( multi_plot( roR,res_swp[6][Jsel][4+iP],ax = axs[2][0],setax = 'no',lab = labls[1][iP+3] ,linecolor = colors[iS],linst = lines[iP],note = note ) )# M(r),Mcrit vs Xi

                if iS == 0:
                    note = f"{str( round(res_swp[5][Jsel],3) )}"
                p_sects[1][iP].append( multi_plot( roR,res_swp[6][Jsel][iP+6],ax = axs[2][1],setax = 'no',lab = labls[1][iP+5] ,linecolor = colors[iS],linst = lines[iP],note = note  ) )# a(r),a' vs Xi
    # Axis Setup
    label = [ f"{labls[1][0]}, {labls[1][1]}",labls[1][2],"M",f"{labls[1][3]}, {labls[1][4]}" ]
    tit = ["Coefficienti "]
    for iP in range(2):
            multi_plot( ax = axs[iAx[iP+1]],labls = [ labls[0][0], label[iP] ] ,setax = 'only',plots = p_coeffs )  # CT,CP,eta
            multi_plot( ax = axs[2][iP],labls = [ labls[0][2],label[2-iP] ],setax = 'only' ) # M(r),Mcrit vs Xi
            #multi_plot( ax = axs[2][1],labls = [ labls[0][2],label[4] ],setax = 'only' ) # a(r),a' vs Xi
    
    
    
    # CT/CP/eta Double axis
    #ax2 = axs[0].twiny()
    #ax2.axis["bottom"] = ax2.new_fixed_axis(loc="bottom", offset=(0, 60))
    #ax2.axis["bottom"].toggle(all=True)
    #p = ax2.plot( res_swp[7]*omega*geom.R/(pi*a_sound) )

    plt.show()

def multi_plot( x = 0, y = 0, ax = 0, labls = ['x','y'], setax = 'both', tit = 'Title', linst = '-', linecolor = 'b', lab = 'data', plots = 0, note = 0 ):
    if setax == 'only' or setax == 'both':
        ax.grid(True,'major') # set grid
        ax.tick_params( axis='both', which='major', labelsize=15 ) # grid thickness and font size
        if tit != 'Title':
            ax.set_title( tit,fontsize = 20 )   # set title
        ax.set_xlabel( xlabel=labls[0],fontsize = 16 )
        ax.set_ylabel( ylabel=labls[1],fontsize = 16 )
        #ax.legend( handles = plots,fontsize = 16 )
    if note != 0:
        xnote = ( 0.8*max(x) + 0.2*min(x) )
        ynote = ( 0.8*max(y) + 0.2*min(y) )
        ax.annotate( note,(xnote,ynote) )


    if setax == 'no' or setax =='both':
        p = ax.plot( x,y,color = linecolor,label = lab,linestyle = linst )
        return p
'''

'''
def YAPF():
    # Geometrical Data Plots
    # Section Geometries: c/R and teta
    # We assume that only sweep changes
    # 1.1
    # c/R and teta
    fig, ax_g = plt.subplots(1,2,constrained_layout = True)    # Ax for c/R
    fig.subplots_adjust(right=0.75)
    twin1 = ax_g[0].twinx() # Ax for beta
    # Plot
    p1,   = ax_g[0].plot( roR, geom.fc(roR), "C0", label="c/R")
    p2,   = twin1.plot( roR, geom.fb(roR), "C1", label=r"$\theta$")
    # Set Limits
    ax_g[0].set( ylim = (0, 1),  ylabel= p1.get_label())
    ax_g[0].tick_params( axis='both', which='major', labelsize=15 )
    ax_g[0].set_xlabel(  xlabel="r/R",fontsize = 16 )
    ax_g[0].set_ylabel(  ylabel="c/R",fontsize = 16 )

    twin1.tick_params( axis='both', which='major', labelsize=15 )
    twin1.set_ylabel(  ylabel = f"{p2.get_label()}[deg]",fontsize = 16 )
    # y-axis color
    ax_g[0].yaxis.label.set_color(p1.get_color())
    twin1.yaxis.label.set_color(p2.get_color())
    ax_g[0].tick_params(axis='y', colors=p1.get_color())
    twin1.tick_params(axis='y', colors=p2.get_color())
    # Grid
    ax_g[0].grid(True,'major')
    # Title
    ax_g[0].set_title('Section Geometry',fontsize = 20)
    # Legend
    ax_g[0].legend(handles=[p1, p2],fontsize = 16 )
    # 1.2
    # sweeps

    ##########################################################################################
    '''