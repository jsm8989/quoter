import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


N = 200
T = 1000
alpha = hub_alpha = 1.5
k = 8
q_list = np.arange(0,1.01,0.1)
trials_list = list(range(200))

##hx_avg_ordered = np.zeros(len(q_list))
##hx_avg_shuffled = np.zeros(len(q_list))
##for i,q in enumerate(q_list):
##    print(q)
##    hx_ordered_trial, hx_shuffled_trial = [], []
##    for trial in trials_list:
##        efile = "../data_ER/edge/N%i_k%i_A%0.1f_HA%0.1f_q%0.1f_T%i_sim%i.txt" % (N,k,alpha,hub_alpha,q,T,trial)
##        try:
##            edata = pd.read_csv(efile, sep = " ")
##        except:
##            print("no data", q)
##        else:
##            hx_ordered_trial.extend(edata["hx"].values)
##            hx_shuffled_trial.extend(edata["hx_both"].values)
##
##    hx_avg_ordered[i] = np.mean(hx_ordered_trial)
##    hx_avg_shuffled[i] = np.mean(hx_shuffled_trial)
##
##df = pd.DataFrame({"q":q_list,"hx_ordered":hx_avg_ordered,"hx_shuffled":hx_avg_shuffled})
##df.to_csv("hx_ER_vary_q.csv", index=False)
    

data = pd.read_csv("hx_ER_vary_q.csv")
plt.plot(data["q"].values,data["hx_ordered"].values,label="ordered")
plt.plot(data["q"].values,data["hx_shuffled"].values,label="shuffled")
plt.legend()
plt.xlabel(r"$q$")
plt.ylabel(r"$\langle h_\times \rangle$")
plt.show()

            
