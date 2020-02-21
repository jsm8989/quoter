import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import stats
import bltools as blt # see baglab github

# This figure requires access to full data: stored in ./hx_distribution.zip

a = 1.2
fig, ax = plt.subplots(2,7,figsize=(8*a,2.5*a), sharey=True)
ax = ax.flatten()
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
        param_sym = "k"
##        title = "Erdős-Rényi"

    else:
        param_sym = "m"
        x = int(x/2) # m = k/2
##        title = "Barabási-Albert"

    title = graph # shortened to ER & BA

    trial_means = []
    trial_medns = []
    for trial in trials_list:
##        if trial % 40 == 0:
##            print(trial, "done")

        
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

    print("compiled hx p-val", stats.normaltest(hx_list)[1]) # compile all hx from all trials -- are these normally distributed?
    print("kurtosis/skewness", stats.kurtosis(hx_list), stats.skew(hx_list))

    # Dont compile all hx. Instead count num trials which have normally distributed hx
    alpha_level = 0.05
    print(len([p for p in pv if p > alpha_level])/len(trials_list), "percent of trials have normaly distributed hx") 

    # Plot compiled hx distribution
    plt.sca(ax[i])
    plt.hist(hx_list, density=True, bins=75, histtype='stepfilled')
    plt.axvline(np.mean(hx_list),color="k",linestyle="-",label="mean")
    plt.axvline(np.median(hx_list),color="r",linestyle="--",label="median")
    
    plt.title("%s" %  title, fontsize=10)


### Small world plot ------------------
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
plt.axvline(np.median(hx_list), color="r", linestyle="--")
plt.xlabel(r"$h_\times$")
plt.title("SW", fontsize=10)



# Real networks -----------
q = 0.5
T = 1000
trials_list = list(range(300))

##small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
##              "Golden Age", "Kapferer tailor", "Les Miserables",
##              "Hollywood music", "Sampson's monastery", "Terrorist"]

# sorted by size
small_networks = ["Sampson's monastery", "Freeman's EIES", "Kapferer tailor",
                  "Hollywood music", "Golden Age", "Dolphins", "Terrorist",
                  "Les Miserables", "CKM physicians", "Email Spain"]

##datadir = "real_networks/data_separate_link-nonlink/data"
datadir = "hx_distribution/data"
for i,name in enumerate(small_networks):
    print(name)
    
    hx_list = []
    for trial in trials_list:
        network_dir = os.path.join(datadir, name)
        efile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
        edata = pd.read_csv(os.path.join(network_dir,efile), sep = " ")

        edata = edata.loc[edata["distance"]==1]
        
        hx_vals = edata["hx"].values
        hx_list.extend(hx_vals)

    plt.sca(ax[i+3])
    plt.hist(hx_list, density=True, bins=75,histtype='stepfilled')
    plt.axvline(np.mean(hx_list),color="k",linestyle="-",label="mean")
    plt.axvline(np.median(hx_list),color="r",linestyle="--",label="median")

    if name != "Les Miserables":
        title = name.split()[0]
    else:
        title = "Les Mis"
    plt.title("%s" %  title, fontsize=10)


for i in range(len(ax)):
    for tick in ax[i].xaxis.get_major_ticks():
        tick.label.set_fontsize(9)

    for tick in ax[i].yaxis.get_major_ticks():
        tick.label.set_fontsize(9)

    plt.sca(ax[i])
    if i in [-1,-2,-3,-4,-5,-6,-7]:
        plt.xlabel(r"$h_\times$")

    if i in [0,7]:
        plt.ylabel("Prob. density")
        
##    if i == 0:
##        plt.legend(handlelength=1.0, loc='upper left')

ax[-1].axis('off')



##blt.letter_subplots(axes=ax.flatten(), xoffset=-.05, yoffset=1.05)
plt.tight_layout(h_pad=0.2, w_pad=0)
plt.savefig("figureX-hx-distribution.pdf")
##plt.show()

