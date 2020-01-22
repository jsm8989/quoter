from read_networks import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import pandas as pd
import networkx as nx
import os
import random
from make_configMod import *

small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]

q = 0.5
T = 1000
trials_list = list(range(300))


### VERSION 1: 100 SWAPS
##nswaps = 100
##data = np.zeros((len(small_networks),11))
##datadir = "../data_xswap/"
##for i,name in enumerate(small_networks):
##
##    # get graph data from reconstructed xswap networks
##    for xswap_trial in range(75):
##        if xswap_trial % 15 == 0:
##            print(name,xswap_trial)
##            
##        G0 = read_any(name)
##        G = xswap(G0,nswaps)
##        
##        nnodes = nx.number_of_nodes(G)
##        nedges = nx.number_of_edges(G)
##        data[i,0] += nnodes
##        data[i,1] += nedges
##        data[i,2] += nedges/(nnodes*(nnodes-1)/2)
##        data[i,3] += 2*nedges/nnodes
##        data[i,4] += max(list(nx.degree(G,G.nodes()).values()))
##        data[i,5] += min(list(nx.degree(G,G.nodes()).values()))
##        data[i,6] += nx.transitivity(G)
##        data[i,7] += nx.average_clustering(G)
##
##    # get edge data
##    count = 0
##    for trial in trials_list:
##            
##        efile = "../data_xswap/%s/%s_q%0.1f_T%i_sim%i.txt" % (name,name,q,T,trial)
##
##        if os.path.isfile(efile):
##            edata = pd.read_csv(efile, sep = " ")
##
##            hx = edata["hx"].values
##            data[i,8] += np.sum(hx)
##            data[i,9] += np.sum(np.power(hx,2))
##            count += len(hx)
##
##    data[i,:8] /= 75
##    data[i,[8,9]] /= count
##    data[i,10] = count
##
### write to csv
####cols = ["nodes","edges","density","average_degree","max_degree","min_degree",
####        "degree_assortativity","transitivity","average_clustering","ASPL",
####        "average_hx","average_hxsquared","average_ECC","count"]
##cols = ["nodes","edges","density","average_degree","max_degree","min_degree",
##        "transitivity","average_clustering",
##        "average_hx","average_hxsquared","count"]
##df_names = pd.DataFrame({"network": small_networks})
##df_stats = pd.DataFrame(data=data,columns=cols)
##df = pd.concat([df_names,df_stats],axis=1)
##df[["network"] + cols].to_csv("real_networks-xswap.csv",index=False)



def sample_var(x1,x2,n):
    return (n*x2 - n*np.power(x1,2))/(n-1) 

##### PLOT: xswap vs original real network
##df1 = pd.read_csv("analyses-2019-10-27/real_networks-links_only.csv")
##df2 = pd.read_csv("real_networks-xswap.csv")
##
##c1 = "ko"
##c2 = "ro"
##var1 = sample_var(df1["average_hx"].values,df1["average_hxsquared"].values,df1["count"].values)
##var2 = sample_var(df2["average_hx"].values,df2["average_hxsquared"].values,df2["count"].values)
##for i in range(len(df1["network"].values)):
##    t1 = df1["transitivity"].values[i]
##    t2 = df2["transitivity"].values[i]
##    h1 = df1["average_hx"].values[i]
##    h2 = df2["average_hx"].values[i]
##    
##    plt.plot([t2,t1],[h2,h1],"k-")
##    print(t1,h1,var1[i])
##    plt.errorbar(t1,h1,yerr=var1[i],fmt=c1)
##    plt.errorbar(t2,h2,yerr=var2[i],fmt=c2)
##
##
##label1 = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
##                          markersize=6, label='Real network')
##label2 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
##                          markersize=6, label='x-swap')
##plt.legend(handles=[label1,label2])
##plt.xlabel("Transitivity")
##plt.ylabel("Cross-entropy")
##plt.show()




# VERSION 2: SWAPS = NUM_EDGES
##data = np.zeros((len(small_networks),5))
##for i,name in enumerate(small_networks):
##    # get edge data
##    count = 0
##    for trial in trials_list:
##        print(name,trial)
##        efile = "../data_xswap2/%s/edge_%s_q%0.1f_T%i_sim%i.txt" % (name,name,q,T,trial)
##        gfile = "../data_xswap2/%s/graph_%s_q%0.1f_T%i_sim%i.txt" % (name,name,q,T,trial)
##
##        if os.path.isfile(efile) and os.path.isfile(gfile):
##            edata = pd.read_csv(efile, sep = " ")
##            gdata = pd.read_csv(gfile, sep = " ")
##
##            data[i,0] += gdata["transitivity"].values[0]
##            data[i,1] += gdata["average_clustering"].values[0]
##
##            hx = edata["hx"].values
##            data[i,2] += np.sum(hx)
##            data[i,3] += np.sum(np.power(hx,2))
##            count += len(hx)
##        else:
##            print("missing data", name, trial)
##
##    data[i,:2] /= len(trials_list)
##    data[i,[2,3]] /= count
##    data[i,4] = count
##
### write to csv
##cols = ["transitivity","average_clustering",
##        "average_hx","average_hxsquared","count"]
##df_names = pd.DataFrame({"network": small_networks})
##df_stats = pd.DataFrame(data=data,columns=cols)
##df = pd.concat([df_names,df_stats],axis=1)
##df[["network"] + cols].to_csv("real_networks-xswap2.csv",index=False)





df1 = pd.read_csv("analyses-2019-10-27/real_networks-links_only.csv")
df2 = pd.read_csv("real_networks-xswap2.csv")

c1 = "ko"
c2 = "ro"
var1 = sample_var(df1["average_hx"].values,df1["average_hxsquared"].values,df1["count"].values)
var2 = sample_var(df2["average_hx"].values,df2["average_hxsquared"].values,df2["count"].values)
for i in range(len(df1["network"].values)):
    t1 = df1["transitivity"].values[i]
    t2 = df2["transitivity"].values[i]
    h1 = df1["average_hx"].values[i]
    h2 = df2["average_hx"].values[i]
    
    plt.plot([t2,t1],[h2,h1],"k-")
    print(t1,h1,var1[i])
    plt.errorbar(t1,h1,yerr=var1[i],fmt=c1)
    plt.errorbar(t2,h2,yerr=var2[i],fmt=c2)


label1 = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
                          markersize=6, label='Real network')
label2 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                          markersize=6, label='x-swap')
plt.legend(handles=[label1,label2])
plt.xlabel("Transitivity")
plt.ylabel("Cross-entropy")
plt.show()
