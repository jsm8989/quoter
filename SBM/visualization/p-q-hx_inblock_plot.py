import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

hx_w = np.loadtxt("../processing/sbm_w_N40.csv",delimiter=",")
hx_b = np.loadtxt("../processing/sbm_b_N40.csv",delimiter=",")

sbm_p_list = [0.2,0.4,0.6,0.8]
sbm_q_list = [0.2,0.4,0.6,0.8]

# Plot 1 -- scatterplot of (p,q) colored by cross-entropy
##for i,sbm_p in enumerate(sbm_p_list):
##    for j,sbm_q in enumerate(sbm_q_list):
##        plt.scatter(sbm_p,sbm_q,c=hx[i,j],vmin=np.min(hx),vmax=np.max(hx))
##
##plt.xlabel(r"$p$")
##plt.ylabel(r"$q$")
##plt.title(r"Information flow in two block symmetric $SBM(p,q)$")
##plt.colorbar()
##plt.show()


# Plot 2 -- plot of p vs cross-entropy, one line plotted per q
style = ['k-','b-','r-','g-']
for j,sbm_q in enumerate(sbm_q_list):
    plt.plot(sbm_p_list, hx_w[:,j], style[j], label="q = %0.1f" % sbm_q)
    plt.plot(sbm_p_list, hx_b[:,j], style[j]+"-")

plt.annotate(s="within block edges",xy=(0.32,3.33))
plt.annotate(s="between block edges",xy=(0.6,3.345))
plt.xlabel(r"$p$ (within block density)")
plt.ylabel("Average cross-entropy per link [bits]")
plt.legend(title="between block density")
plt.title(r"Information flow in $SBM(p,q)$")
plt.show()


# Plot 3 -- plot of q vs cross-entropy, one line plotted per p
##for i,sbm_p in enumerate(sbm_p_list):
##    plt.plot(sbm_q_list, hx[i,:], label="p = %0.1f" % sbm_p)
##
##plt.xlabel(r"$q$ (between block density)")
##plt.ylabel("Average cross-entropy per link [bits]")
##plt.legend(title="within block density")
##plt.title(r"Information flow in two block symmetric $SBM(p,q)$")
##plt.show()
