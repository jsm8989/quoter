import numpy as np
import pandas as pd
import os
from read_networks import *
from make_configMod import *

q = 0.9
T = 1000
trials_list = list(range(300))
small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]
eps = 0.25
##Clustering experiment
data = np.zeros((len(small_networks),14))
datadir = "../../data-NEW/data_clustering"
for i,name in enumerate(small_networks):
    print(name)
    
##    for _ in range(300):
##        os.chdir("../") # <--this is a mess. Change this!!
##        G0 = read_any(name)
##        os.chdir("analyses-2019-10-29")
##        nnodes = nx.number_of_nodes(G0)
##        nedges = nx.number_of_edges(G0)
##        
##        n = min(int( nedges*eps ),len(list(nx.non_edges(G0))))
##        G = add_edges(G0,n)
##        nnodes = nx.number_of_nodes(G)
##        nedges = nx.number_of_edges(G)
##
##        data[i,0] += nnodes
##        data[i,1] += nedges
##        data[i,2] += nedges/(nnodes*(nnodes-1)/2)
##        data[i,3] += 2*nedges/nnodes
##        data[i,4] += max(list(nx.degree(G,G.nodes()).values()))
##        data[i,5] += min(list(nx.degree(G,G.nodes()).values()))
##        data[i,6] += nx.degree_assortativity_coefficient(G)
##        data[i,7] += nx.transitivity(G)
##        data[i,8] += nx.average_clustering(G)
##        data[i,9] += nx.average_shortest_path_length(G)
    
    count = 0 # the total number of edges involved in the computation (across all trials) 
    for trial in trials_list:
        outdir = os.path.join(datadir, name)
##        outfile = "EDGE_%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
        outfile = "TRIANGLE_%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
        edata = pd.read_csv(os.path.join(outdir,outfile), sep = " ")

        

        data[i,10] += np.sum(edata["hx"].values)
        data[i,11] += np.sum(np.power(edata["hx"].values,2))
        edata["ECC"].loc[edata["ECC"]==2] = 1 # call undefined ECC to  be 1
        data[i,12] += np.sum(edata["ECC"].values)
        count += len(edata["hx"].values)

    data[i,:10] /= 300
    data[i,[10,11,12]] /= count
    data[i,13] = count

# write to csv
cols = ["nodes","edges","density","average_degree","max_degree","min_degree",
        "degree_assortativity","transitivity","average_clustering","ASPL",
        "average_hx","average_hxsquared","average_ECC","count"]
df_names = pd.DataFrame({"network": small_networks})
df_stats = pd.DataFrame(data=data,columns=cols)
df = pd.concat([df_names,df_stats],axis=1)
##df[["network"] + cols].to_csv("real_networks-links_only-EDGE.csv",index=False)
df[["network"] + cols].to_csv("real_networks-links_only-TRIANGLE.csv",index=False)

