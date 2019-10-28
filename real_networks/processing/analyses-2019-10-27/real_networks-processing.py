from read_networks import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import pandas as pd
import networkx as nx
import os
import random

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

### PLOT 1 split into links which are at distance 1 & average over all
##data = np.zeros((len(small_networks),14))
##datadir = "../../data_separate_link-nonlink/data"
##for i,name in enumerate(small_networks):
##    print(name)
##    
##    os.chdir("../") # <--this is a mess. Change this!!
##    G = read_any(name)
##    os.chdir("analyses-2019-10-27")
##    
##    nnodes = nx.number_of_nodes(G)
##    nedges = nx.number_of_edges(G)
##    data[i,0] = nnodes
##    data[i,1] = nedges
##    data[i,2] = nedges/(nnodes*(nnodes-1)/2)
##    data[i,3] = 2*nedges/nnodes
##    data[i,4] = max(list(nx.degree(G,G.nodes()).values()))
##    data[i,5] = min(list(nx.degree(G,G.nodes()).values()))
##    data[i,6] = nx.degree_assortativity_coefficient(G)
##    data[i,7] = nx.transitivity(G)
##    data[i,8] = nx.average_clustering(G)
##    data[i,9] = nx.average_shortest_path_length(G)
##
##    count = 0 # the total number of edges involved in the computation (across all trials) 
##    for trial in trials_list:
##        outdir = os.path.join(datadir, name)
##        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
##        edata = pd.read_csv(os.path.join(outdir,outfile), sep = " ")
##
##
##        data[i,10] += np.sum(edata["hx"].loc[edata["distance"]==1].values)
##        data[i,11] += np.sum(np.power(edata["hx"].loc[edata["distance"]==1].values,2))
##        edata["ECC"].loc[edata["ECC"]==2] = 1 # call undefined ECC to  be 1
##        data[i,12] += np.sum(edata["ECC"].loc[edata["distance"]==1].values)
##        count += len(edata["hx"].loc[edata["distance"]==1].values)
##
##    data[i,[10,11,12]] /= count
##    data[i,13] = count
##
### write to csv
##cols = ["nodes","edges","density","average_degree","max_degree","min_degree",
##        "degree_assortativity","transitivity","average_clustering","ASPL",
##        "average_hx","average_hxsquared","average_ECC","count"]
##df_names = pd.DataFrame({"network": small_networks})
##df_stats = pd.DataFrame(data=data,columns=cols)
##df = pd.concat([df_names,df_stats],axis=1)
##df[["network"] + cols].to_csv("real_networks-links_only.csv",index=False)


### Real networks: cross-entropy versus density & other network statistics
##df = pd.read_csv("real_networks-links_only.csv")
##fig = plt.figure(figsize=(10,3))
##plt.subplot(1,3,1)
##plt.plot(df["density"],df["average_hx"],'ko')
##plt.xlabel(r"Density,  $M/\binom{N}{2}$")
##plt.ylabel("Cross-entropy")
##plt.subplot(1,3,2)
##plt.plot(df["transitivity"],df["average_hx"],'ko')
##plt.xlabel(r"Transitivity")
##plt.subplot(1,3,3)
##plt.plot(df["density"],df["transitivity"],'ko')
##plt.xlabel(r"Density,  $M/\binom{N}{2}$")
##plt.ylabel("Transitivity")
##plt.tight_layout()
##plt.show()

### standard deviation
##df = pd.read_csv("real_networks-links_only.csv")
##m2_minus_m1_sq = df["average_hxsquared"].values - np.power(df["average_hx"].values,2) 
##n_over_n_minus_1 = np.divide(df["count"].values,df["count"].values - 1)
##sample_stdev = np.sqrt(np.multiply(n_over_n_minus_1,m2_minus_m1_sq))
##fig = plt.figure(figsize=(10,3))
##plt.subplot(1,2,1)
##plt.plot(df["density"],sample_stdev,'ko')
##plt.xlabel(r"Density,  $M/\binom{N}{2}$")
##plt.ylabel("Cross-entropy standard deviation")
##plt.subplot(1,2,2)
##plt.plot(df["transitivity"],sample_stdev,'ko')
##plt.xlabel(r"Transitivity")
##plt.tight_layout()
##plt.show()

### ECC
##fig = plt.figure(figsize=(10,3))
##plt.subplot(1,2,1)
##plt.plot(df["average_ECC"],df["average_hx"],'ko')
##plt.xlabel("Average ECC")
##plt.ylabel("Cross-entropy")
##plt.subplot(1,2,2)
##plt.plot(df["average_clustering"],df["average_ECC"],'ko')
##plt.xlabel("Average [node] clustering")
##plt.ylabel("Average ECC")
##plt.tight_layout()
##plt.show()





# PLOT 2: Clustering experiment
##data = np.zeros((len(small_networks),14))
##datadir = "../../data_separate_link-nonlink/data_clustering"
##for i,name in enumerate(small_networks):
##    print(name)
##    
##    count = 0 # the total number of edges involved in the computation (across all trials) 
##    for trial in trials_list:
##        outdir = os.path.join(datadir, name)
##        outfile = "EDGE_%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
####        outfile = "TRIANGLE_%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
##        edata = pd.read_csv(os.path.join(outdir,outfile), sep = " ")
##
##        G = nx.read_edgelist(os.path.join(outdir, "edgelist_" + outfile), create_using=nx.Graph())
##        nnodes = nx.number_of_nodes(G)
##        nedges = nx.number_of_edges(G)
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
##
##        data[i,10] += np.sum(edata["hx"].loc[edata["distance"]==1].values)
##        data[i,11] += np.sum(np.power(edata["hx"].loc[edata["distance"]==1].values,2))
##        edata["ECC"].loc[edata["ECC"]==2] = 1 # call undefined ECC to  be 1
##        data[i,12] += np.sum(edata["ECC"].loc[edata["distance"]==1].values)
##        count += len(edata["hx"].loc[edata["distance"]==1].values)
##
##    data[i,:10] /= len(trials_list)
##    data[i,[10,11,12]] /= count
##    data[i,13] = count
##
### write to csv
##cols = ["nodes","edges","density","average_degree","max_degree","min_degree",
##        "degree_assortativity","transitivity","average_clustering","ASPL",
##        "average_hx","average_hxsquared","average_ECC","count"]
##df_names = pd.DataFrame({"network": small_networks})
##df_stats = pd.DataFrame(data=data,columns=cols)
##df = pd.concat([df_names,df_stats],axis=1)
##df[["network"] + cols].to_csv("real_networks-links_only-EDGE.csv",index=False)
####df[["network"] + cols].to_csv("real_networks-links_only-TRIANGLE.csv",index=False)





### ADDING EDGES VS TRIANGLES
##df1 = pd.read_csv("real_networks-links_only.csv")
##df2 = pd.read_csv("real_networks-links_only-EDGE.csv")
##df3 = pd.read_csv("real_networks-links_only-TRIANGLE.csv")

### just EDGE vs TRIANGLE
##for i in range(len(df1["network"].values)):
##    t2 = df2["transitivity"].values[i]
##    t3 = df3["transitivity"].values[i]
##    h2 = df2["average_hx"].values[i]
##    h3 = df3["average_hx"].values[i]
##
##    plt.plot(t2,h2,"co")
##    plt.plot(t3,h3,"ro")
##    
##    plt.plot([t2,t3],[h2,h3],"k-")
##    
##label2 = mlines.Line2D([], [], color='cyan', marker='o', linestyle='None',
##                          markersize=6, label='Edge added randomly')
##label3 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
##                          markersize=6, label='Triangle completion')
##plt.legend(handles=[label2,label3])
##plt.xlabel("Transitivity")
##plt.ylabel("Cross-entropy")
##plt.show()


### EDGE vs TRIANGLE vs original real network
##c1 = "ko"
##c2 = "co"
##c3 = "ro"
##for i in range(len(df1["network"].values)):
##    t1 = df1["transitivity"].values[i]
##    t2 = df2["transitivity"].values[i]
##    t3 = df3["transitivity"].values[i]
##    h1 = df1["average_hx"].values[i]
##    h2 = df2["average_hx"].values[i]
##    h3 = df3["average_hx"].values[i]
##    plt.plot(t1,h1,c1)
##    plt.plot(t2,h2,c2)
##    plt.plot(t3,h3,c3)
##
##    plt.plot([t2,t1,t3],[h2,h1,h3],"k-")
##    
####    z = sorted(zip([t1,t2,t3],[h1,h2,h3],[c1,c2,c3]), key = lambda x: x[0])
####    z = list(zip(*z))
##    
####    plt.plot(z[0][0],z[1][0],z[2][0])
####    plt.plot(z[0][1],z[1][1],z[2][1])
####    plt.plot(z[0][2],z[1][2],z[2][2])
####    
####    plt.plot([z[0][0],z[0][1],z[0][2]],[z[1][0],z[1][1],z[1][2]],"k--")
##    
##label1 = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
##                          markersize=6, label='Real network')
##label2 = mlines.Line2D([], [], color='cyan', marker='o', linestyle='None',
##                          markersize=6, label='Edge added randomly')
##label3 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
##                          markersize=6, label='Triangle completion')
##plt.legend(handles=[label1,label2,label3])
##plt.xlabel("Transitivity")
##plt.ylabel("Cross-entropy")
##plt.show()



# PLOT 3: cross-entropy versus "edge" statistics (quoteProb, ECC, distance)
##datadir = "../../data_separate_link-nonlink/data"
##
##with open("edge_stats-all_networks-links_only.txt","a+") as g:
##    g.write("network trial alter ego quoteProb hx distance triangles d_u d_v ECC\n")
##    
##for i,name in enumerate(small_networks):
##    print(name)
##    
##    os.chdir("../") # <--this is a mess. Change this!!
##    G = read_any(name)
##    os.chdir("analyses-2019-10-27")
##    
##    for trial in trials_list:
##        outdir = os.path.join(datadir, name)
##        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
##        edata = pd.read_csv(os.path.join(outdir,outfile), sep = " ")
##        with open(os.path.join(outdir,outfile),"r") as f:
##            next(f)
##            with open("edge_stats-all_networks-links_only.txt","a+") as g:
##                for line in f:
##                    line = line.rstrip().split()
##                    if line[-1] == "2.0000": # ECC undefined
##                        line[-1] = "1.0000" 
##                    if line[4] == "1": # distance == 1 --> links only
##                        g.write("%s %i " % (name,trial) + " ".join(line) + "\n")

            
# plot
##stat_list = []
##hx_list = []
#####"network trial alter ego quoteProb hx distance triangles d_u d_v ECC\n"
##with open("edge_stats-all_networks-links_only.txt","r") as f:
##    next(f)
##    
##    for line in f:
##        line = line.rstrip().split()
##        if float(line[-1]) <= 1: # golden age has self-loops and some ECC > 1
##            stat_list.append(float(line[-1])) # ECC
##            hx_list.append(float(line[-6])) # indexing from end because 'network' names are 2 words... sigh
####        stat_list.append(float(line[-7])) # quote probability
####        hx_list.append(float(line[-6]))
##print(len(hx_list))            
##sample = random.sample(range(len(hx_list)),10000) # take a sample
##stat_list = np.array(stat_list)[sample]
##hx_list = np.array(hx_list)[sample]
##plt.plot(stat_list,hx_list,'ko')
##plt.xlabel("ECC")
##plt.ylabel("Cross-entropy")
##plt.show()









