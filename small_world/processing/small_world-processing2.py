import numpy as np
import pandas as pd
import os

N_list = [200,400]
k_list = [6,12]
q = 0.9
T = 1000

p_list = np.logspace(-4,0,8)
trials_list = list(range(500))

hx_avg = np.zeros(len(p_list))
hx_var = np.zeros(len(p_list))
C_avg = np.zeros(len(p_list))
for N in N_list:
    for k in k_list:
        for i,p in enumerate(p_list):
            hx_trial = []
            C_trial = []
            for trial in trials_list:
                efile = "../data_clustering2/edge/N%i_k%i_p%0.4f_q%0.1f_T%i_sim%i.txt" % (N,k,p,q,T,trial)
                gfile = "../data_clustering2/graph/N%i_k%i_p%0.4f_q%0.1f_T%i_sim%i.txt" % (N,k,p,q,T,trial)

                try:
                    edata = pd.read_csv(efile, sep=" ")
                    gdata = pd.read_csv(gfile, sep=" ")
                except:
                    print("no data",p,trial)

                else:
                    hx_trial.extend(edata["hx"].values)
                    C_trial.extend(gdata["transitivity"].values)

            hx_avg[i] = np.mean(hx_trial)
            hx_var[i] = np.var(hx_trial)
            C_avg[i] = np.mean(C_trial)

            print(N,k,p,"done")

        df = pd.DataFrame(data={"p":p_list,"hx_avg":hx_avg,"hx_var":hx_var,"C":C_avg})
        df.to_csv("small_world_N%i_k%i.csv" % (N,k), index=False)
