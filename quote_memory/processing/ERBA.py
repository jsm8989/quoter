# -*- coding: utf-8 -*-

# ER_sims.py
# Tyson Pond
# Last Modified: 2019-10-14

import networkx as nx # version 1.11
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


N = 200
q = 0.5
T = 1000

param_list = np.arange(2,21,2) # k's for ER
##param_list = [ 1, 2, 3,  4,  5,  6, 7,  8,  9, 11] # m's for BA

trials_list = list(range(200))

##hx_avg = np.zeros(len(param_list))
##hx_var = np.zeros(len(param_list))
##for i,x in enumerate(param_list):
##    print(x)
##    hx_trial = []
##    for trial in trials_list:
##        efile = "../data_ER/edge/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)            
####        efile = "../data_BA/edge/N%i_m%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)            
##        edata = pd.read_csv(efile, sep = " ")
##        hx_trial.extend(edata["hx"].values)
##
##    hx_avg[i] = np.mean(hx_trial)
##    hx_var[i] = np.var(hx_trial)
##
##df = pd.DataFrame({"param":param_list,"hx_avg":hx_avg,"hx_var":hx_var})
##df.to_csv("hx_ER.csv",index=False)

ER=pd.read_csv("hx_ER.csv")
BA=pd.read_csv("hx_BA.csv")
ERparam = np.arange(2,21,2) # k's for ER
BAparam = [ 1, 2, 3,  4,  5,  6, 7,  8,  9, 11] # m's for BA
BAparam = [2*m - 2*m**2/N for m in BAparam]

fig,ax = plt.subplots(1,2,figsize=(8,4),sharey=False)
plt.sca(ax[0])
plt.plot(ERparam,ER["hx_avg"],'ko',label="ER")
plt.plot(BAparam,BA["hx_avg"],'ro',label="BA")
plt.legend()
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel(r"$\langle h_\times \rangle$")

plt.sca(ax[1])
plt.plot(ERparam,ER["hx_var"],'ko')
plt.plot(BAparam,BA["hx_var"],'ro')
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel("Variance cross-entropy")
plt.tight_layout()
plt.show()




