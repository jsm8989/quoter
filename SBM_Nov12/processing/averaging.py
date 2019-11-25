import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N= 1000
q=0.9
T=1000
p_list = np.arange(0.1,0.71,0.1)
mu = 0.15
trials_seq = [50,100,200,500]

##for n_trials in trials_seq:
##    W = np.zeros(len(p_list))
##    B = np.zeros(len(p_list))
##    for i,p in enumerate(p_list):
##        hx_w = []
##        hx_b = []
##        print(n_trials,p)
##        for trial in range(n_trials):
##            
##            efile = "../data-Nov13/edge/N%i_p%0.3f_mu%0.4f_q%0.2f_T%i_sim%i.txt" % (N,p,mu,q,T,trial)
##            try:
##                edata = pd.read_csv(efile, sep = " ")
##            except:
##                print("No data", p,mu,trial)
##
##            else:
##                
##                block1 = list(range(0,int(N/2)))
##                block2 = list(range(int(N/2),N))
##
##                hx_w.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block1))].values)
##                hx_w.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block2))].values)
##                hx_b.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block2))].values)
##                hx_b.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block1))].values)
##
##        W[i] = np.mean(hx_w)
##        B[i] = np.mean(hx_b)
##
##
##    df = pd.DataFrame({"p":p_list,"hx_w":W,"hx_b":B})
##    df = df.to_csv("averaging/sbm_q%0.1f_trials%i.csv" % (q,n_trials), index=False)




# PLOT: subplots
style=['C%i-' %i for i in range(len(trials_seq))]
fig,ax = plt.subplots(1,4,figsize=(11,4),sharey=True)
for i,n_trials in enumerate(trials_seq):
    plt.sca(ax[i])
    data = pd.read_csv("averaging/sbm_q%0.1f_trials%i.csv" % (q,n_trials))
    plt.plot(data["p"],data["hx_w"],style[i],label="within")
    plt.plot(data["p"],data["hx_b"],style[i]+'-',label="between")
    plt.xlabel("$p$")
    plt.legend()
    plt.title("%i trials" % (2*trials_seq[i]))
    if i==0:
        plt.ylabel("Average cross-entropy")
plt.show()


