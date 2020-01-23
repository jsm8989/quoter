import numpy as np
import pandas as pd
import os

N = 200
k = 6
q = 0.9
T = 1000
p_list = np.arange(0, 1.01, 0.1)
trials_list = list(range(300))

hx_avg = np.zeros(len(p_list))
hx_var = np.zeros(len(p_list))
C_avg = np.zeros(len(p_list))
for i,p in enumerate(p_list):
    hx_trial = []
    C_trial = []
    for trial in trials_list:
        # change to "data_uniform" for uniform distribution vocabulary
        efile = "../data_clustering/edge/N%i_p%0.1f_q%0.1f_T%i_sim%i.txt" % (N,p,q,T,trial)
        gfile = "../data_clustering/graph/N%i_p%0.1f_q%0.1f_T%i_sim%i.txt" % (N,p,q,T,trial)

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

    print(p,"done")

df = pd.DataFrame(data={"p":p_list,"hx_avg":hx_avg,"hx_var":hx_var,"C":C_avg})
df.to_csv("small_world.csv", index=False)
