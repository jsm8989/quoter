import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N = 2000
M = 10000
q = 0.9
T = 1000
##trials_list = list(range(300))
trials_list = list(range(150))
mu_list = np.arange(0.05,0.51,0.05)
alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5),(1.5,2.0),(2.5,2.0)]
W = np.zeros(len(mu_list))
B = np.zeros(len(mu_list))
AA = np.zeros(len(mu_list))
AB = np.zeros(len(mu_list))
BA = np.zeros(len(mu_list))
BB = np.zeros(len(mu_list))

##for alpha in alpha_list:
##    alpha_A = alpha[0]
##    alpha_B = alpha[1]
##    for j,mu in enumerate(mu_list):
##        hx_AA, hx_AB, hx_BA, hx_BB = [], [], [], []
##        print(j)
##        for trial in trials_list:
##            efile = "../data-Dec2/edge/N%i_mu%0.2f_M%iaA%0.1f_aB_%0.1f_q%0.1f_T%i_sim%i.txt" % (N,mu,M,alpha_A,alpha_B,q,T,trial)
##            try:
##                edata = pd.read_csv(efile, sep = " ")
##            except:
##                print("No data",mu,trial)
##
##            else:
##                
##                block1 = list(range(0,int(N/2)))
##                block2 = list(range(int(N/2),N))
##
##                data_AA = edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block1))].values
##                data_BB = edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block2))].values
##                data_AB = edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block2))].values
##                data_BA = edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block1))].values
##                hx_AA.extend(data_AA)
##                hx_BB.extend(data_BB)
##                hx_AB.extend(data_AB)
##                hx_BA.extend(data_BA)
##
##        W[j] = np.mean(hx_AA+hx_BB)
##        B[j] = np.mean(hx_AB+hx_BA)
##        AA[j] = np.mean(hx_AA)
##        BB[j] = np.mean(hx_BB)
##        AB[j] = np.mean(hx_AB)
##        BA[j] = np.mean(hx_BA)
##        
##
##    df = pd.DataFrame(data={"mu":mu_list,"hx_w":W,"hx_b":B,
##                            "AA":AA,"BB":BB,"AB":AB,"BA":BA})
##    df = df.to_csv("sbm_aA%0.1f_aB%0.1f.csv" % (alpha_A,alpha_B), index=False)


# PLOT 1
##alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5)]
##fig, ax = plt.subplots(1,3,figsize=(10,6),sharey=False)
##for i,alpha in enumerate(alpha_list):
##    plt.sca(ax.flatten()[i])
##    alpha_A = alpha[0]
##    alpha_B = alpha[1]
##    data =  pd.read_csv("sbm_aA%0.1f_aB%0.1f.csv" % (alpha_A,alpha_B))
##    plt.plot(data["mu"],data["AB"],'o-',label=r"$h_\times(A|B)$") # these are reversed oops
##    plt.plot(data["mu"],data["BA"],'o-',label=r"$h_\times(B|A)$") # ...
##    plt.plot(data["mu"],data["AA"],'o-',label=r"$h_\times(A|A)$")
##    plt.plot(data["mu"],data["BB"],'o-',label=r"$h_\times(B|B)$")
##    plt.plot(data["mu"],data["hx_w"],'o-',label="within")
##    plt.plot(data["mu"],data["hx_b"],'o-',label="between")
##    plt.title(r"$\alpha_A = %0.1f, \alpha_B = %0.1f$" %(alpha_A,alpha_B))
##    plt.xlabel(r"$\mu$")
##    if i == 0:
##        plt.legend()
##        plt.ylabel("Average cross-entropy")
##
##plt.tight_layout()
##plt.show()

# PLOT 2
alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5)]
style = ['C0-','C1-','C2-']
for i,alpha in enumerate(alpha_list):
    alpha_A = alpha[0]
    alpha_B = alpha[1]
    data =  pd.read_csv("sbm_aA%0.1f_aB%0.1f.csv" % (alpha_A,alpha_B))
    plt.plot(data["mu"],data["hx_w"].values,style[i],label=r"$\alpha_B = %0.1f$" %alpha_B)
    plt.plot(data["mu"],data["hx_b"].values,style[i]+'-')
    plt.title(r"$\alpha_A = 2.0$")
    plt.legend()
    plt.xlabel(r"$\mu$")
    plt.ylabel("Average cross-entropy")
plt.show()



