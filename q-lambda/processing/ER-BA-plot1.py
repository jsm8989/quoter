import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

q_list = [0, .2, .4, .6, .8, .9, .99, .999, .9999]
lam_list = [1, 2, 4, 6, 8]

data1 = np.loadtxt("hx_ER_k%i.csv" % 5, delimiter=",")
data2 = np.loadtxt("hx_ER_k%i.csv" % 20, delimiter=",")

plt.imshow(np.subtract(data2,data1), origin="lower")
plt.colorbar()
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
plt.title(r"$\langle h_\times \rangle_{k = 20} - \langle h_\times\rangle_{k = 5}$")
plt.show()


