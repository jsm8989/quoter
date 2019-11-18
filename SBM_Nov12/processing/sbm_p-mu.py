import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N= 1000
q=0.5
T=1000
p_list = mu_list = np.arange(0.1,0.91,0.1)
trials_list = list(range(200))

##W = np.zeros((len(p_list),len(mu_list)))
##B = np.zeros((len(p_list),len(mu_list)))
##for i,p in enumerate(p_list):
##    for j,mu in enumerate(mu_list):
##        hx_w = []
##        hx_b = []
##        print(i,j)
##        count = 0
##        for trial in trials_list:
##            
##            efile = "../data/edge/N%i_p%0.3f_mu%0.4f_q%0.2f_T%i_sim%i.txt" % (N,p,mu,q,T,trial)
##            try:
##                edata = pd.read_csv(efile, sep = " ")
##            except:
##                print("No data", p,mu,trial)
##
##            else:
##                count += 1
##                
##                block1 = list(range(0,int(N/2)))
##                block2 = list(range(int(N/2),N))
##
##                hx_w.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block1))].values)
##                hx_w.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block2))].values)
##                hx_b.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block2))].values)
##                hx_b.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block1))].values)
##
##        if count > 100: # missing some data. Only compute <hx> for (p,mu) with 100+ trials
##            W[i,j] = np.mean(hx_w)
##            B[i,j] = np.mean(hx_b)
##
##inds = ["p=%0.1f" % p for p in p_list]
##cols = ["mu=%0.1f" % mu for mu in mu_list]
##dfW = pd.DataFrame(data=W,index=inds,columns=cols)
##dfW = dfW.to_csv("sbm_q%0.1f_W_links.csv" % q, index=False)
##dfB = pd.DataFrame(data=B,index=inds,columns=cols)
##dfB = dfB.to_csv("sbm_q%0.1f_B_links.csv" % q, index=False)




# PLOT
dataW =  pd.read_csv("sbm_q%0.1f_W_links.csv" % q).values[:7,:]
dataB =  pd.read_csv("sbm_q%0.1f_B_links.csv" % q).values[:7,:]
print(dataW)
##style = ['k-','b-','r-','g-',]
mu_list = np.arange(0.1,0.91,0.1)
p_list = np.arange(0.1,0.71,0.1)
for j in range(len(mu_list)):
##    plt.plot(p_list,dataW[:,j],style[j],label=r"$\mu=%0.1f$" % mu_list[j])
##    plt.plot(p_list,dataB[:,j],style[j]+'-')
    if j % 2 == 1:
        plt.plot(p_list,dataW[:,j],'C' + str(j//2) + '-',label=r"$\mu=%0.1f$" % mu_list[j])
        plt.plot(p_list,dataB[:,j],'C' + str(j//2) + '--')

plt.legend()
plt.xlabel(r"$p$")
plt.ylabel("Cross-entropy")
plt.show()


