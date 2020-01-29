import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bltools as blt

dir1 = "dichotomous_graph/processing"
##fig, ax = plt.subplots(1,2,figsize=(7,3),sharey=False)
fig, ax = plt.subplots(1,2,figsize=(7,3),sharey=False)

n_list = [250, 500] # network size
k1k2_list = [32,64] # k1+k2, i.e. twice the average degree

n_style = ["C0", "C1"]
k_style = ["o-", "x-"]

for i,n in enumerate(n_list):
    for j,k1k2 in enumerate(k1k2_list):
        data = pd.read_csv(f"{dir1}/hx_dichotomous_n%i_k1k2%i.csv" % (n,k1k2))
            
        plt.sca(ax[0])
        plt.plot(data["degree_ratio"].values, data["hx_avg"].values, n_style[i] + k_style[j], label="%i, %i" % (2*n,k1k2/2))
##        plt.plot(data["degree_variance"].values, data["hx_avg"].values, n_style[i] + k_style[j], label="%i %i" % (n,k1k2/2))
        
        plt.sca(ax[1])
        plt.plot(data["degree_ratio"].values, data["hx_var"].values, n_style[i] + k_style[j], label="%i, %i" % (2*n,k1k2/2))
##        plt.plot(data["degree_variance"].values, data["hx_var"].values, n_style[i] + k_style[j], label="%i %i" % (n,k1k2/2))

plt.sca(ax[0])
##plt.xlabel(r"Variance of degree distribution")
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")

plt.sca(ax[1])
##plt.xlabel(r"Variance of degree distribution")
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Variance of $h_\times$")
plt.legend(title = r"$N, \langle k \rangle$", fontsize='small')

blt.letter_subplots(axes=ax, xoffset=-0.1)
plt.tight_layout()
plt.savefig("figure2.pdf")
plt.show()

