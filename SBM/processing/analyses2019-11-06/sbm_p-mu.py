import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N=40
q=0.5
T=1000
p_list = [0.2,0.4,0.6,0.8]
mu_list = [0.2,0.4,0.6,0.8]
trials_list = list(range(200))

W = np.zeros((len(p_list),len(mu_list)))
B = np.zeros((len(p_list),len(mu_list)))
for i,p in enumerate(p_list):
    for j,mu in enumerate(mu_list):
        hx_w = []
        hx_b = []
        for trial in trials_list:
            if trial % 50 == 0:
                print(i,j,trial)
            
            efile = "../../data_sbm-p-mu-N40/N%i_p%0.3f_mu%0.4f_q%0.2f_T%i_sim%i.txt" % (N,p,mu,q,T,trial)

            edata = pd.read_csv(efile, sep = " ")

            block1 = list(range(0,int(N/2)))
            block2 = list(range(int(N/2),N))

            edata = edata.loc[edata["distance"] == 1] # links only

            hx_w.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block1))].values)
            hx_w.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block2))].values)
            hx_b.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block2))].values)
            hx_b.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block1))].values)

        W[i,j] = np.mean(hx_w)
        B[i,j] = np.mean(hx_b)

inds = ["p=%0.1f" % p for p in p_list]
cols = ["mu=%0.1f" % mu for mu in mu_list]
dfW = pd.DataFrame(data=W,index=inds,columns=cols)
dfW = dfW.to_csv("sbm_q%0.1f_W_links.csv" % q, index=False)
dfB = pd.DataFrame(data=B,index=inds,columns=cols)
dfB = dfB.to_csv("sbm_q%0.1f_B_links.csv" % q, index=False)

dataW =  pd.read_csv("sbm_q%0.1f_W_links.csv" % q).values
dataB =  pd.read_csv("sbm_q%0.1f_B_links.csv" % q).values

style = ['r-','k-','b-','g-']
for j in range(len(mu_list)):
    plt.plot(p_list,dataW[:,j],style[j],label=r"$\mu=%0.1f$" % mu_list[j])
    plt.plot(p_list,dataB[:,j],style[j]+'-',label=r"$\mu=%0.1f$" % mu_list[j])

plt.legend()
plt.xlabel(r"$p$")
plt.ylabel("Cross-entropy")
plt.show()


