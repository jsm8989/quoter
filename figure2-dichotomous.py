import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bltools as blt

dir1 = "dichotomous_graph/processing"
fig, ax = plt.subplots(2,2,figsize=(8,5),sharey=False)
ax = ax.flatten()

n_list = [250, 500] # network size
k1k2_list = [32,64] # k1+k2, i.e. twice the average degree
q = 0.5
n_style = ["C0", "C1"]
k_style = ["o-", "x-"]

for i,n in enumerate(n_list):
    for j,k1k2 in enumerate(k1k2_list):
        data = pd.read_csv(f"{dir1}/hx_dichotomous_n%i_k1k2%i_q%0.1f.csv" % (n,k1k2,q))
            
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


# 2ND ROW: Influential nodes
n=500
k1k2=32
q = 0.5
data = pd.read_csv(f"{dir1}/hx_dichotomous_n%i_k1k2%i_q%0.1f.csv" % (n,k1k2,q))

edgetypes = [["1","1"],["1","2"],["2","1"],["2","2"]] # which types of edges are most influential/influenced??
##edgetypes = [["X","1"],["X","2"],["1","X"],["2","X"]] # ...     ...    nodes   ....     ...    ...

for e in edgetypes:
    n1 = e[0]
    n2 = e[1]
    plt.sca(ax[2])
    plt.plot(data["degree_ratio"].values, data["hx%s%s_avg" % (n1,n2)].values, "o-", label=r"$n_{%s} \to n_{%s}$" % (n1,n2))

    plt.sca(ax[3])
    plt.plot(data["degree_ratio"].values, data["hx%s%s_var" % (n1,n2)].values, "o-", label=r"$n_{%s} \to n_{%s}$" % (n1,n2))

plt.sca(ax[2])
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.legend()

plt.sca(ax[3])
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Variance of $h_\times$")
plt.legend()

blt.letter_subplots(axes=ax, xoffset=-0.1)
plt.tight_layout()
plt.savefig("figure2-dichotomous.pdf")
plt.show()

