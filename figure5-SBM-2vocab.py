import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import bltools as blt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def Zipf(alpha,N):
    vocab = np.arange(1,N+1)
    weights = vocab**(-alpha)
    weights /= weights.sum()
    return weights

dir1 = "SBM_Vocab/processing"

alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5)]
mu = 0.15

fig, ax = plt.subplots(1,3,figsize=(8,3),sharey=True, constrained_layout=True)
for i,alpha in enumerate(alpha_list):
    plt.sca(ax[i])
    alpha_A = alpha[0]
    alpha_B = alpha[1]

    # load data
    data =  pd.read_csv(f"{dir1}/sbm_2param_aA%0.1f_aB%0.1f.csv" % (alpha_A,alpha_B))

    # what to plot on the x-axis? within-block connection prob, modularity, ?
    #x = data["p"].values
    x = np.linspace(-.2,.3,11)

    plt.plot(x,data["AB"].values,'o-',label=r"$A \to B$", ms=4) # these are reversed oops
    plt.plot(x,data["BA"].values,'o-',label=r"$B \to A$", ms=4) # ...
    plt.plot(x,data["AA"].values,'s-',label=r"$A \to A$", ms=4)
    plt.plot(x,data["BB"].values,'s-',label=r"$B \to B$", ms=4)
##    plt.plot(x,data["hx_w"].values,'o-',label="within")
##    plt.plot(x,data["hx_b"].values,'o-',label="between")
    
    plt.title(r"$\alpha_A = %0.1f, \alpha_B = %0.1f$" % (alpha_A,alpha_B))
    if i == 0:
##        plt.legend(title=r"$h_\times$")
        plt.legend(title=r'$h_\times$', ncol=1, fontsize=9, labelspacing=0, handlelength=0.75, handletextpad=0.4, borderaxespad=0.25)
        plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
    if i == 1:
        plt.xlabel(r"Modularity, $Q$")

    # inset plots
    axcurr = plt.gca()
    dd = 0.02
    dx,dy = -0.195+dd, -0.13+dd
    a = 1.3
    wi,hi = a*0.4-dd,a*0.4*0.8-dd
    if i == 0:
        axins = inset_axes(axcurr, width="100%", height="100%",
                   bbox_to_anchor=(.65+dx, .3+dy, wi,hi),
                   bbox_transform=axcurr.transAxes, loc="center")
    else:
        axins = inset_axes(axcurr, width="100%", height="100%",
                   bbox_to_anchor=(.65+dx, .67+dy, wi,hi),
                   bbox_transform=axcurr.transAxes, loc="center")
    axins.tick_params(labelsize=9)
        

    plt.plot(list(range(1,1001)),Zipf(alpha_A,1000),"k",   linewidth=2, label=r'$A$')
    plt.plot(list(range(1,1001)),Zipf(alpha_B,1000),"C6:",linewidth=3, label=r'$B$')
    if i == 0:
        plt.legend(fontsize=8,  labelspacing=0,handletextpad=0.4, borderaxespad=0.25,loc='lower left')
    plt.xlabel(r"$r$", labelpad=-2)
    plt.ylabel(r"       $P(w_r)$")
    plt.xscale("log")
    plt.yscale("log")

blt.letter_subplots(axes=ax, yoffset=1.05, xoffset=0)
# plt.tight_layout()
plt.savefig("figure5-SBM-2vocab.pdf")
#plt.show()
