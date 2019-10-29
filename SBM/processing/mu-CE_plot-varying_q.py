import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import csv

N=600
q_list = np.arange(0,0.21,0.05)
T=1000
mu_list = np.arange(.05,.51,.05)
trials_list = list(range(300))

hx_w = np.zeros((len(q_list),len(mu_list))) # within block
hx_b = np.zeros((len(q_list),len(mu_list))) # between block
hx_all = np.zeros((len(q_list),len(mu_list)))
for i,q in enumerate(q_list):
    for j,mu in enumerate(mu_list):
        trial_avg_w = count_w = trial_avg_b = count_b = trial_avg_all = count_all = 0
        for trial in trials_list:
            efile = "../data_vary_q-new/N%i_mu%0.2f_q%0.2f_T%i_sim%i.txt" % (N,mu,q,T,trial)

            try:
                edata = pd.read_csv(efile, sep = " ")
                
                block1 = list(range(0,int(N/2)))
                block2 = list(range(int(N/2),N))

                egos = edata["ego"].values
                alters = edata["alter"].values
                hx_list = edata["hx"].values
                
                for ego,alter,hx in zip(egos,alters,hx_list):
                    if ego == 0:
                        pass
                    
                    #within block
                    elif ego in block1:
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
np.savetxt("sbm_seed_N600_vary_q_within.csv",hx_w,delimiter=",")
np.savetxt("sbm_seed_N600_vary_q_between.csv",hx_b,delimiter=",")
np.savetxt("sbm_seed_N600_vary_q_all.csv",hx_all,delimiter=",")



