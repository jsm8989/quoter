import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data0 = np.loadtxt("hx_SW-NEW_p%0.1f.csv" % 0, delimiter=",")
data1 = np.loadtxt("hx_SW-NEW_p%0.1f.csv" % 1, delimiter=",")

q_list = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9] + [.99, .999, .9999]
lam_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

plt.imshow(np.subtract(data1,data0), origin="lower")
plt.colorbar()
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
plt.title(r"$\langle h_\times \rangle_{p = 1} - \langle h_\times\rangle_{p = 0}$")
plt.show()
