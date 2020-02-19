import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from scipy.stats import stats

##N_list = [200,400] # number of nodes
##k_list = [6,12] # degree

q = 0.5
T = 1000
p_list = np.logspace(-4,0,8) # rewiring 
trials_list = list(range(500))

# let's just study one combination of (N,k,p)
N = 200
k = 6
p = p_list[0]
print(p)

hx_list = []
pv = []
for trial in trials_list:
    if trial % 50 == 0:
        print(trial, "done")
        
    efile = "../data_clustering2/edge/N%i_k%i_p%0.4f_q%0.1f_T%i_sim%i.txt" % (N,k,p,q,T,trial)

    if os.path.isfile(efile):
        edata = pd.read_csv(efile, sep=" ")


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
plt.ylabel("Count (in 500 trials x 500 edges/trial)")
plt.title(r"Histogram of $h_\times$ in SW networks: $N=%i$, $k = %i$" % (N,k))
plt.show()

