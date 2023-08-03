import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bltools as blt

dir1 = "q-lambda/processing"

# parameter lists for axes labels
q_list = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9] + [.99, .999, .9999]
lam_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

a = 1.6
fig, ax = plt.subplots(1,3,figsize=(8*a,3*a))

# (1,1): robustness of density result (ER)
data1 = np.loadtxt(f"{dir1}/hx_ER-NEW_k%i.csv" % 6, delimiter=",")
data2 = np.loadtxt(f"{dir1}/hx_ER-NEW_k%i.csv" % 20, delimiter=",")

plt.sca(ax[0])
plt.imshow(np.subtract(data2,data1), origin="lower")
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Mean quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$", labelpad=-10)
cb = plt.colorbar(fraction=0.058, pad=0.05)
cb.ax.tick_params(labelsize=8)
cb.ax.set_ylabel(r"$\langle h_\times \rangle_{k = 20} - \langle h_\times\rangle_{k = 6}$",
                 rotation=270, size=12, labelpad=20)
plt.title("Erdős-Rényi")

# (1,2): robustness of density result (BA)
data1 = np.loadtxt(f"{dir1}/hx_BA_k%i.csv" % 6, delimiter=",")
data2 = np.loadtxt(f"{dir1}/hx_BA_k%i.csv" % 20, delimiter=",")

plt.sca(ax[1])
plt.imshow(np.subtract(data2,data1), origin="lower")
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Mean quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$", labelpad=-10)
cb = plt.colorbar(fraction=0.058, pad=0.05)
cb.ax.tick_params(labelsize=8)
cb.ax.set_ylabel(r"$\langle h_\times \rangle_{k = 20} - \langle h_\times\rangle_{k = 6}$",
                 rotation=270, size=12, labelpad=20)
plt.title("Barabási-Albert")


# (1,3): robustness of clustering result (small-world)
data0 = np.loadtxt(f"{dir1}/hx_SW-NEW_p%0.1f.csv" % 0, delimiter=",")
data1 = np.loadtxt(f"{dir1}/hx_SW-NEW_p%0.1f.csv" % 1, delimiter=",")

plt.sca(ax[2])
plt.imshow(np.subtract(data1,data0), origin="lower")
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Mean quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$", labelpad=-10)
cb = plt.colorbar(fraction=0.058, pad=0.05)
cb.ax.tick_params(labelsize=8)
cb.ax.set_ylabel(r"$\langle h_\times \rangle_{p = 0} - \langle h_\times\rangle_{p = 1}$",
                 rotation=270, size=12, labelpad=20)
plt.title("Small-World")



#blt.letter_subplots(axes=ax, xoffset=-0.22, yoffset=1.03)
plt.tight_layout()
plt.savefig("figure8-robustness-q-lambda.pdf")
# plt.show()


