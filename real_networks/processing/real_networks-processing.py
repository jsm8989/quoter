from read_networks import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import pandas as pd
import networkx as nx
import os
import random
import scipy.stats


networks_dict = {"Adolescent health": read_adolescent,
                "Arxiv CondMat": read_arxiv_CondMat,
##                "Arxiv GrQc": read_arxiv_GrQc,
                "CKM physicians": read_ckm,
                "Dolphins": read_dolphins,
                "Email Spain": read_email,
                "Email Enron": read_enron,
##                "Email Eu Core": read_Eu_Core,
                "Freeman's EIES": read_Freemans,
                "Golden Age": read_golden,
##                "Hypertext": read_hypertext,
                "Kapferer tailor": read_kapf,
                "Les Miserables": read_lesmis,
##                "Marvel": read_Marvel, 
                "Hollywood music": read_movies,
##                "Network science": read_netscience,
##                "NFL": read_NFL,
##                "Intra-organizational": read_org,
##                "Web of Trust": read_pgp,
                "Sampson's monastery": read_Sampson,
                "Terrorist": read_terrorist}
##                "UC Irvine": read_UC_Irvine}

small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]

q = 0.5
T = 1000
trials_list = list(range(300))

### Compute edge betweenness
##datadir = "../data_separate_link-nonlink/data"
##if not os.path.isdir("edge_betweenness/"):
##    os.mkdir("edge_betweenness/")
##    
##for name in small_networks:
##    if not os.path.isdir("edge_betweenness/" + name):
##        os.mkdir("edge_betweenness/" + name)
##        
##    G = read_any(name)
##    EB = nx.edge_betweenness_centrality(G)
##
##    for trial in trials_list:
##        if trial % 50 == 0:
##            print(name,trial)
##        indir = os.path.join(datadir, name)
##        infile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
##        with open(os.path.join(indir,infile),"r") as f:
##            with open(os.path.join("edge_betweenness/",name,infile),"w") as g:
##                header = f.readline().rstrip()
##                g.write(header + " " + "edge_betweenness\n")
##                for line in f:
##                    data = line.rstrip()
##                    alter = int(data.split()[0])
##                    ego = int(data.split()[1])
##                    dist = int(data.split()[4])
##                    if dist == 1:
##                        if (alter,ego) in EB:
##                            ebw = EB[(alter,ego)]
##                        elif (ego,alter) in EB:
##                            ebw = EB[(ego,alter)]
##                        data = data + " " + "%0.8f\n" % ebw
##                    else:
##                        data =  data + " " + "NA\n"
##                    g.write(data)
                    
                
# Edge betweenness plot
datadir = "edge_betweenness/"

for name in [small_networks[0]]:
    stat_list = []
    hx_list = []
    for trial in trials_list:
        infile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
        df = pd.read_csv(os.path.join(datadir,name,infile), sep = " ")
        df = df.loc[~df["edge_betweenness"].isnull()]
        stat_list.extend(df["edge_betweenness"].values)
        hx_list.extend(df["hx"].values)
            
#plot
sample = random.sample(range(len(hx_list)),5000) # take a sample
X = np.array(stat_list)[sample]
Y = np.array(hx_list)[sample]
        
binned_stat = scipy.stats.binned_statistic
# nice builtin function!
y_bins,bin_edges, misc = binned_stat(X,Y, statistic="mean", bins=8)
x_bins = (bin_edges[:-1]+bin_edges[1:])/2

s_bins,bin_edges, misc = binned_stat(X,Y, statistic=np.std, bins=8)


plt.plot(X,Y, 'o', alpha=0.5)
plt.plot(x_bins, y_bins, "-", linewidth=3, markersize=12)

# Now, plot the std as errorbars! (check out the docstring)
plt.errorbar( x_bins, y_bins, yerr=s_bins,
fmt="none", # only show errorbars
elinewidth=5,
ecolor='C1',
zorder=5 # plot bars ABOVE scatter
)

plt.xlabel("Edge betweenness")
plt.ylabel("Cross-entropy")
plt.show()














