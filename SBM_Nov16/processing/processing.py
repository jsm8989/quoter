import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N = 1000
m = N//2 
q=0.9
T=1000
p = 0.4
mu_seq = [0.0444, 0.0570857, 0.0705176, 0.0847636, 0.0999,
              0.116013, 0.1332, 0.151572, 0.171257, 0.1924, 0.215169,
              0.23976, 0.2664, 0.295357, 0.326945, 0.361543, 0.3996]
##trials_list = list(range(1000))
trials_list = list(range(500))

##W_avg = np.zeros(len(mu_seq))
##B_avg = np.zeros(len(mu_seq))
##W_var = np.zeros(len(mu_seq))
##B_var = np.zeros(len(mu_seq))
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
##    W_avg[i] = np.mean(hx_w)
##    B_avg[i] = np.mean(hx_b)
##    W_var[i] = np.var(hx_w)
##    B_var[i] = np.var(hx_b)
##    
##df = pd.DataFrame({"mu":mu_seq,"hx_w_avg":W_avg,"hx_b_avg":B_avg,
##                   "hx_w_var":W_var,"hx_b_var":B_var})
##df = df.to_csv("sbm_q%0.2f.csv" % q, index=False)




## PLOT
data =  pd.read_csv("sbm_q%0.2f.csv" % q)
print(data)
mod_list = np.arange(0,0.41,0.025)
##plt.plot(data["mu"],data["hx_w_var"],label="within")
##plt.plot(data["mu"],data["hx_b_var"],label="between")
plt.plot(mod_list,data["hx_w_var"],label="within")
plt.plot(mod_list,data["hx_b_var"],label="between")
plt.legend()
plt.xlabel(r"Modularity, $Q$")
plt.ylabel("Variance of cross-entropy")
plt.show()


