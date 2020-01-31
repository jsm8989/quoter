import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bltools as blt

dir1 = "ER_BA_N1000/processing"
dir2 = "dichotomous_graph/processing"

fig, ax = plt.subplots(2,3,figsize=(8,5),sharey=False)
ax = ax.flatten()

ER = pd.read_csv(f"{dir1}/hx_ER.csv")
BA = pd.read_csv(f"{dir1}/hx_BA.csv")
N = 1000
BAdeg = np.array([2*m - 2*m**2/N for m in BA["m"].values]) # theoretical degree for BA

### variance of cross-entropy vs average degree
plt.sca(ax[0])
Ier_ = ER["k"].values <= 40
Iba_ = BAdeg <= 40
plt.plot(ER["k"].values[Ier_], np.power(ER["hx_std"].values[Ier_], 2), 'ko-', label="ER")
plt.plot(BAdeg[Iba_], np.power(BA["hx_std"].values[Iba_], 2), 'ro-', label="BA")
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel(r"Variance of $h_\times$")


# DICHOTOMOUS NETWORKS
n_list = [250, 500] # size of each group... total number of nodesis N=2*n
k1k2_list = [32,64] # k1+k2... average degree is (k1+k2)/2
q = 0.5
n_style = ["C0", "C1"]
k_style = ["o-", "x-"]

for i,n in enumerate(n_list):
    for j,k1k2 in enumerate(k1k2_list):
        data = pd.read_csv(f"{dir2}/hx_dichotomous_n%i_k1k2%i_q%0.1f.csv" % (n,k1k2,q))
            
        plt.sca(ax[1])
        plt.plot(data["degree_ratio"].values, data["hx_avg"].values, n_style[i] + k_style[j], label="%i, %i" % (2*n,k1k2/2))
##        plt.plot(data["degree_variance"].values, data["hx_avg"].values, n_style[i] + k_style[j], label="%i %i" % (n,k1k2/2))
        
        plt.sca(ax[2])
        plt.plot(data["degree_ratio"].values, data["hx_var"].values, n_style[i] + k_style[j], label="%i, %i" % (2*n,k1k2/2))
##        plt.plot(data["degree_variance"].values, data["hx_var"].values, n_style[i] + k_style[j], label="%i %i" % (n,k1k2/2))

plt.sca(ax[1])
##plt.xlabel(r"Variance of degree distribution")
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")

plt.sca(ax[2])
##plt.xlabel(r"Variance of degree distribution")
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Variance of $h_\times$")
plt.legend(title = r"$N, \langle k \rangle$", fontsize='small')

# (2,1):
ax[3].set_visible(False)

# 2ND ROW: Influential nodes
n=500 # size of each group... total number of nodesis N=2*n
k1k2=32 # k1+k2... average degree is (k1+k2)/2
q = 0.5
data = pd.read_csv(f"{dir2}/hx_dichotomous_n%i_k1k2%i_q%0.1f.csv" % (n,k1k2,q))

# (2,2): 
plt.sca(ax[4])
edgetypes = [["1","1"],["1","2"],["2","1"],["2","2"]] # which types of edges are most influential/influenced??

for e in edgetypes:
    n1 = e[0]
    n2 = e[1]
    
    plt.plot(data["degree_ratio"].values, data["hx%s%s_avg" % (n1,n2)].values, "o-", label=r"$k_{%s} \to k_{%s}$" % (n1,n2))

plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.legend()

# (2,3):
plt.sca(ax[5])
##edgetypes = [["X","1"],["X","2"],["1","X"],["2","X"]]
edgetypes = [["X","1"],["X","2"]]
for e in edgetypes:
    n1 = e[0]
    n2 = e[1]
    plt.plot(data["degree_ratio"].values, data["hx%s%s_avg" % (n1,n2)].values, "o-", label=r"$k_{\bullet} \to k_{%s}$" % n2)

plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.legend()

blt.letter_subplots(axes=[ax[0],ax[1],ax[2],ax[4],ax[5]], xoffset=-0.1, yoffset=1.1)
plt.tight_layout()
plt.savefig("figure3-dichotomous.pdf")
plt.show()

