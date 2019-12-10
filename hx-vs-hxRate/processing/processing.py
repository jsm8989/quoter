import networkx as nx # version 1.11
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys




N = 1000
q = 0.5
T = 1000

alpha = hub_alpha = 1.5
k = 10
trials_list = list(range(200))



hx, hx_shuffle_ego, hx_shuffle_alter, hx_shuffle_both = [], [], [], []
for trial in trials_list:
    efile = "../data_ER/edge/N%i_k%i_A%0.1f_HA%0.1f_q%0.1f_T%i_sim%i.txt" % (N,k,alpha,hub_alpha,q,T,trial)
    if os.path.isfile(efile):
        edata = pd.read_csv(efile, sep = " ")
        hx.extend(edata["hx"].values)
        hx_shuffle_ego.extend(edata["hx_target"].values)
        hx_shuffle_alter.extend(edata["hx_source"].values)
        hx_shuffle_both.extend(edata["hx_both"].values)

plt.plot(sorted(hx),1. * np.arange(len(hx)) / (len(hx) - 1),label="ordered")
plt.plot(sorted(hx_shuffle_ego),1. * np.arange(len(hx_shuffle_ego)) / (len(hx_shuffle_ego) - 1),label="ego shuffled")
plt.plot(sorted(hx_shuffle_alter),1. * np.arange(len(hx_shuffle_alter)) / (len(hx_shuffle_alter) - 1), label="alter shuffled")
plt.plot(sorted(hx_shuffle_both),1. * np.arange(len(hx_shuffle_both)) / (len(hx_shuffle_both) - 1), label="both shuffled")
plt.legend()
plt.xlabel("Cross-entropy")
plt.ylabel("Cumulative frequency")
plt.show()
