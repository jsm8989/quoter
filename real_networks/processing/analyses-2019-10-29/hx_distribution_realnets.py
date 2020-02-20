from read_networks import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import os
import random
from scipy.stats import stats
import bltools as blt # see baglab github

networks_dict = {"Adolescent health": read_adolescent,
                "Arxiv CondMat": read_arxiv_CondMat,
                "Arxiv GrQc": read_arxiv_GrQc,
                "CKM physicians": read_ckm,
                "Dolphins": read_dolphins,
                "Email Spain": read_email,
                "Email Enron": read_enron,
                "Email Eu Core": read_Eu_Core,
                "Freeman's EIES": read_Freemans,
                "Golden Age": read_golden,
                "Hypertext": read_hypertext,
                "Kapferer tailor": read_kapf,
                "Les Miserables": read_lesmis,
                "Marvel": read_Marvel, 
                "Hollywood music": read_movies,
                "Network science": read_netscience,
                "NFL": read_NFL,
                "Intra-organizational": read_org,
                "Web of Trust": read_pgp,
                "Sampson's monastery": read_Sampson,
                "Terrorist": read_terrorist,
                "UC Irvine": read_UC_Irvine}

q = 0.5
T = 1000
trials_list = list(range(300))
small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]



# Process & plot histogram
fig, ax = plt.subplots(4,3, figsize=(8,6), sharey=True)
ax = ax.flatten()

datadir = "../../data_separate_link-nonlink/data"
##with open("histogram_data.csv", "w") as f:
##    f.write("name,n,bin\n")
    
for i,name in enumerate(small_networks):
    print(name)
    
    os.chdir("../")  
    G = read_any(name)
    os.chdir("analyses-2019-10-29")
    
    hx_list = []
    for trial in trials_list:
        outdir = os.path.join(datadir, name)
        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
        edata = pd.read_csv(os.path.join(outdir,outfile), sep = " ")

        edata = edata.loc[edata["distance"]==1]
        
        hx_vals = edata["hx"].values
        hx_list.extend(hx_vals)

    plt.sca(ax[i])
    plt.hist(hx_list, density=True, bins=100)

##    n,bins = np.histogram(hx_list, 100)
##    with open("histogram_data.csv", "a") as f:
##        f.write("".join(["%s,%0.8f,%0.8f\n" % (name,x,y) for x,y in zip(n,bins[:-1])]))
##        f.write("%s,%i,%0.8f\n" % (name,-555, bins[-1])) # bins has 1 more item than `n'
    

    plt.axvline(np.mean(hx_list),color="k",linestyle="-",label="mean")
    plt.axvline(np.median(hx_list),color="C6",linestyle="--",label="median")
    if i in [0,3,6,9]:
        plt.ylabel("Density")
        if i == 0:
            plt.legend()
        
    plt.title("%s" %  name)

ax[-1].axis('off')
ax[-2].axis('off')

##blt.letter_subplots(axes=ax.flatten(), xoffset=-.1, yoffset=1.05)
plt.tight_layout()
##plt.savefig("figureX-hx-distribution.pdf")
plt.show()


### Reading in preprocessed histogram data
##fig, ax = plt.subplots(4,3, figsize=(8,6), sharey=True)
##ax = ax.flatten()
##
##df = pd.read_csv("histogram_data.csv", sep = ",")
##for i,name in enumerate(small_networks):
##    plt.sca(ax[i])
##    data = df.loc[df["name"]==name]
##    n = data["n"].values[:-1]
##    bins = data["bin"].values
##    plt.bar(bins[:-1],n)    
##
####    plt.axvline(np.mean(hx_list),color="k",linestyle="-",label="mean")
####    plt.axvline(np.median(hx_list),color="C6",linestyle="--",label="median")
##    if i in [0,3,6,9]:
##        plt.ylabel("Density")
####        if i == 0:
####            plt.legend()
##        
##    plt.title("%s" %  name)
##    
##ax[-1].axis('off')
##ax[-2].axis('off')
##
####blt.letter_subplots(axes=ax.flatten(), xoffset=-.1, yoffset=1.05)
##plt.tight_layout()
####plt.savefig("figureX-hx-distribution.pdf")
##plt.show()
##



