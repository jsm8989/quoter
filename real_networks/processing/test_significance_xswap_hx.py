import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats


small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]

q = 0.9
T = 1000
trials_list = list(range(300))

for i,name in enumerate(small_networks):
    hx_orig = []
    hx_swap = []
    for trial in trials_list:
        efile_swap = "../data-NEW/data_xswap-5x/%s/edge_%s_q%0.1f_T%i_sim%i.txt" % (name,name,q,T,trial)
        edata_swap = pd.read_csv(efile_swap, sep = " ")
        hx_swap.extend(edata_swap["hx"].values)

        efile_orig = "../data-NEW/data/%s/%s_q%0.1f_T%i_sim%i.txt" % (name,name,q,T,trial)
        edata_orig = pd.read_csv(efile_orig, sep = " ")
        hx_orig.extend(edata_orig["hx"].values)

    u,p = scipy.stats.mannwhitneyu(hx_orig,hx_swap)
    print(name, np.mean(hx_orig) - np.mean(hx_swap), p)

    
        
