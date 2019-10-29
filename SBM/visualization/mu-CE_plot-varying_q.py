import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import csv


q_list = np.arange(0,0.21,0.05)
mu_list = np.arange(.05,.51,.05)



hx_w = np.loadtxt("../processing/sbm_seed_N100_vary_q-multi_within.csv",delimiter=",")
hx_b = np.loadtxt("../processing/sbm_seed_N100_vary_q-multi_between.csv",delimiter=",")
hx_all = np.loadtxt("../processing/sbm_seed_N100_vary_q-multi_all.csv",delimiter=",")

##for i,row in enumerate(hx_w): # loop over rows = loop over q's
##    plt.plot(mu_list,hx_w[i,:],'r-',label="q = %0.2f, w" % q_list[i])
##    plt.plot(mu_list,hx_b[i,:],'r-',label="q = %0.2f, b" % q_list[i])

fig = plt.figure(figsize=(10,6))

rows = 2
cols = 3
for n in range(len(q_list)):
    plt.subplot(rows,cols,n+1)
    plt.plot(mu_list,hx_w[n,:])
    plt.plot(mu_list,hx_b[n,:])
##    plt.ylim([3.375,3.3795])
    if n % cols == 0:
        plt.ylabel("Mean cross-entropy")
##    else:
##        plt.yticks([])
    plt.xlabel(r"$\mu$")
    plt.title(r"$q = %0.2f$" % q_list[n])
plt.tight_layout()
plt.show()



