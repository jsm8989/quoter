from read_networks import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import os

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
trials_list = list(range(500))

# PLOT 1: split into links based on distances
##max_dist = 10
##data = np.zeros((max_dist + 5,len(small_networks)))
##
##for i,name in enumerate(small_networks):
##    print(name)
##    
##    G = read_any(name)
##    nnodes = nx.number_of_nodes(G)
##    nedges = nx.number_of_edges(G)
##    data[max_dist,i] = nx.average_shortest_path_length(G)
##    data[max_dist+1,i] = nedges/(nnodes*(nnodes-1)/2)
##    data[max_dist+2,i] = nx.transitivity(G)
##    data[max_dist+3,i] = nx.degree_assortativity_coefficient(G)
##    data[max_dist+4,i] = 2*nedges/nnodes
##
##    count = np.zeros(max_dist)
##    for trial in trials_list:
##        outdir = os.path.join("../data/", name)
##        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
##        edata = pd.read_csv(os.path.join(outdir,outfile), sep = " ")
##
##        for dist in range(1,max_dist+1):
##            try:
##                data[dist-1,i] += np.sum(edata["hx"].loc[edata["distance"]==dist].values)
##                count[dist-1] += len(edata["hx"].loc[edata["distance"]==dist].values)
##            except: # no nodes at distance == dist
##                pass
##
##        data[:max_dist,i] = np.divide(data[:max_dist,i],count)
##
##dfstat = pd.DataFrame({"network":small_networks, "ASPL":data[max_dist,:],
##                   "density":data[max_dist+1,:],"transitivity":data[max_dist+2,:],
##                   "assortativity":data[max_dist+3,:],"average_degree":data[max_dist+4,:]})
##dfhx = pd.DataFrame(data=data[:max_dist,:], index=range(0,max_dist), columns=list(map(str,range(1,max_dist+1))))
##
##df = pd.concat([dfstat,dfhx], axis=1)
##df = df.to_csv("hx_real-Distance.csv",index=False)
##



# PLOT 2 split into links which are at distance 1 & average over all
##data = np.zeros((6,len(small_networks)))
##
##for i,name in enumerate(small_networks):
##    print(name)
##    
##    G = read_any(name)
##    nnodes = nx.number_of_nodes(G)
##    nedges = nx.number_of_edges(G)
##    data[1,i] = nx.average_shortest_path_length(G)
##    data[2,i] = nedges/(nnodes*(nnodes-1)/2)
##    data[3,i] = nx.transitivity(G)
##    data[4,i] = nx.degree_assortativity_coefficient(G)
##    data[5,i] = 2*nedges/nnodes
##
##    count = 0
##    for trial in trials_list:
##        outdir = os.path.join("../data/", name)
##        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
##        edata = pd.read_csv(os.path.join(outdir,outfile), sep = " ")
##
##        try:
####            data[0,i] += np.sum(edata["hx"].loc[edata["distance"]==1].values)
####            count += len(edata["hx"].loc[edata["distance"]==1].values)
##            data[0,i] += np.sum(edata["hx"].values)
##            count += len(edata["hx"].values)
##        except: # no nodes at distance == dist
##            pass
##
##    data[0,i] = np.divide(data[0,i],count)
##
##df = pd.DataFrame({"network":small_networks, "hx":data[0,:], "ASPL":data[1,:],
##                   "density":data[2,:],"transitivity":data[3,:],
##                   "assortativity":data[4,:],"average_degree":data[5,:]})
##
####df = df.to_csv("hx_real-nonlinks1.csv",index=False)
##df = df.to_csv("hx_real-nonlinks.csv",index=False)
##
##df = pd.read_csv("hx_real-nonlinks.csv")
##df1 = pd.read_csv("hx_real-nonlinks1.csv")
##plt.plot(df["density"],df["hx"],'o',label="Average over all distances")
##plt.plot(df1["density"],df1["hx"],'o',label="Average at distance 1")
##plt.legend()
##plt.xlabel(r"Density,  $M/\binom{N}{2}$")
##plt.ylabel("Cross-entropy")
##plt.show()



# PLOT 3: Configuration model
##data = np.zeros((6,len(small_networks)))
##
##for i,name in enumerate(small_networks):
##    count_hx = 0
##    count_trials = 0
##    for trial in trials_list:
##        print(name,trial)
##        outdir = os.path.join("../data_configuration/", name)
##        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
##        edata = pd.read_csv(os.path.join(outdir,outfile), sep = " ")
##
##        G = nx.read_edgelist(os.path.join(outdir, "edgelist_" + outfile), create_using=nx.Graph())
##        nnodes = nx.number_of_nodes(G)
##        nedges = nx.number_of_edges(G)
##        data[1,i] += nx.average_shortest_path_length(G)
##        data[2,i] += nedges/(nnodes*(nnodes-1)/2)
##        data[3,i] += nx.transitivity(G)
##        data[4,i] += nx.degree_assortativity_coefficient(G)
##        data[5,i] += 2*nedges/nnodes
##        count_trials += 1
##
##        try:
####            data[0,i] += np.sum(edata["hx"].loc[edata["distance"]==1].values)
####            count += len(edata["hx"].loc[edata["distance"]==1].values)
##            data[0,i] += np.sum(edata["hx"].values)
##            count_hx += len(edata["hx"].values)
##        except: # no nodes at distance == dist
##            pass
##
##    data[0,i] = np.divide(data[0,i],count_hx)
##    data[1:,i] = np.divide(data[1:,i],count_trials)
##
##df = pd.DataFrame({"network":small_networks, "hx":data[0,:], "ASPL":data[1,:],
##                   "density":data[2,:],"transitivity":data[3,:],
##                   "assortativity":data[4,:],"average_degree":data[5,:]})
##
####df = df.to_csv("hx_real-nonlinks1_config.csv",index=False)
##df = df.to_csv("hx_real-nonlinks_config.csv",index=False)

df = pd.read_csv("hx_real-nonlinks.csv")
df1 = pd.read_csv("hx_real-nonlinks_config.csv")
plt.plot(df["transitivity"],df1["transitivity"],"o")
##plt.plot(df["density"],df["hx"],'o',label="Real network")
##plt.plot(df1["density"],df1["hx"],'o',label="Configuration model")
plt.legend()
plt.xlabel("Transitivity")
plt.ylabel("Cross-entropy")
plt.show()
                
