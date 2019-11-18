import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N = 1000
m = N//2 
q=0.5
T=1000
p = 0.4
mu_seq = [0.0444, 0.0570857, 0.0705176, 0.0847636, 0.0999,
              0.116013, 0.1332, 0.151572, 0.171257, 0.1924, 0.215169,
              0.23976, 0.2664, 0.295357, 0.326945, 0.361543, 0.3996]
trials_list = list(range(1000))

##W = np.zeros(len(mu_seq))
##B = np.zeros(len(mu_seq))
##for i,mu in enumerate(mu_seq):
##    hx_w = []
##    hx_b = []
##    print(i)
##    for trial in trials_list:
##        
##        efile = "../data-Nov16/edge/N%i_p%0.2f_mu%0.4f_q%0.2f_T%i_sim%i.txt" % (N,p,mu,q,T,trial)
##        try:
##            edata = pd.read_csv(efile, sep = " ")
##        except:
##            print("No data", p,mu,trial)
##
##        else:
##            
##            hx_w.extend(edata["hx"].loc[edata["ego"]==1].values)
##            hx_b.extend(edata["hx"].loc[edata["ego"]==m].values)
####            block1 = list(range(0,int(N/2)))
####            block2 = list(range(int(N/2),N))
##
####            hx_w.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block1))].values)
####            hx_w.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block2))].values)
####            hx_b.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block2))].values)
####            hx_b.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block1))].values)
##
##    W[i] = np.mean(hx_w)
##    B[i] = np.mean(hx_b)
##
##df = pd.DataFrame({"mu":mu_seq,"hx_w":W,"hx_b":B})
##df = df.to_csv("sbm_q%0.2f.csv" % q, index=False)




## PLOT
data =  pd.read_csv("sbm_q%0.2f.csv" % q)
print(data)
plt.plot(data["mu"],data["hx_w"],label="within")
plt.plot(data["mu"],data["hx_b"],label="between")
plt.legend()
plt.xlabel(r"$\mu$")
plt.ylabel("Average cross-entropy")
plt.show()


