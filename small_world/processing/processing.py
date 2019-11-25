import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

N = 200
k = 6
q = 0.9
T = 1000
p_list = np.arange(0, 1.01, 0.1)
trials_list = list(range(300))

# CLUSTERING VS HX
##hx_avg = np.zeros(len(p_list))
##hx_var = np.zeros(len(p_list))
##C_avg = np.zeros(len(p_list))
##for i,p in enumerate(p_list):
##    hx_trial = []
##    C_trial = []
##    for trial in trials_list:
##        efile = "../data_clustering/edge/N%i_p%0.1f_q%0.1f_T%i_sim%i.txt" % (N,p,q,T,trial)
##        gfile = "../data_clustering/graph/N%i_p%0.1f_q%0.1f_T%i_sim%i.txt" % (N,p,q,T,trial)
##
##        try:
##            edata = pd.read_csv(efile, sep=" ")
##            gdata = pd.read_csv(gfile, sep=" ")
##        except:
##            print("no data",p,trial)
##
##        else:
##            hx_trial.extend(edata["hx"].values)
##            C_trial.extend(gdata["transitivity"].values)
##
##    hx_avg[i] = np.mean(hx_trial)
##    hx_var[i] = np.var(hx_trial)
##    C_avg[i] = np.mean(C_trial)
##
##    print(p,"done")
##
##df = pd.DataFrame(data={"p":p_list,"hx_avg":hx_avg,"hx_var":hx_var,"C":C_avg})
##df = df.to_csv("small_world_q%0.1f.csv" % q, index=False)
##
##
### PLOT: clustering vs hx
##data = pd.read_csv("small_world_q%0.1f.csv" % q)
####plt.plot(data["p"],data["hx_avg"],'o-')
##plt.errorbar(data["C"],data["hx_avg"],data["hx_var"])
##plt.xlabel("Transitivity")
####plt.xlabel(r"Rewiring probability, $\beta$")
##plt.ylabel("Average cross-entropy")
##plt.show()


# DISTANCE VS HX (in ring lattice)
##d_list = range(1,21)
##hx_avg = np.zeros(len(d_list))
##hx_var = np.zeros(len(d_list))
##p = 0
##hx_trial = [ [None] for _ in range(len(d_list)) ]
##for trial in trials_list:
##    efile = "../data_clustering/edge/N%i_p%0.1f_q%0.1f_T%i_sim%i.txt" % (N,p,q,T,trial)
##
##    try:
##        edata = pd.read_csv(efile, sep=" ")
##    except:
##        print("no data",p,trial)
##
##    else:
##        for i,d in enumerate(d_list):
##            hx_trial[i].extend(edata["hx"].loc[edata["distance"]==d].values)
##
##
##for i,d in enumerate(d_list):
##    print(len(hx_trial[i]))
##    hx_avg[i] = np.mean(hx_trial[i][1:])
##    hx_var[i] = np.var(hx_trial[i][1:])
##
##
##df = pd.DataFrame(data={"d":d_list,"hx_avg":hx_avg,"hx_var":hx_var})
##df = df.to_csv("small_world_Dist_q%0.1f.csv" % q, index=False)


# PLOT distance vs hx
data = pd.read_csv("small_world_Dist_q%0.1f.csv" % q)
plt.plot(data["d"],data["hx_avg"],'C0o-')
plt.errorbar(data["d"],data["hx_avg"],data["hx_var"])
plt.xlabel("Distance")
plt.ylabel("Average cross-entropy")
plt.show()



