import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

N_list = [200,400]
k_list = [6,12]

N_style = ["C0", "C1"]
k_style = ["o-", "x-"]

# hx versus p
for i,N in enumerate(N_list):
    for j,k in enumerate(k_list):
        data = pd.read_csv("small_world_N%i_k%i.csv" % (N,k))
        plt.plot(data["p"], data["hx_avg"], N_style[i] + k_style[j], label="%i, %i" % (N,k))
        
plt.xlabel(r"Rewiring probability, $p$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.xscale("log")
plt.legend(title=r"$N, k$")
plt.show()

# hx versus transitivity
for i,N in enumerate(N_list):
    for j,k in enumerate(k_list):
        data = pd.read_csv("small_world_N%i_k%i.csv" % (N,k))
        plt.plot(data["C"], data["hx_avg"], N_style[i] + k_style[j], label="%i, %i" % (N,k))
        
plt.xlabel("Transitivity")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
##plt.xscale("log")
plt.legend(title=r"$N, k$")
plt.show()
