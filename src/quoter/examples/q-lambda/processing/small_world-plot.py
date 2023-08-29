import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data1 = np.loadtxt("hx_SW_p%0.1f.csv" % 0, delimiter=",")
data2 = np.loadtxt("hx_SW_p%0.1f.csv" % 1, delimiter=",")

q_list = [0, .2, .4, .6, .8, .9, .99, .999, .9999]
lam_list = [1, 2, 4, 6, 8]

plt.imshow(np.subtract(data2,data1), origin="lower")
plt.colorbar()
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
plt.title(r"$\langle h_\times \rangle_{p = 0} - \langle h_\times\rangle_{p = 1}$")
plt.show()
