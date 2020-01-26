import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats

q_list = [0, 0.1, .2, 0.3, .4, 0.5, .6, 0.7, .8, .9, .99, .999, 1]
lam_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

data1 = np.loadtxt("Jan-20/hx_ER_k%i.csv" % 5, delimiter=",")
data2 = np.loadtxt("Jan-20/hx_ER_k%i.csv" % 20, delimiter=",")

plt.imshow(np.subtract(data2,data1), origin="lower")
plt.colorbar()
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
plt.title(r"$\langle h_\times \rangle_{k = 20} - \langle h_\times\rangle_{k = 5}$")
plt.show()


# store Spearman's correlation coefficient in data
data = np.zeros((len(q_list),len(lam_list)))
k_list = [5,10,15,20]
for i,_ in enumerate(q_list):
    for j,_ in enumerate(lam_list):
        A = [] # append <hx> for each k
        for k in k_list:
            data_q_lam = np.loadtxt("Jan-20/hx_ER_k%i.csv" % k, delimiter=",")
            A.append(data_q_lam[i,j])
        data[i,j] = scipy.stats.spearmanr(k_list, A)[0]
print(data)
        
plt.imshow(data, origin="lower")
plt.colorbar()
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
plt.title(r"Spearman's correlation of $\langle h_\times \rangle$ for $\langle k \rangle = 5,10,15,20,25$")
plt.show()
