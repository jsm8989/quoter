from read_networks import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
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
##data = np.zeros((9,len(small_networks)))
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
##    C = nx.average_clustering(G)
##    data[6,i] = C
##
##    count_all = count_abv = count_blw = 0
##    for trial in trials_list:
##        outdir = os.path.join("../data/", name)
##        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
##        edata = pd.read_csv(os.path.join(outdir,outfile), sep = " ")
##
##        C_dict = nx.clustering(G)
##        egos = edata["ego"].values
##        
##        for ego in egos:
##            ego_C = C_dict[ego]
##            ego_hxs = edata["hx"].loc[edata["ego"] == ego].values
##            
##            if ego_C > C:          
##                data[7,i] += np.sum(ego_hxs)
##                count_abv += len(ego_hxs)
##
##        
##            if ego_C < C:
##                data[8,i] += np.sum(ego_hxs)
##                count_blw += len(ego_hxs)
##
##        try:
####            data[0,i] += np.sum(edata["hx"].loc[edata["distance"]==1].values)
####            count += len(edata["hx"].loc[edata["distance"]==1].values)
##            data[0,i] += np.sum(edata["hx"].values)
##            count_all += len(edata["hx"].values)
##        except: # no nodes at distance == dist
##            pass
##
##    data[0,i] /= count_all
##    data[7,i] /= count_abv
##    data[8,i] /= count_blw
##
##df = pd.DataFrame({"network":small_networks, "hx":data[0,:], "ASPL":data[1,:],
##                   "density":data[2,:],"transitivity":data[3,:],
##                   "assortativity":data[4,:],"average_degree":data[5,:],
##                   "average_clustering":data[6,:],"hx_abv":data[7,:],
##                   "hx_blw":data[8,:]})
##
####df = df.to_csv("hx_real-nonlinks1.csv",index=False)
##df = df.to_csv("hx_real-nonlinks-NEW.csv",index=False)

##df = pd.read_csv("hx_real-nonlinks.csv")
##df1 = pd.read_csv("hx_real-nonlinks1.csv")
##plt.plot(df["density"],df["hx"],'o',label="Average over all distances")
##plt.plot(df1["density"],df1["hx"],'o',label="Average at distance 1")
##plt.legend()
##plt.xlabel(r"Density,  $M/\binom{N}{2}$")
##plt.ylabel("Cross-entropy")
##plt.show()



# PLOT 3: Configuration model & clustering sims
##data = np.zeros((7,len(small_networks)))
####trials_list = list(range(500)) # configuration sims
##trials_list = list(range(300)) # clustering sims
##for i,name in enumerate(small_networks):
##    count_hx = 0
##    count_trials = 0
##    for trial in trials_list:
##        print(name,trial)
####        outdir = os.path.join("../data_configuration/", name)
####        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
##        outdir = os.path.join("../data_clustering", name)
##        outfile = "TRIANGLE3_%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
##        edata = pd.read_csv(os.path.join(outdir,outfile), sep = " ")
##
##        G = nx.read_edgelist(os.path.join(outdir, "edgelist_" + outfile), create_using=nx.Graph())
##        nnodes = nx.number_of_nodes(G)
##        nedges = nx.number_of_edges(G)
##
##        LCC = max(nx.connected_component_subgraphs(G), key=len)
##        data[1,i] += nx.average_shortest_path_length(LCC) # note: ASPL is slow
##        data[2,i] += nedges/(nnodes*(nnodes-1)/2)
##        data[3,i] += nx.transitivity(G)
##        data[4,i] += nx.degree_assortativity_coefficient(G)
##        data[5,i] += 2*nedges/nnodes
##        data[6,i] += nx.average_clustering(G)
##        count_trials += 1
##
##        try:
####            data[0,i] += np.sum(edata["hx"].loc[edata["distance"]==1].values)
####            count_hx += len(edata["hx"].loc[edata["distance"]==1].values)
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
##                   "assortativity":data[4,:],"average_degree":data[5,:],
##                   "average_clustering":data[6,:]})
##
####df = df.to_csv("hx_real-nonlinks1_config.csv",index=False)
##df = df.to_csv("hx_real-add_TRIANGLE3.csv",index=False)




# ACTUAL PLOT (CONFIGURATION)
##df = pd.read_csv("hx_real-nonlinks1.csv")
##df1 = pd.read_csv("hx_real-nonlinks1_config.csv")
####plt.plot(df["transitivity"],df["hx"],'o',label="Real network")
####plt.plot(df1["transitivity"],df1["hx"],'o',label="Configuration model")
##
##for i in range(len(df["hx"].values)):
##    plt.plot(df["transitivity"].values[i],df["hx"].values[i],'ko')
##    plt.plot(df1["transitivity"].values[i],df1["hx"].values[i],'ro')
##    plt.plot([df["transitivity"].values[i],df1["transitivity"].values[i]],[df["hx"].values[i],df1["hx"].values[i]],'r-')
##
##label1 = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
##                          markersize=6, label='Real network')
##label2 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
##                          markersize=6, label='Configuration model')
##plt.legend(handles=[label1,label2])
##plt.xlabel("Transitivity")
##plt.ylabel("Cross-entropy")
##plt.show()


# ADDING EDGES VS TRIANGLES
##df1 = pd.read_csv("hx_real-nonlinks.csv")
##df2 = pd.read_csv("hx_real-add_EDGE.csv")
##df3 = pd.read_csv("hx_real-add_TRIANGLE3.csv")
##
##for i in range(len(df1["hx"].values)):
##    plt.plot(df2["transitivity"].values[i],df2["hx"].values[i],'ko')
##    plt.plot(df3["transitivity"].values[i],df3["hx"].values[i],'ro')
##    plt.plot([df2["transitivity"].values[i],df3["transitivity"].values[i]],
##             [df2["hx"].values[i],df3["hx"].values[i]],'r-')
##    
##label1 = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
##                          markersize=6, label='Edge added randomly')
##label2 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
##                          markersize=6, label='Triangle completion')
##plt.legend(handles=[label1,label2])
##plt.xlabel("Transitivity")
##plt.ylabel("Cross-entropy")
##plt.show()



# ABOVE VS BELOW AVERAGE C_i
##fig = plt.figure(figsize=(14,4))
##df = pd.read_csv("hx_real-nonlinks.csv")
##n = len(df["network"].values)
##ypos = list(range(4*n))
##ypos = [y for i,y in enumerate(ypos) if (i-3) % 4 != 0]
##widths = []
##colors = ["red","black","blue"]*n
##for i in range(n):
##    widths.extend([df["hx"].values[i], df["hx_abv"].values[i], df["hx_blw"].values[i]])
##plt.barh(ypos,widths,color=colors)
##plt.yticks(ypos[1::3],df["network"].values)
##plt.xlim([3.34,3.39])
##plt.xlabel("Cross-entropy")
##label1 = mpatches.Patch(color='red', label='hx all')
##label2 = mpatches.Patch(color='black', label=r'$C_i > \langle C_i \rangle$')
##label3 = mpatches.Patch(color='blue', label=r'$C_i < \langle C_i \rangle$')
##plt.legend(handles=[label1,label2,label3])
##plt.show()


def edge_clustering_coeff(G,u,v,return_info=False):
    u_nbrs = nx.neighbors(G,u)
    v_nbrs = nx.neighbors(G,v)
    uv_nbrs = set(u_nbrs) & set(v_nbrs)
    triangles = len(uv_nbrs)

    deg_u = len(u_nbrs)
    deg_v = len(v_nbrs)
    
    if min(deg_u-1,deg_v-1) == 0:
        ECC = "leaf"
    else:
        ECC = triangles/min(deg_u-1,deg_v-1)
    
    if return_info:
        return triangles, deg_u, deg_v, ECC
    else:
        return ECC

### ECC example from paper
##G = nx.Graph()
##G.add_edges_from([(1,2),(1,4),(1,5),(1,6),(2,3),(3,4),(3,5),(3,6),
##                  (4,5),(4,6),(5,6)])
##print(ECC(G,1,4))
##pos = nx.spring_layout(G)
##labels=nx.draw_networkx_labels(G,pos)
##nx.draw(G,pos)
##plt.show()

for name in networks_dict:
    print(name)
    G = read_any(name)
    ECCs = []
    for i,e in enumerate(G.edges()):
        ECCs.append(edge_clustering_coeff(G,e[0],e[1]))
##    print(len([x for x in ECCs if x == "leaf"])/len(G.edges()))
    print(np.mean([x for x in ECCs if x != "leaf"]))
##plt.hist([x for x in ECCs if x != "leaf"])
##plt.show()











