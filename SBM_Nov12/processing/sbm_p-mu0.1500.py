import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N= 1000
q=0.9
T=1000
p_list = np.arange(0.1,0.71,0.1)
mu = 0.1500
trials_list = list(range(10000))

##W = np.zeros(len(p_list))
##B = np.zeros(len(p_list))
##for i,p in enumerate(p_list):
##    hx_w = []
##    hx_b = []
##    count = 0
##    for trial in trials_list:
##        if trial % 500 == 0:
##            print(p,trial)
##        
##        efile = "../data-Nov13/edge/N%i_p%0.3f_mu%0.4f_q%0.2f_T%i_sim%i.txt" % (N,p,mu,q,T,trial)
##        try:
##            edata = pd.read_csv(efile, sep = " ")
##        except:
##            print("No data", p,mu,trial)
##
##        else:
##            count += 1
##            
##            block1 = list(range(0,int(N/2)))
##            block2 = list(range(int(N/2),N))
##
##            hx_w.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block1))].values)
##            hx_w.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block2))].values)
##            hx_b.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block2))].values)
##            hx_b.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block1))].values)
##
##    if count > 5000: # missing some data. Only compute <hx> for (p,mu) with 100+ trials
##        W[i] = np.mean(hx_w)
##        B[i] = np.mean(hx_b)
##
##
##df = pd.DataFrame(data={"p":p_list,"hx_w":W,"hx_b":B})
##df = df.to_csv("sbm_mu0.1500.csv", index=False)





# PLOT
data =  pd.read_csv("sbm_mu0.1500.csv")
plt.plot(data["p"],data["hx_w"],'C0-',label="within")
plt.plot(data["p"],data["hx_b"],'C0--',label="between")
plt.legend()
plt.xlabel(r"$p$")
plt.ylabel("Average cross-entropy")
plt.show()


