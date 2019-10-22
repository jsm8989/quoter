import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import networkx as nx

N = 100
q = 0.5
T = 1000
trials_list = list(range(200))

k = 5
hx_sum = 0
hx_count = 0
dens = 0
ASPL_sum = 0
clus = 0
assort = 0
count = 0
data = []
for trial in trials_list:
    efile = "../data_ER/edge/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,k,q,T,trial)
    gfile = "../data_ER/graph/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,k,q,T,trial)
    if os.path.isfile(efile):
        elist = []
        G = nx.Graph()
        with open(efile,"r") as f:
            next(f)
            for line in f:
                line = line.rstrip().split()
                alter = int(line[0])
                ego = int(line[1])
                elist.append((alter,ego))
        G.add_edges_from(elist)
        ccs = sorted(nx.connected_components(G), key=len, reverse=True)
        G.remove_nodes_from(list(set(range(N)) - set(ccs[0])))
        ASPL = nx.average_shortest_path_length(G)
        ASPL_sum += ASPL
        count += 1

        with open(gfile,"r") as f:
            outfile = efile = "../data_ER/graph2/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,k,q,T,trial)
            with open(outfile,"w") as g:
                g.write(f.readline())
                data = f.readline().rstrip().split()
                s = " ".join(data[:10]) + " "  + "%0.8f" % ASPL + " " + " ".join(data[11:])
                g.write(s)
print(ASPL_sum/count)



##np.savetxt("hx_ER.csv",data_list,delimiter=",")
