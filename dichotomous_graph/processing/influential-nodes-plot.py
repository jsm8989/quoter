import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

n=500
k1k2=64
q = 0.9

fig, ax = plt.subplots(1,2,figsize=(8,4),sharey=False)
data = pd.read_csv("hx_dichotomous_influentials_n%i_k1k2%i_q%0.1f.csv" % (n,k1k2,q))


for nn in [[1,1],[1,2],[2,1],[2,2]]:
    n1 = nn[0]
    n2 = nn[1]
    plt.sca(ax[0])
    plt.plot(data["degree_ratio"].values, data["hx%i%i_avg" % (n1,n2)].values, "o-", label=r"$n_{%i} \to n_{%i}$" % (n1,n2))

    plt.sca(ax[1])
    plt.plot(data["degree_ratio"].values, data["hx%i%i_var" % (n1,n2)].values, "o-", label=r"$n_{%i} \to n_{%i}$" % (n1,n2))

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
