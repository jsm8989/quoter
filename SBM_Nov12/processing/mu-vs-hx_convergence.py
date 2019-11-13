import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys


N = 2000
M = 10000
q = 0.5
T = 2000
trials_list = list(range(300))
mu_list = np.arange(0.1,0.51,0.1)
times_list = np.array([100,200,300,400,500,1000,1500,2000])*N
dist_list = range(1,6)

block1 = list(range(0,int(N/2)))
block2 = list(range(int(N/2),N))

##mu = 0.5 # look at one mu for now
##avg_hx_w = np.zeros((len(times_list),len(dist_list)))
##avg_hx_b = np.zeros((len(times_list),len(dist_list)))
##count_w = np.zeros((len(times_list),len(dist_list)))
##count_b = np.zeros((len(times_list),len(dist_list)))
##for trial in trials_list:
##    efile = "../data_convergence/N%i_mu%0.2f_M%i_q%0.2f_T%i_sim%i.txt" % (N,mu,M,q,T,trial)
##    data = pd.read_csv(efile, sep = " ")
##    for i,t in enumerate(times_list):
##        data_t = data.loc[data["time"] == t]
##        for j,d in enumerate(dist_list):
##            hx_w = data_t["hx"].loc[(data_t["ego"].isin(block1)) & (data_t["distance"] == d)].values
##            hx_b = data_t["hx"].loc[(data_t["ego"].isin(block2)) & (data_t["distance"] == d)].values
##            avg_hx_w[i,j] += np.sum(np.power(hx_w,2))
##            avg_hx_b[i,j] += np.sum(np.power(hx_b,2))
##            count_w[i,j] += len(hx_w)
##            count_b[i,j] += len(hx_b)
##    print(trial)
##    
##avg_hx_w = np.divide(avg_hx_w, count_w)
##avg_hx_b = np.divide(avg_hx_b, count_b)
##
##df_w = pd.DataFrame(data=avg_hx_w)
##df_b = pd.DataFrame(data=avg_hx_b)
##df_w = df_w.to_csv("sbm_conv_q%0.2f_mu%0.2f_W-var.csv" % (q,mu), index=False)
##df_b = df_b.to_csv("sbm_conv_q%0.2f_mu%0.2f_B-var.csv" % (q,mu), index=False)


# PLOT
mu = 0.1
df_w = pd.read_csv("sbm_conv_q%0.2f_mu%0.2f_W.csv" % (q,mu))
df_b = pd.read_csv("sbm_conv_q%0.2f_mu%0.2f_B.csv" % (q,mu))
df_w2 = pd.read_csv("sbm_conv_q%0.2f_mu%0.2f_W-var.csv" % (q,mu))
df_b2 = pd.read_csv("sbm_conv_q%0.2f_mu%0.2f_B-var.csv" % (q,mu))
df_w = df_w.values
df_b = df_b.values
df_w_sd = np.sqrt(df_w2.values - np.power(df_w,2))
df_b_sd = np.sqrt(df_b2.values - np.power(df_b,2))

for j,d in enumerate(dist_list):
    yerr = df_w_sd
    plt.errorbar(times_list/N,df_w[:,j],yerr[:,j],label=r"$d = %i$" % d, capsize=10, elinewidth=0.5, markeredgewidth=2)
plt.legend()
plt.xlabel("Time")
plt.ylabel("Average cross-entropy")
plt.show()


for i,t in enumerate(times_list):
    yerr = df_w_sd
    plt.errorbar(dist_list,df_w[i,:],yerr[i,:],label=r"$t = %i$" % int(t/N), capsize=10, elinewidth=0.5, markeredgewidth=2)
plt.legend()
plt.xlabel("Distance")
plt.xticks(dist_list)
plt.ylabel("Average cross-entropy")
plt.show()



           

