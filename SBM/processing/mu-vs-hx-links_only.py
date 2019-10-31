import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N=2000
M=10000
q_list=[0.5,0.1,0.9]
T=1000
mu_list = np.arange(.05,.51,.05)
trials_list = list(range(300))


##for q in q_list:
##    hx_w_avg = []
##    hx_b_avg = []
##    for i,mu in enumerate(mu_list):
##        hx_w_this_mu = []
##        hx_b_this_mu = []
##        for trial in trials_list:
##            efile = "../data_links/N%i_mu%0.2f_M%i_q%0.2f_T%i_sim%i.txt" % (N,mu,M,q,T,trial)
##
##            try:
##                df = pd.read_csv(efile, sep = " ")
##            except FileNotFoundError:
##                print("no data",q,mu,trial)
##            else:
##                block1 = list(range(0,int(N/2)))
##                block2 = list(range(int(N/2),N))
##
####                data = df[["alter","ego","hx"]].values
####                for alter,ego,hx in data:
####                    if (alter in block1 and ego in block1) or (alter in block2 and ego in block2):
####                        hx_w_this_mu.append(hx)
####                    else:
####                        hx_b_this_mu.append(hx)
##
##                hx_w_this_mu.extend(df["hx"].loc[(df["ego"].isin(block1)) & (df["alter"].isin(block1))])
##                hx_w_this_mu.extend(df["hx"].loc[(df["ego"].isin(block2)) & (df["alter"].isin(block2))])
##                hx_b_this_mu.extend(df["hx"].loc[(df["ego"].isin(block1)) & (df["alter"].isin(block2))])
##                hx_b_this_mu.extend(df["hx"].loc[(df["ego"].isin(block2)) & (df["alter"].isin(block1))])
##            if trial % 50 == 0:
##                print(mu,trial)
##        hx_w_avg.append(np.mean(hx_w_this_mu))
##        hx_b_avg.append(np.mean(hx_b_this_mu))
##        
##    df = pd.DataFrame({"mu":mu_list,
##                       "hx_w":hx_w_avg,
##                       "hx_b":hx_b_avg})
##    df = df.to_csv("sbm_links-only_q%0.2f.csv" % q, index=False)

def SNR(m1,m2,n):
    """ Signal to noise ratio, computed elementwise 
        m1 = sample 1st moment (sample mean) .. can be np.array or pandas
        m2 = sample 2nd moment .. can be np.array or pandas
        n = number of observations .. can be np.array or pandas
    """
    try: # if passed in as pandas
        m1 = m1.values
        m2 = m2.values
        n = n.values
    except:
        pass
    var = m2-np.power(m1,2)
    sample_s = np.sqrt(np.multiply(np.divide(n,n-1),var)) #sqrt( (n/(n-1)) * var)
    return np.divide(m1,sample_s)
    

data1 = pd.read_csv("sbm_links-only_q0.10.csv")
data2 = pd.read_csv("sbm_links-only_q0.50.csv")
data3 = pd.read_csv("sbm_links-only_q0.90.csv")

fig = plt.figure(figsize=(10,3))

plt.subplot(1,3,1)
plt.plot(data1["mu"],data1["hx_w"],label=r"$h_x(A|i)$")
plt.plot(data1["mu"],data1["hx_b"],label=r"$h_x(B|i)$")
plt.xlabel(r"$\mu$")
plt.ylabel("Mean cross-entropy")
##plt.ylim([3.374,3.399])
##plt.ylim([3.287,3.37])
plt.legend()
plt.title(r"$q=0.1$")

plt.subplot(1,3,2)
plt.plot(data2["mu"],data2["hx_w"],label=r"$h_x(A|i)$")
plt.plot(data2["mu"],data2["hx_b"],label=r"$h_x(B|i)$")
plt.xlabel(r"$\mu$")
plt.ylabel("Mean cross-entropy")
##plt.ylim([3.374,3.399])
##plt.ylim([3.287,3.37])
plt.legend()
plt.title(r"$q=0.5$")

plt.subplot(1,3,3)
plt.plot(data3["mu"],data3["hx_w"],label=r"$h_x(A|i)$")
plt.plot(data3["mu"],data3["hx_b"],label=r"$h_x(B|i)$")
plt.xlabel(r"$\mu$")
plt.ylabel("Mean cross-entropy")
##plt.ylim([3.374,3.399])
##plt.ylim([3.287,3.37])
plt.legend()
plt.title(r"$q=0.9$")

plt.tight_layout()
plt.show()



