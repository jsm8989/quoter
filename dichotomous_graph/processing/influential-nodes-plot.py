import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

n=500
k1k2=32
q = 0.5

fig, ax = plt.subplots(1,2,figsize=(8,5),sharey=False)
data = pd.read_csv("hx_dichotomous_n%i_k1k2%i_q%0.1f.csv" % (n,k1k2,q))

##edgetypes = [["1","1"],["1","2"],["2","1"],["2","2"]] # which types of edges are most influential/influenced??
edgetypes = [["X","1"],["X","2"],["1","X"],["2","X"]] # ...     ...    nodes   ....     ...    ...

for e in edgetypes:
    n1 = e[0]
    n2 = e[1]
    plt.sca(ax[0])
    plt.plot(data["degree_ratio"].values, data["hx%s%s_avg" % (n1,n2)].values, "o-", label=r"$n_{%s} \to n_{%s}$" % (n1,n2))

    plt.sca(ax[1])
    plt.plot(data["degree_ratio"].values, data["hx%s%s_var" % (n1,n2)].values, "o-", label=r"$n_{%s} \to n_{%s}$" % (n1,n2))

plt.sca(ax[0])
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.legend()

plt.sca(ax[1])
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Variance of $h_\times$")
plt.legend()

plt.tight_layout()
plt.show()
