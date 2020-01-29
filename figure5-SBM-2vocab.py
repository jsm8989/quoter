import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import bltools as blt

dir1 = "SBM_Vocab/processing"

alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5)]
mu = 0.15

fig, ax = plt.subplots(1,3,figsize=(10,5),sharey=True)
for i,alpha in enumerate(alpha_list):
    plt.sca(ax[i])
    alpha_A = alpha[0]
    alpha_B = alpha[1]

    # load data
    data =  pd.read_csv(f"{dir1}/sbm_2param_aA%0.1f_aB%0.1f.csv" % (alpha_A,alpha_B))

    # what to plot on the x-axis? within-block connection prob, modularity, ?
    #x = data["p"].values
    x = np.linspace(-.2,.3,11)

    plt.plot(x,data["AB"].values,'o-',label=r"$A \to B$") # these are reversed oops
    plt.plot(x,data["BA"].values,'o-',label=r"$B \to A$") # ...
    plt.plot(x,data["AA"].values,'o-',label=r"$A \to A$")
    plt.plot(x,data["BB"].values,'o-',label=r"$B \to B$")
##    plt.plot(x,data["hx_w"].values,'o-',label="within")
##    plt.plot(x,data["hx_b"].values,'o-',label="between")
    
    plt.title(r"$\alpha_A = %0.1f, \alpha_B = %0.1f$" % (alpha_A,alpha_B))
    if i == 0:
        plt.legend(title=r"$h_\times$")
        plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
    if i == 1:
        plt.xlabel(r"Modularity, $Q$")

plt.tight_layout()
blt.letter_subplots(axes=ax, xoffset=0, yoffset=1.05)
plt.savefig("figure5-SBM-2vocab.pdf")
plt.show()
