import sys, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import bltools as blt

dir1 = "SBM_Nov12/processing"

mu_list = [0.15,0.20,0.25,0.30]
N = 100
m = N//2
a=1.15
fig, ax = plt.subplots(1,3,figsize=(a*8,a*3),sharey=False)

style = ['C0-','C1-','C2-','C3-']

### hx vs p
plt.sca(ax[0])
for i,mu in enumerate(mu_list):
    data =  pd.read_csv(f"{dir1}/sbm_mu%0.2f_N%i.csv" % (mu,N))
    plt.plot(data["p"].values, data["hx_w"].values, style[i], label="%0.2f" % mu)
    plt.plot(data["p"].values, data["hx_b"].values, style[i]+'-')
leg1 = plt.legend(title=r"$p_1$", handlelength=1, fontsize=9)
ax[0].add_artist(leg1)

win_line = mlines.Line2D([], [], color='k', ls='-',  label='Within')
btw_line = mlines.Line2D([], [], color='k', ls='--', label='Between')
plt.legend([win_line, btw_line], ['Within', "Between"], loc='upper left', handlelength=1.25, fontsize=9)

plt.xlabel(r"$p_0$")
plt.ylabel(r"$\langle h_\times \rangle$")

# (1,1): Delta hx vs p
plt.sca(ax[1])
for i,mu in enumerate(mu_list):
    data =  pd.read_csv(f"{dir1}/sbm_mu%0.2f_N%i.csv" % (mu,N))
    plt.plot(data["p"].values, data["hx_b"].values-data["hx_w"].values, style[i], label="%0.2f" % mu)
plt.legend(title=r"$p_1$", fontsize=9, handlelength=1)
plt.xlabel(r"$p_0$")
plt.ylabel(r"$\Delta h_\times$")
plt.axhline(y=0, linestyle='--', color='k', zorder=-2, lw=1)

# (1,2): Delta hx vs modularity
plt.sca(ax[2])
for i,mu in enumerate(mu_list):
    data =  pd.read_csv(f"{dir1}/sbm_mu%0.2f_N%i.csv" % (mu,N))
    p_list = data["p"].values
    mu_list = np.array([mu]*len(p_list))
    modularity = (1/2)*np.divide(p_list-p_list*m+mu_list*m, p_list-p_list*m-mu_list*m)
    delta_hx = data["hx_b"].values-data["hx_w"].values
    plt.plot(modularity, delta_hx, style[i], label="%0.2f" % mu)

plt.axhline(y=0, linestyle='--', color='k', zorder=-2, lw=1)
plt.xlabel(r"Modularity, $Q$")
plt.ylabel(r"$\Delta h_\times$")
plt.legend(title=r"$p_1$", fontsize=9, handlelength=1)

blt.letter_subplots(xoffset=[-0.275,-0.29,-0.29])
plt.tight_layout(w_pad=0.5)
plt.savefig("figure5-SBM.pdf")
##plt.show()
