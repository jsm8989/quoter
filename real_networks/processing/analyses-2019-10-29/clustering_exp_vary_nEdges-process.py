import numpy as np
import pandas as pd
import os, sys
import networkx as nx

sys.path.append("/home/jimjam/Documents/Adelaide/quoter")
from real_networks.sims_scripts.read_networks import small_networks


q = 0.5
T = 1000
trials_list = list(range(300))

# Clustering experiment... how does varying number of edges added affect hx
epsilon_list = np.arange(0.05, 0.41, 0.05)
data = np.zeros((len(epsilon_list), 14))
datadir = "../../data_separate_link-nonlink/data_CKM_vary_n-edges/"
name = "CKM physicians"
for i, eps in enumerate(epsilon_list):
    print(i)

    count = (
        0  # the total number of edges involved in the computation (across all trials)
    )
    for trial in trials_list:
        outdir = os.path.join(datadir, name)
        ##        outfile = "EDGE_%s_eps%0.2f_q%0.1f_T%i_sim%i.txt" % (name,eps,q,T,trial)
        outfile = "TRIANGLE_%s_eps%0.2f_q%0.1f_T%i_sim%i.txt" % (name, eps, q, T, trial)
        edata = pd.read_csv(os.path.join(outdir, outfile), sep=" ")

        G = nx.read_edgelist(
            os.path.join(outdir, "edgelist_" + outfile), create_using=nx.Graph()
        )
        nnodes = nx.number_of_nodes(G)
        nedges = nx.number_of_edges(G)
        data[i, 0] += nnodes
        data[i, 1] += nedges
        data[i, 2] += nedges / (nnodes * (nnodes - 1) / 2)
        data[i, 3] += 2 * nedges / nnodes
        data[i, 4] += max(list(nx.degree(G, G.nodes()).values()))
        data[i, 5] += min(list(nx.degree(G, G.nodes()).values()))
        data[i, 6] += nx.degree_assortativity_coefficient(G)
        data[i, 7] += nx.transitivity(G)
        data[i, 8] += nx.average_clustering(G)
        data[i, 9] += nx.average_shortest_path_length(G)

        data[i, 10] += np.sum(edata["hx"].loc[edata["distance"] == 1].values)
        data[i, 11] += np.sum(
            np.power(edata["hx"].loc[edata["distance"] == 1].values, 2)
        )
        data[i, 12] += np.sum(edata["ECC"].loc[edata["distance"] == 1].values)
        count += len(edata["hx"].loc[edata["distance"] == 1].values)

    data[i, :10] /= len(trials_list)
    data[i, [10, 11, 12]] /= count
    data[i, 13] = count

# write to csv
cols = [
    "nodes",
    "edges",
    "density",
    "average_degree",
    "max_degree",
    "min_degree",
    "degree_assortativity",
    "transitivity",
    "average_clustering",
    "ASPL",
    "average_hx",
    "average_hxsquared",
    "average_ECC",
    "count",
]
df_names = pd.DataFrame({"epsilon": epsilon_list})
df_stats = pd.DataFrame(data=data, columns=cols)
df = pd.concat([df_names, df_stats], axis=1)
df[["epsilon"] + cols].to_csv("CKM-links_only-EDGE.csv", index=False)
##df[["epsilon"] + cols].to_csv("CKM-links_only-TRIANGLE.csv",index=False)
