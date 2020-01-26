import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats

dir1 = "q-lambda/processing"

# parameter lists for axes labels
q_list = [0, 0.1, .2, 0.3, .4, 0.5, .6, 0.7, .8, .9, .99, .999, 1]
lam_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

fig, ax = plt.subplots(1,2,figsize=(8,4))

# (1,1): robustness of density result (ER-BA) ... k=5 vs k=20
data1 = np.loadtxt(f"{dir1}/Jan-20/hx_ER_k%i.csv" % 5, delimiter=",")
data2 = np.loadtxt(f"{dir1}/Jan-20/hx_ER_k%i.csv" % 20, delimiter=",")

plt.sca(ax[0])
plt.imshow(np.subtract(data2,data1), origin="lower")
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
cb = plt.colorbar()
cb.ax.set_ylabel(r"$\langle h_\times \rangle_{k = 20} - \langle h_\times\rangle_{k = 5}$",
                 rotation=270, size=12, labelpad=15)

# (1,2): robustness of density result (ER-BA) ... Spearman's for [k=5,k=10,...,k=25]
data = np.zeros((len(q_list),len(lam_list)))
k_list = [5,10,15,20,25]
for i,_ in enumerate(q_list):
    for j,_ in enumerate(lam_list):
        A = [] # append <hx> for each k
        for k in k_list:
            data_q_lam = np.loadtxt(f"{dir1}/Jan-20/hx_ER_k%i.csv" % k, delimiter=",")
            A.append(data_q_lam[i,j])
        data[i,j] = scipy.stats.spearmanr(k_list, A)[0]

plt.sca(ax[1])
plt.imshow(data, origin="lower")
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
cb = plt.colorbar()
cb.ax.set_ylabel(r"Spearman's corr. of $\langle h_\times \rangle$" + "\n" +
          r"for $\langle k \rangle = 5,10,15,20,25$",
                 rotation=270, size=10, labelpad=25)

plt.tight_layout(w_pad=5)
plt.savefig("figure9-v2-InProgress.pdf")
##plt.show()
