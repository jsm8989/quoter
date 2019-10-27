import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

N = 100
q_list = np.arange(0,0.21, 0.05)
T = 1000
trials_list = list(range(300))
mu_list = np.arange(0.05,0.51,0.05)
##seeds = range(10)

hx_w = np.zeros((len(q_list),len(mu_list))) # within block
hx_b = np.zeros((len(q_list),len(mu_list))) # between block
hx_all = np.zeros((len(q_list),len(mu_list)))
for i,q in enumerate(q_list):
    for j,mu in enumerate(mu_list):
        trial_avg_w = count_w = trial_avg_b = count_b = trial_avg_all = count_all = 0
        for trial in trials_list:
            efile = "../data_vary_q-multiseed/N%i_mu%0.2f_q%0.2f_T%i_sim%i.txt" % (N,mu,q,T,trial)

            try:
                edata = pd.read_csv(efile, sep = " ")
                
                block1 = list(range(0,int(N/2)))
                block2 = list(range(int(N/2),N))

                egos = edata["ego"].values
                alters = edata["alter"].values
                hx_list = edata["hx"].values
                
                for ego,alter,hx in zip(egos,alters,hx_list):
                    #within block
                    if ego in block1:
                        trial_avg_w += hx
                        count_w += 1
                        
                    else: # between block
                        trial_avg_b += hx
                        count_b += 1
                        

                    trial_avg_all += hx
                    count_all += 1

            except: # no data
                pass

        print(i,j)
        hx_w[i,j] = trial_avg_w/count_w
        hx_b[i,j] = trial_avg_b/count_b
        hx_all[i,j] = trial_avg_all/count_all

# write data
np.savetxt("sbm_seed_N100_vary_q-multi_within.csv",hx_w,delimiter=",")
np.savetxt("sbm_seed_N100_vary_q-multi_between.csv",hx_b,delimiter=",")
np.savetxt("sbm_seed_N100_vary_q-multi_all.csv",hx_all,delimiter=",")

        
##data_qlow = pd.read_csv("sbm_seed_N600_q0.05_tri300.csv")
##data_qmed = pd.read_csv("sbm_seed_N600_q0.05_tri600.csv")
##data_qhigh = pd.read_csv("sbm_seed_N600_q0.05_tri1200.csv")
####plt.plot(data["mu"],data["hx_all"])
##
##fig = plt.figure(figsize=(10,3))
##
##plt.subplot(1,3,1)
##plt.plot(data_qlow["mu"],data_qlow["hx_w"],label=r"hx($i|A$)")
##plt.plot(data_qlow["mu"],data_qlow["hx_b"],label=r"hx($i|B$)")
##plt.xlabel(r"$\mu$")
##plt.ylabel("Mean cross-entropy")
##plt.legend()
##plt.title(r"300 trials")
##
##plt.subplot(1,3,2)
##plt.plot(data_qmed["mu"],data_qmed["hx_w"],label=r"hx($i|A$)")
##plt.plot(data_qmed["mu"],data_qmed["hx_b"],label=r"hx($i|B$)")
##plt.xlabel(r"$\mu$")
##plt.ylabel("Mean cross-entropy")
##plt.legend()
##plt.title(r"600 trials")
##
##plt.subplot(1,3,3)
##plt.plot(data_qhigh["mu"],data_qhigh["hx_w"],label=r"hx($i|A$)")
##plt.plot(data_qhigh["mu"],data_qhigh["hx_b"],label=r"hx($i|B$)")
##plt.xlabel(r"$\mu$")
##plt.ylabel("Mean cross-entropy")
##plt.legend()
##plt.title(r"1200 trials")
##
##
##plt.tight_layout()
##plt.show()



