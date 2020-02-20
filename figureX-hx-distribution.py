import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import stats
import bltools as blt # see baglab github

# This figure requires access to full data: stored in ./hx_distribution.zip

fig, ax = plt.subplots(1,3,figsize=(8,2.5), sharey=True)
##dir1 = "ER_BA_N1000"
##dir2 = "small_world"
dir1 = dir2 = "hx_distribution"

# ERBA plots ------
N = 1000
q = 0.5
T = 1000
trials_list = list(range(200))

##graph = "ER" # ER or BA
x=12 # average degree

for i,graph in enumerate(["ER","BA"]):
    hx_list = []
    pv = []

    # file naming format depends on whether ER or BA
    if graph == "ER":
        graph_name = "Erdős-Rényi"
        param_sym = "k"
    else:
        graph_name = "Barabási-Albert"
        param_sym = "m"
        x = int(x/2) # m = k/2

    trial_means = []
    trial_medns = []
    for trial in trials_list:
        #if trial % 40 == 0:
        #    print(trial, "done")


        efile = "%s/data_%s/edge/N%i_%s%i_q%0.1f_T%i_sim%i.txt" % (dir1,graph,N,param_sym,x,q,T,trial)

        if os.path.isfile(efile):
            edata = pd.read_csv(efile, sep = " ")

            hx_vals = edata["hx"].values
            trial_means.append(np.mean(hx_vals))
            trial_medns.append(np.median(hx_vals))
            hx_list.extend(hx_vals) # compile all hx
            pv.append(stats.normaltest(hx_vals)[1]) # store p-value of normality test for this trial

        else:
            print(trial, "no data")
    trial_means = np.array(trial_means)
    trial_medns = np.array(trial_medns)

    print("compiled hx p-val", stats.normaltest(hx_list)) # compile all hx from all trials -- are these normally distributed?
    print("kurtosis/skewness",stats.kurtosis(hx_list), stats.skew(hx_list))

    # Dont compile all hx. Instead count num trials which have normally distributed hx
    alpha_level = 0.05
    print(len([p for p in pv if p > alpha_level])/len(trials_list), "percent of trials have normaly distributed hx") 

    # Plot compiled hx distribution
    plt.sca(ax[i])
    plt.hist(hx_list, density=True, bins=75, histtype='stepfilled')
    plt.axvline(np.mean(hx_list),color="k",linestyle="-",label="mean")
    plt.axvline(np.median(hx_list),color="C6",linestyle="--",label="median")
    plt.xlabel(r"$h_\times$")
    #plt.ylabel("Count (in 200 trials x 1000 edges/trial)")
    if i==0:
        plt.ylabel("Prob. density")
        plt.legend(handlelength=1.0, loc='upper left')
    plt.title("%s" % graph_name, fontsize=10)




# Small world plot ------------------
##N_list = [200,400] # number of nodes
##k_list = [6,12] # degree

plt.sca(ax[2])

q = 0.5
T = 1000
p_list = np.logspace(-4,0,8) # rewiring 
trials_list = list(range(500))

# let's just study one combination of (N,k,p)
N = 200
k = 6
p = p_list[0]

hx_list = []
pv = []
for trial in trials_list:
    #if trial % 50 == 0:
    #    print(trial, "done")

    efile = "%s/data_clustering2/edge/N%i_k%i_p%0.4f_q%0.1f_T%i_sim%i.txt" % (dir2,N,k,p,q,T,trial)

    if os.path.isfile(efile):
        edata = pd.read_csv(efile, sep=" ")


        hx_vals = edata["hx"].values

        hx_list.extend(hx_vals) # compile all hx
        pv.append(stats.normaltest(hx_vals)[1]) # store p-value of normality test for this trial

    else:
        print(trial, "no data")

print("compiled hx p-val", stats.normaltest(hx_list)) # compile all hx from all trials -- are these normally distributed?
print("kurtosis/skewness",stats.kurtosis(hx_list), stats.skew(hx_list))

# Dont compile all hx. Instead count num trials which have normally distributed hx
print(len([p for p in pv if p > alpha_level])/len(trials_list), "percent of trials have normaly distributed hx\n")

# Plot compiled hx distribution
plt.hist(hx_list, density=True, bins=75, histtype='stepfilled')
plt.axvline(np.mean(hx_list), color="k", linestyle="-")
plt.axvline(np.median(hx_list), color="C6", linestyle="--")
plt.xlabel(r"$h_\times$")
##plt.ylabel("Count (in 500 trials x 500 edges/trial)")
plt.title("Small-World", fontsize=10)

blt.letter_subplots(axes=ax.flatten(), xoffset=-.05, yoffset=1.05)
plt.tight_layout(h_pad=0.0, w_pad=0)
plt.savefig("figureX-hx-distribution.pdf")
# plt.show()

