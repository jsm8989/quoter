import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

# Parameters for simulation, used in loading in files
N = 1000
q = 0.5
T = 1000
trials_list = list(range(200))

graph = "ER" # ER or BA
x=10 # average degree

hx_list = []
for trial in trials_list:
    if trial % 40 == 0:
        print(trial, "done")

    # file naming format depends on whether ER or BA
    if graph == "ER":
        param_sym = "k"
    else:
        param_sym = "m"
    
    efile = "../data_%s/edge/N%i_%s%i_q%0.1f_T%i_sim%i.txt" % (graph,N,param_sym,x,q,T,trial)
    nfile = "../data_%s/node/N%i_%s%i_q%0.1f_T%i_sim%i.txt" % (graph,N,param_sym,x,q,T,trial)
    gfile = "../data_%s/graph/N%i_%s%i_q%0.1f_T%i_sim%i.txt" % (graph,N,param_sym,x,q,T,trial)
    
    if os.path.isfile(efile) and os.path.isfile(nfile) and os.path.isfile(gfile):
        edata = pd.read_csv(efile, sep = " ")
##        ndata = pd.read_csv(nfile, sep = " ")
##        gdata = pd.read_csv(gfile, sep = " ")

        hx_list.extend(edata["hx"].values)

plt.hist(hx_list, bins=100)
plt.xlabel(r"$h_\times$")
plt.ylabel("Count (in 200 trials x 1000 edges/trial)")
plt.title(r"Histogram of $h_\times$ in ER networks: $N=1000$, $\langle k \rangle = 10$")
plt.show()

    



