import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N = 2000
M = 10000
q = 0.9
T = 1000
trials_list = list(range(300))
mu_list = np.arange(0.05,0.51,0.05)

##W = np.zeros(len(mu_list))
##B = np.zeros(len(mu_list))
##AA = np.zeros(len(mu_list))
##AB = np.zeros(len(mu_list))
##BA = np.zeros(len(mu_list))
##BB = np.zeros(len(mu_list))
##for j,mu in enumerate(mu_list):
##    hx_AA, hx_AB, hx_BA, hx_BB = [], [], [], []
##    print(j)
##    for trial in trials_list:
##        efile = "../data/edge/N%i_mu%0.2f_M%i_q%0.1f_T%i_sim%i.txt" % (N,mu,M,q,T,trial)
##        try:
##            edata = pd.read_csv(efile, sep = " ")
##        except:
##            print("No data",mu,trial)
##
##        else:
##            
##            block1 = list(range(0,int(N/2)))
##            block2 = list(range(int(N/2),N))
##
##            data_AA = edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block1))].values
##            data_BB = edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block2))].values
##            data_AB = edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block2))].values
##            data_BA = edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block1))].values
##            hx_AA.extend(data_AA)
##            hx_BB.extend(data_BB)
##            hx_AB.extend(data_AB)
##            hx_BA.extend(data_BA)
##
##    W[j] = np.mean(hx_AA+hx_BB)
##    B[j] = np.mean(hx_AB+hx_BA)
##    AA[j] = np.mean(hx_AA)
##    BB[j] = np.mean(hx_BB)
##    AB[j] = np.mean(hx_AB)
##    BA[j] = np.mean(hx_BA)
##    
##
##df = pd.DataFrame(data={"mu":mu_list,"hx_w":W,"hx_b":B,
##                        "AA":AA,"BB":BB,"AB":AB,"BA":BA})
##df = df.to_csv("sbm_q%0.1f_Vocab.csv" % q, index=False)


# PLOT
data =  pd.read_csv("sbm_q%0.1f_Vocab.csv" % q)
plt.plot(data["mu"],data["AB"],'o-',label=r"$h_\times(A|B)$") # these are reversed oops
plt.plot(data["mu"],data["BA"],'o-',label=r"$h_\times(B|A)$") # ...
plt.plot(data["mu"],data["AA"],'o-',label=r"$h_\times(A|A)$")
plt.plot(data["mu"],data["BB"],'o-',label=r"$h_\times(B|B)$")
plt.plot(data["mu"],data["hx_w"],'o-',label="within")
plt.plot(data["mu"],data["hx_b"],'o-',label="between")
plt.legend()
plt.xlabel(r"$\mu$")
plt.ylabel("Average cross-entropy")
plt.show()



