import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dir1 = "q-lambda/processing"

# parameter lists for axes labels
q_list = [0, .2, .4, .6, .8, .9, .99, .999, .9999]
lam_list = [1, 2, 4, 6, 8]


fig, ax = plt.subplots(1,2,figsize=(8,4))

# (1,1): robustness of density result (ER-BA)
data1 = np.loadtxt(f"{dir1}/hx_ER_k%i.csv" % 5, delimiter=",")
data2 = np.loadtxt(f"{dir1}/hx_ER_k%i.csv" % 20, delimiter=",")

plt.sca(ax[0])
plt.imshow(np.subtract(data2,data1), origin="lower")
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
cb = plt.colorbar()
cb.ax.set_ylabel(r"$\langle h_\times \rangle_{k = 20} - \langle h_\times\rangle_{k = 5}$",
                 rotation=270, size=12, labelpad=20)

# (1,2): robustness of clustering result (small-world)
data1 = np.loadtxt(f"{dir1}/hx_SW_p%0.1f.csv" % 0, delimiter=",")
data2 = np.loadtxt(f"{dir1}/hx_SW_p%0.1f.csv" % 1, delimiter=",")

plt.sca(ax[1])
plt.imshow(np.subtract(data2,data1), origin="lower")
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
cb = plt.colorbar()
cb.ax.set_ylabel(r"$\langle h_\times \rangle_{p = 0} - \langle h_\times\rangle_{p = 1}$",
                 rotation=270, size=12, labelpad=20)

plt.tight_layout(w_pad=5)
plt.savefig("figure9.pdf")
##plt.show()


