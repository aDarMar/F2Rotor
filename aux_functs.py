from numpy import linspace
import matplotlib.pyplot as plt

def polar_calc(alphas,Res,Ms):
    Re_v = linspace(Res[0],Res[1],nRe)
    M_v  = linspace(Ms[0],Ms[1],nM)


def calc_sects(alphas,aero,Re,M):
    Re_ref = 1e6
    nA = 10
    alpha_v = linspace(alphas[0],alphas[1],nA)
    Cl = linspace(0,0,nA)
    Cd = linspace(0,0,nA)
    for an,aoa in enumerate(alpha_v):
        Cl[an],Cd[an] = aero.clcd2( aoa, Re_ref, Re, M )
    plot_fun(Cl,Cd,alpha_v)


def plot_fun(Cl,Cd,alpha):
    fig,ax = plt.subplots(2,1)
    ax[0].plot(alpha,Cl)
    ax[1].plot(Cd,Cl)

    plt.show()