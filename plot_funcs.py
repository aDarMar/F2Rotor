import matplotlib.pyplot as plt
from math import pi,tan,cos
from numpy import linspace,isnan
lin_pl = 2
leg_font = 25
tit_font = 32
CT_p = 0.35
COLORS = ['#E41A1C', '#377EB8', '#4DAF4A', '#FF7F00', '#984EA3',
          '#FFFF33', '#A65628', '#F781BF', '#00CED1', '#999999']

'''
class PlotContainer:
    
    def __init__(self):
        self.fig   = []
        self.ax    = []
        self.name  = []
        self.lines = []

    def add_plot(self,label,nrows = 1,ncols = 1):
        t_fig, ax_t = plt.subplots( nrows,ncols,constrained_layout = True )
        self.fig.append( t_fig )
        self.ax.append( ax_t )
        self.name.append( label )
        self.lines.append( [] )

    # Plots for FIGURE 1
    def geom_plot( self, geom_obj, roR,col ):
        line_G = []
        temp = self.ax[0].twinx()
        self.ax[0].append( temp )
        temp = self.ax[0].twiny()
        self.ax[0].append( temp )

        line_G.append( ax[0][0].plot( roR,geom_obj.fb( roR ) ) )
        line_G.append( ax[0][1].plot( roR,geom_obj.fc( roR ) ) )

        line_G.append( ax[0][1].plot( [0,1],[0,1] ) )

        self.lines[0].append( line_G )

    # Plots for FIGURE 2
    def ct_cp_etaplot( Jvec,res ):
        temp = self.ax[1].twinx()
        for i in range(2):
            line_G.append( ax[1][0].plot( Jvec,res[2+i] ) )
        line_G.append( ax[1][1].plot( Jvec,res[4] ) )

    # Plots for FIGURE 3 and 4
    def sec_plots( self,roR,res_sweep ):
        line_G = []
        line_G.append( ax[2][0].plot( roR,res_sweep ) )


    def single_plot( self,x,y,tag,col,ax_ch = 0 ):
        try:
            iP = self.index( tag )
        except:
            print("Error: Could not find the selected ax/fig")
            return
        if ax_ch > len( self.ax[iP] ):
            print("Too few axes")
            return
        else:
            self.lines[iP].append( base_plot( x,y,self.ax[iP][ax_ch],col ) )

    def base_plot( self,x,y,ax,col ):
        lin = ax.plot( x,y )
        return lin

def plot_res( results, geom_obj, roR, omega, a_sound ):
    ''' '''
    # Definition of Aliases for Readability
    Jvec = results[0][0]
    # Definition of Axes and Figures
    pts = PlotContainer()
    # Figure 1 
    # # - 1.1 beta,c/R vs r/R
    # # - 1.2 sweep vs r/R
    # Figure 2 
    # # - 2.1 Cl,Cd vs r/R @ J,Sweep
    # # - 2.2 dCT,dCp vs r/R
    # Figure 3
    # # - 3.1 M,Mcr vs r/R
    # # - 3.2 alpha,alpha_i,beta,psi vs r/R

    nrows = [ 1,1,1,1 ]
    ncols = [ 2,1,2,2 ]
    tags  = [ "Geometry", "Coeff_J", "Sec_Coeff", "Sec_Mach" ]
    # Initialization of Axes and Figures
    for i in range( len(nrows) ):
        pts.add_plot( tags[i],nrows[i],ncols[i] )
    # Plots
    pts.geom_plot(  geom_obj, roR, col )
    
    for iS,res_sweep in results:
        pts.single_plot( roR,res_sweep[7],"Geometry" )
        pts.ct_cp_etaplot( Jvec,res_sweep )

        for  iJ,J in enumerate( Jvec ):
            #pts.single_plot( Jvec, )
            pts.sec_plots( roR,res_sweep,iJ,J )
'''

# Plot for Multiple Betas
def beta_plots( res_beta,geom_obj,roR,omega,a_sound,betas ):
    figure_0( res_beta,omega,geom_obj,a_sound,betas  )
    figure_1( roR,res_beta[2],geom_obj ) #Results with beta075 = 0

def figure_0( res_beta,omega,geom_obj,a_sound,betas ):
    ''' eta vs beta vs sweep'''
    ymax,xmax,iFl = 0,0,True
    fig,ax = plt.subplots( 1,1,constrained_layout = True )
    ps,xmax,ymax = [],0,0
    au_ax = ax.twiny()
    for iB,sin_beta in enumerate(res_beta):
        xmax,ymax = 0,0
        for iS, res_sweep in enumerate(sin_beta):
            col = COLORS[iS]
            tempo = ax.plot( res_sweep[5],res_sweep[4],color = col,linestyle = '-',linewidth = lin_pl*0.85,label = f"{r'$\Lambda_'}{str(iS+1)}$" )
            if iFl:
                ps.append( tempo[0] )

            tempi = max( res_sweep[4] )
            if tempi > ymax:
                ymax = tempi
                xmax = res_sweep[4].index(ymax)
                xmax = res_sweep[5][xmax]
        iFl = False

        ax.annotate( str( round(betas[iB],1) ), xy=(xmax, ymax*1.01) )
    #ax.set_xlabel( xlabel=pp[0].get_label(),fontsize = 16 )
    #ax.tick_params( axis='both', which='major', labelsize=15 ) 
    set_ax( ax,["J",r"$\eta$"] )
    pp = au_ax.plot( [ JJ*omega*geom_obj.R/(pi*a_sound) for JJ in res_sweep[5] ],[0 for JJ in res_sweep[5]],alpha = 0,linestyle = '-',linewidth = lin_pl,label = r'M$_{\infty}$' )
    au_ax.spines.bottom.set_position(("axes", 1.2))
    ax.legend(handles=ps,fontsize = 16 )
    au_ax.set_xlabel( xlabel=pp[0].get_label(),fontsize = 16 )
    au_ax.tick_params( axis='both', which='major', labelsize=15 ) 

def figure_1( roR,results,geom_obj ):
    ''' teta, c/R vs r/R and sweep vs r/R'''
    ps = []
    fix,ax = plt.subplots( 1,2,constrained_layout = True )
    au_ax = ax[0].twinx()
    p1 = ax[0].plot( roR,geom_obj.fc(roR),color = 'k',linestyle = '-',linewidth = lin_pl,label = r'c/R' )
    p2 = au_ax.plot( roR,[geom_obj.fb(rr) - 20 for rr in roR],color = 'b',linestyle = '-',linewidth = lin_pl,label = r'$\theta$' )
    for iS, res_sweep in enumerate(results):
        col = COLORS[iS]
        tempo = ax[1].plot( roR,res_sweep[7],color = col,linestyle = '-',linewidth = lin_pl,label = f"{r'$\Lambda_'}{str(iS+1)}$" ) 
        ps.append( tempo[0] )
    set_ax( ax[0],["r/R",r"c/R"] )
    set_ax( au_ax,["r/R",r"$\theta$ [deg]"] )
    set_ax( ax[1],["r/R",r"$\Lambda$ [deg]"] )
    # Set Limits
    ax[0].set( ylim = (0, 0.40) )
    au_ax.set( ylim = (25, 65) )
    au_ax.tick_params(axis='y', colors=p2[0].get_color())
    au_ax.yaxis.label.set_color(p2[0].get_color())
    # Legend
    ax[0].legend(handles=[p1[0], p2[0]],fontsize = 16 )
    ax[1].legend(handles=ps,fontsize = 16 )

# Plot for Fixed Beta
def main_plot( results, geom_obj, roR, omega, a_sound,teta = 15 ):
    
    figure_2( roR,results,geom_obj,omega,a_sound,teta )
    Jsel = [20,20]#[55,55] #[35,35]
    # Plots at fixed CT,Beta
    find_CT( results,roR,teta )
    # Plots at fixed J,beta
    iS = range( len(results) )
    sect_plot( roR,results,Jsel,iS,teta )



    #Cl_Cd_dCT_dCP_vs_r( roR,results,Jsel,teta )
    #Mcr_Meff_vs_r( roR,results,Jsel,teta )
    #find_CT( results )
    plt.show()





def figure_2( roR,results,geom_obj,omega,a_sound,teta = 15 ):
    ''' CT,CP,eta vs J'''
    fig,ax = plt.subplots( 1,1,constrained_layout = True )
    au_ax  = ax.twinx()
    au_ax2 = ax.twiny()

    nan_i = []


    for iS, res_sweep in enumerate(results):
        col = COLORS[iS]
        ax.plot( res_sweep[5],res_sweep[2],color = col,linestyle = '-',linewidth = lin_pl,label = r'C$_T$' )
        ax.plot( res_sweep[5],res_sweep[3],color = col,linestyle = '--',linewidth = lin_pl,label = r'C$_P$' )
        au_ax.plot( res_sweep[5],res_sweep[4],color = col,linestyle = '-.',linewidth = lin_pl,label = r'$\eta$' )

        for ieta,eta in enumerate( res_sweep[4] ):
            if isnan(eta):
                nan_i.append( res_sweep[5][ieta] )
                #nan_idx.append( ieta )
                break
    if len( nan_i )>0:
        Jlim = max( nan_i )
        nlim = res_sweep[5].index( Jlim )
    else:
        Jlim = max( res_sweep[4] )
        nlim = len( res_sweep[4] )-1
    # Double x-axis with Mach
    Mach = [ res_sweep[5][i]*omega*geom_obj.R/(pi*a_sound) for i in range( nlim+1 ) ]
    pp = au_ax2.plot( Mach,[0 for JJ in range( nlim+1 )],alpha = 0,linestyle = '-',linewidth = lin_pl,label = r'M$_{\infty}$' )
    au_ax2.spines.bottom.set_position(("axes", 1.2))
    # Labels
    au_ax2.set_xlabel( xlabel=pp[0].get_label(),fontsize = 16 )
    au_ax2.tick_params( axis='both', which='major', labelsize=15 ) 
    fig.suptitle(f"{r'Propeller Coefficients'}\n{r'$\theta_{75}$'} = {teta}", fontsize=16)
    set_ax( ax,["J",r"C$_T$, C$_P$"] )
    set_ax( au_ax,["J",r"$\eta$"] )
    au_ax.grid(False)
    # Set Limits
    
    ax.set( xlim = (results[0][5][0],Jlim), ylim = (0, 0.35) )
    #au_ax.set( xlim = (Mach[0],Mach[-1]), ylim = (0, 0.9) )
    #au_ax.tick_params(axis='y', colors=p2[0].get_color())
    #au_ax.yaxis.label.set_color(p2[0].get_color())

def Cl_Cd_dCT_dCP_vs_r( roR,res_sweep,Jsel,iS = 0,teta = 15,ax = 0,au_ax = 0,CT = 'a' ):
    ''' Cl,Cd vs r/R and dCT, dCP vs r/R 
        - res_sweep : result vector for given sweep
        - Jsel  : indices of chosen J
        - iS    : sweep index (for color codes)
        - teta  : reference teta075 (for labels)
    '''
    axCH = False
    if isinstance(ax,int):
        fig,ax = plt.subplots( 1,2,constrained_layout = True )
        au_ax = ax[0].twinx()
        axCH = True
    #for iS, res_sweep in enumerate(results):
    col = COLORS[iS]
    if isinstance( Jsel,list ) == False:
        Jsel = [Jsel,Jsel]
    for iJ in Jsel:
        J = res_sweep[5][iJ] # J

        temp0 = ax[0].plot( roR,res_sweep[6][iJ][6],color = col,linestyle = '-',linewidth = lin_pl,label = r'C$_l$' )
        temp1 = au_ax.plot( roR,res_sweep[6][iJ][7],color = col, linestyle = '-.',linewidth =lin_pl,label = r'C$_d$' )

        temp2 = ax[1].plot( roR,res_sweep[6][iJ][0], color = col,linestyle = '-',linewidth = lin_pl, label = r'dC$_T$' )
        temp3 = ax[1].plot( roR,res_sweep[6][iJ][1], color = col,linestyle = '-.',linewidth = lin_pl, label = r'dC$_P$' )

    ax[0].legend(handles=[temp0[0], temp1[0]], fontsize = leg_font )
    ax[1].legend(handles=[temp2[0], temp3[0]], fontsize = leg_font )
    lines = [ temp0[0],temp0[0],temp0[0],temp0[0] ]
    if axCH: #isinstance( ax,float ) or isinstance( ax,int ) :
        tit = f"{r'Sections Coefficients'}\nJ = {round(J,3)},{r' $\theta_{75}$'} = {teta}"
        if CT != 'a':
            tit = f"{tit}, {r"C$_T$"} = {round(res_sweep[2][iJ],3)}"
        fig.suptitle( tit, fontsize=tit_font)
        set_ax( ax[0],[ r"r/R",r'C$_l$'] )
        set_ax( au_ax,[ r"r/R",r'C$_d$'] )
        set_ax( ax[1],[ r"r/R",r'dC$_T$, dC$_P$'] )
    return ax,au_ax, lines

def set_ax( ax,labls = 'no',tit = 'Title' ):
    ax.grid(True,'major') # set grid
    ax.tick_params( axis='both', which='major', labelsize=15 ) # grid thickness and font size
    if tit != 'Title':
        ax.set_title( tit,fontsize = 20 )   # set title
    ax.tick_params(axis='x', labelsize=25)  # Cambia la dimensione dei numeri sull'asse x
    ax.tick_params(axis='y', labelsize=25)
    if labls != 'no':
        ax.set_xlabel( xlabel=labls[0],fontsize = 25 )
        ax.set_ylabel( ylabel=labls[1],fontsize = 25 )

def Mcr_Meff_vs_r( roR,res_sweep,Jsel,iS = 0,teta = 15,ax = 0,CT = 'a' ):
    ''' M, Mcr vs r/R
        - Jsel  : indices of chosen J
        - iS    : sweep index (for color codes)
        - teta  : reference teta075 (for labels)
    '''
    axCH = False
    if ax == 0:
        fig,ax = plt.subplots( 1,1,constrained_layout = True )
        #au_ax = ax.twinx()
        axCH = True
    #for iS, res_sweep in enumerate(results):
    col = COLORS[iS]
    if isinstance( Jsel,list ) == False:
        Jsel = [Jsel,Jsel]
    for iJ in Jsel:
        J = res_sweep[5][iJ] # J

        temp0 = ax.plot( roR,res_sweep[6][iJ][4],color = col,linestyle = '-',linewidth = lin_pl,label = r'M$_{eff}$' )
        temp1 = ax.plot( roR,res_sweep[6][iJ][5],color = col,linestyle = '--',linewidth = lin_pl,label = r'M$_{crit}$' )

    lines = [ temp0[0],temp0[0] ]
    if axCH:
        tit = f"{r'Sections Mach Number'}\nJ = {round(J,3)},{r' $\theta_{75}$'} = {teta}"
        if CT != 'a':
            tit = f"{tit}, {r"C$_T$"} = {round(res_sweep[2][iJ],3)}"
        set_ax( ax,[ r"r/R",r"M$_{eff}$, M$_{crit}$" ] )
        fig.suptitle(tit, fontsize=tit_font)
        ax.legend(handles=[temp0[0], temp1[0]],fontsize = leg_font )
    return ax, lines




    #if isinstance( Jsel,list ) == False:
    #    Jsel = [Jsel,Jsel]

    #fig,ax = plt.subplots( 1,1,constrained_layout = True )

    #for iS, res_sweep in enumerate(results):
    #col = COLORS[iS]
    #for iJ in Jsel:
    #    J = res_sweep[5][iJ] # J
        #temp0 = ax[0].plot( roR,res_sweep[6][iJ][8],color = col,linestyle = '-',linewidth = lin_pl,label = r'$\alpha_i$' )
        #temp1 = ax[0].plot( roR,res_sweep[6][iJ][9],color = col,linestyle = '--',linewidth = lin_pl,label = r'$\alpha$' )
        #temp2 = ax[0].plot( roR,res_sweep[6][iJ][10],color = col,linestyle = '-.',linewidth = lin_pl,label = r'$\theta$' )
        #temp3 = ax[0].plot( roR,res_sweep[6][iJ][11],color = col,linestyle = ':',linewidth = lin_pl,label = r'$\phi$' )

    #    temp0 = ax.plot( roR,res_sweep[6][iJ][4],color = col,linestyle = '-',linewidth = lin_pl,label = r'M$_{eff}$' )
     #   temp1 = ax.plot( roR,res_sweep[6][iJ][5],color = col,linestyle = '--',linewidth = lin_pl,label = r'M$_{crit}$' )

    #set_ax( ax[0],[ r"r/R",r"Angles [deg]" ] )
    #set_ax( ax,[ r"r/R",r"M$_{eff}$, M$_{crit}$" ] )
    #fig.suptitle(f"{r'Sections Coefficients'}\nJ = {round(J,3)}{r'$\theta_{75}$'} = {teta}", fontsize=tit_font)
    #ax.legend(handles=[temp0[0], temp1[0]],fontsize = leg_font )
    #ax.legend(handles=[temp0[0], temp1[0], temp2[0], temp3[0]],fontsize = 16 )

def plot_blade( geom_obj,ax ):
    xx = linspace( geom_obj.r_hub,geom_obj.R,100 ) #/geom_obj.R,1,100 )

    sweeps = geom_obj.fs( xx/geom_obj.R )
    coR    = geom_obj.fc( xx/geom_obj.R )
    coR    = [ cR*geom_obj.R for cR in coR ] # [ cR/max(coR) for cR in coR ] scale c with respect to the maximum value
    beta   = geom_obj.fb( xx/geom_obj.R )
    ingr   = [-tan(sweep*pi/180) for sweep in sweeps] # Integrand function
    mn_ln  = [ 0 for x in xx ]
    lead   = [ 0 for x in xx ]
    trail  = [ 0 for x in xx ]
    # Trapezoidal Integration for Mean Line
    for ix in range( len(xx)-1 ) :
        df          = 0.5*( ingr[ix+1] + ingr[ix] )*( xx[ix+1] - xx[ix] )
        # Mean Line
        mn_ln[ix+1] = mn_ln[ix] + df
        # Leading Edge
        lead[ix+1] =  mn_ln[ix+1] + coR[ix+1]*cos( beta[ix+1]*pi/180 )*0.25
        # Trailing Edge
        trail[ix+1] =  mn_ln[ix+1] - coR[ix+1]*cos( beta[ix+1]*pi/180 )*0.75
    
    ax.plot( xx,mn_ln,color = 'k',linestyle = '--',linewidth = lin_pl,label = r'Quarter-chord line' )
    ax.plot( xx,lead,color = 'k',linestyle = '-',linewidth = lin_pl,label = r'Leading-edge line' )
    ax.plot( xx,trail,color = 'k',linestyle = '-',linewidth = lin_pl,label = r'Trailing-edge line' )
    set_ax( ax )

def find_CT( res_beta,roR,teta ):
    CT_choice = CT_p
    tol = 0.05
    idx = [-2 for i in range( len(res_beta) ) ]
    for iS,res_sweep in enumerate( res_beta ):
        idx[iS] = find_val( res_sweep[2],CT_choice,tol )
        sect_plot( roR,res_sweep,idx[iS],iS,teta )

def sect_plot( roR,results,Jsel,iS,teta ): 
    ''' Plots data along span for a given beta,J'''
    
    if isinstance(iS,list) or isinstance(iS,range):
        LST = True
    else:
        LST = False

    if LST:
        # Multiple sweep curves in one plot
        #if iS > len( results )-1:
        #    print( 'ERROR: index out of Range')
        #    return
        ax = 0
        ax2 = 0
        au_ax = 0
        for iSs,res_sweep in enumerate( results ):
            try:
                pos = iS.index(iSs)
            except:
                print('a')
            else: 
                # Cl,Cd vs r/R and dCT,dCp vs r/R
                ax,au_ax,lines  = Cl_Cd_dCT_dCP_vs_r( roR,res_sweep,Jsel,iSs,teta,ax,au_ax )
                # Mcrit,Mdd vs r/R
                ax2,lines  = Mcr_Meff_vs_r( roR,res_sweep,Jsel,iSs,teta,ax2 )
                #iS[pos] = -1 
    else:
        # Only one sweep curve
        ax,a,lines   = Cl_Cd_dCT_dCP_vs_r( roR,results,Jsel,iS,teta,CT = CT_p )
        ax2,lines2  = Mcr_Meff_vs_r( roR,results,Jsel,iS,teta,CT = CT_p )
    # M_crit
    
def find_val( arr,var,tol ):
    store_diff = []
    store_idx  = []
    min,idx = 1,0
    for inum,num in enumerate(arr):
        diff = abs( 1-var/num )
        if diff < tol and diff < min:
            # Finds all the numbers that are in the acceptable margin
            min = diff
            idx = inum
            #store_diff.append( diff )
            #store_idx.append( inum )
    #if isinstance( store_diff,list ): #CHecks if diff is a list or a single number
        #diff = min( store_diff )
        #inum = store_idx.index( diff )
    return idx
    #else:
        #return store_idx