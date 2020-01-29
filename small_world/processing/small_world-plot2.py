import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

##N_list = [200,400]
##k_list = [6,12]
##q=0.5
##
##N_style = ["C0", "C1"]
##k_style = ["o-", "x-"]
##
### hx versus p
##for i,N in enumerate(N_list):
##    for j,k in enumerate(k_list):
##        data = pd.read_csv("small_world_N%i_k%i_q%0.1f.csv" % (N,k,q))
##        plt.plot(data["p"], data["hx_avg"], N_style[i] + k_style[j], label="%i, %i" % (N,k))
##        
##plt.xlabel(r"Rewiring probability, $p$")
##plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
##plt.xscale("log")
##plt.legend(title=r"$N, k$")
##plt.show()
##
### hx versus transitivity
##for i,N in enumerate(N_list):
##    for j,k in enumerate(k_list):
##        data = pd.read_csv("small_world_N%i_k%i_q%0.1f.csv" % (N,k,q))
##        plt.plot(data["C"], data["hx_avg"], N_style[i] + k_style[j], label="%i, %i" % (N,k))
##        
##plt.xlabel("Transitivity")
##plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
##plt.legend(title=r"$N, k$")
##plt.show()



q_list = [0.1, 0.5, 0.9]
N = 200
k = 6
# hx versus p
for i,q in enumerate(q_list):
    data = pd.read_csv("small_world_N%i_k%i_q%0.1f.csv" % (N,k,q))
    plt.plot(data["p"], data["hx_avg"], "o-", label=r"$q=%0.1f$" % q)
        
plt.xlabel(r"Rewiring probability, $p$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.xscale("log")
plt.legend()
plt.show()

# hx versus transitivity
for i,q in enumerate(q_list):
    data = pd.read_csv("small_world_N%i_k%i_q%0.1f.csv" % (N,k,q))
    plt.plot(data["C"], data["hx_avg"], "o-", label=r"$q=%0.1f$" % q)
        
plt.xlabel("Transitivity")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.legend()
plt.show()
