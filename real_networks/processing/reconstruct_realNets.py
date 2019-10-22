import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os
import networkx as nx
import shutil

q = 0.5
T = 1000
trials_list = list(range(100))

for folder in next(os.walk("../data_real/"))[1]:
    try:
        os.mkdir("../data_real/%s/graph2/" % folder)
    except:
        pass
    
    for trial in trials_list:
        efile = "../data_real/%s/edge/q%0.1f_T%i_sim%i.txt" % (folder,q,T,trial)

        if os.path.isfile(efile):
            outdir = "../data_real/%s/graph2/" % folder
            outfile = "q%0.1f_T%i_sim%i.txt" % (q,T,trial)
            with open(efile,"r") as f:
                next(f)
                elist = []
                for line in f:
                    dat = line.rstrip().split()
                    elist.append((int(dat[0]),int(dat[1])))
                G = nx.DiGraph()
                G.add_edges_from(elist)
                print(folder,trial)
                
            # graph skeleton for calculating clustering, transitivity, ASPL, etc.
            H = G.to_undirected()

            if trial == 0:
                # compute graph data
                nnodes = nx.number_of_nodes(H)
                nedges = nx.number_of_edges(H)
                dens = nedges/(nnodes*(nnodes-1)/2)
                indegs = list(G.in_degree(G.nodes()).values())
                outdegs = list(G.out_degree(G.nodes()).values())
                ccs = sorted(nx.connected_components(H), key=len, reverse=True)

                try: # error is raised if graph is disconnected
                    avg_shortest_path = nx.average_shortest_path_length(H)
                except:
                    avg_shortest_path = 0
                
                data_tuple = (nnodes,nedges,dens,np.mean(indegs), np.min(indegs), np.max(indegs),
                                  np.min(outdegs), np.max(outdegs), nx.transitivity(H), nx.average_clustering(H),
                                  avg_shortest_path, nx.degree_assortativity_coefficient(H), 
                                len(ccs), len(ccs[0])) # note avg_in == avg_out, so we only need to record one

                # write graph data
                with open(outdir + outfile, "w") as f:
                    f.write("nodes edges density average_degree min_indegree max_indegree " +
                            "min_outdegree max_outdegree transitivity average_clustering " +
                            "average_shortest_path_length assortativity " +
                            "number_of_components largest_component\n") # header
                    
                    f.write("%i %i %0.8f %0.8f %i %i %i %i %0.8f %0.8f %0.8f %0.8f %i %i" % data_tuple)

            else:
                shutil.copyfile("../data_real/%s/graph2/q%0.1f_T%i_sim0.txt" % (folder,q,T), outdir + outfile)
                





          



