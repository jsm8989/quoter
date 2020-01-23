import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir("Hubs_Vocab/processing")

ERparam =  np.arange(2,51,2) # for ER
BAparam = list(range(1,21+1)) + list(range(22,25+1)) # for BA
N = 1000
BAparam = [2*m - 2*m**2/N for m in BAparam] # theoretical degree

alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5)] 
style = ['-','x','o']

fig, ax = plt.subplots(1,2,figsize=(8,4),sharey=False)
for i,alphas in enumerate(alpha_list):
    alpha = alphas[0]
    hub_alpha = alphas[1]

    # load data
    ER = pd.read_csv("hx_ER_A%0.1f_HA%0.1f.csv" % (alpha,hub_alpha))
    BA = pd.read_csv("hx_BA_A%0.1f_HA%0.1f.csv" % (alpha,hub_alpha))

    # avg hx vs avg deg
    plt.sca(ax[0])
    plt.plot(ERparam,ER["hx_avg"].values,'k'+style[i],label=r"$\alpha=%0.1f, \alpha_{hub}=%0.1f$" %(alpha,hub_alpha))
    plt.plot(BAparam,BA["hx_avg"].values,'r'+style[i])
    plt.xlabel(r"$\langle k \rangle$")
    plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
    plt.title("Black = ER, Red = BA")
    plt.legend() 

    # variance hx vs avg deg
    plt.sca(ax[1])
    plt.plot(ERparam,np.power(ER["hx_std"].values,2),'k'+style[i])
    plt.plot(BAparam,np.power(BA["hx_std"].values,2),'r'+style[i])
    plt.xlabel(r"$\langle k \rangle$")
    plt.ylabel(r"Variance of $h_\times$")

plt.tight_layout()
plt.savefig("../../figure6.pdf")
plt.show()

