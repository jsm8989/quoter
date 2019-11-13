import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N=2000
M=10000
q_list=[0.5,0.1,0.9]
T=1000
p = 0.01
mu_list = np.linspace(p/10, p, 10)
trials_list = list(range(300))

##for q in [q_list[0]]:
##    hx_w_avg = []
##    hx_b_avg = []
##    for i,mu in enumerate(mu_list):
##        hx_w_this_mu = []
##        hx_b_this_mu = []
##        for trial in trials_list:
##            if trial % 50 == 0:
##                print(i,trial)
##            
##            efile = "../data_sbm-p-mu/N%i_p%0.3f_mu%0.4f_q%0.2f_T%i_sim%i.txt" % (N,p,mu,q,T,trial)
##
##            edata = pd.read_csv(efile, sep = " ")
##
##            block1 = list(range(0,int(N/2)))
##            block2 = list(range(int(N/2),N))
##
##            edata = edata.loc[edata["distance"] == 1] # links only
##
##            hx_w_this_mu.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block1))])
##            hx_w_this_mu.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block2))])
##            hx_b_this_mu.extend(edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block2))])
##            hx_b_this_mu.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block1))])
##
##        hx_w_avg.append(np.mean(hx_w_this_mu))
##        hx_b_avg.append(np.mean(hx_b_this_mu))
##        
##    df = pd.DataFrame({"mu":mu_list,
##                       "hx_w":hx_w_avg,
##                       "hx_b":hx_b_avg})
##    df = df.to_csv("sbm_p%0.3f_q%0.2f_links.csv" % (p,q), index=False)


##data0 =  pd.read_csv("sbm_p%0.3f_q0.10.csv" % p)
data1 =  pd.read_csv("sbm_p%0.3f_q0.50_links.csv" % p)
##data2 =  pd.read_csv("sbm_p%0.3f_q0.90.csv" % p)

plt.plot(data1["mu"],data1["hx_w"],label="within")
plt.plot(data1["mu"],data1["hx_b"],label="between")
plt.legend()
plt.xlabel(r"$\mu$")
plt.ylabel("Cross-entropy")
plt.show()


