import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.stats import stats

# Parameters for simulation, used in loading in files
N = 1000
q = 0.5
T = 1000
trials_list = list(range(200))

graph = "ER" # ER or BA
x=10 # average degree

hx_list = []
pv = []
for trial in trials_list:
    if trial % 40 == 0:
        print(trial, "done")

    # file naming format depends on whether ER or BA
    if graph == "ER":
        param_sym = "k"
    else:
        param_sym = "m"
    
    efile = "../data_%s/edge/N%i_%s%i_q%0.1f_T%i_sim%i.txt" % (graph,N,param_sym,x,q,T,trial)
    
    if os.path.isfile(efile):
        edata = pd.read_csv(efile, sep = " ")

        hx_vals = edata["hx"].values

        hx_list.extend(hx_vals) # compile all hx
        pv.append(stats.normaltest(hx_vals)[1]) # store p-value of normality test for this trial

    else:
        print(trial, "no data")

print("compiled hx p-val", stats.normaltest(hx_list)) # compile all hx from all trials -- are these normally distributed?

# Dont compile all hx. Instead count num trials which have normally distributed hx
print(len([p for p in pv if p > .05])/len(trials_list), "percent of trials have normaly distributed hx") 

# Plot compiled hx distribution
plt.hist(hx_list, bins=100)
plt.xlabel(r"$h_\times$")
plt.ylabel("Count (in 200 trials x 1000 edges/trial)")
plt.title(r"Histogram of $h_\times$ in ER networks: $N=1000$, $\langle k \rangle = 10$")
plt.show()

    


