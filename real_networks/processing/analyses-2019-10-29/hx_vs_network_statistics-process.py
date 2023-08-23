import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import pandas as pd
import networkx as nx
import os
import random
import sys

sys.path.append(
    "/home/jimjam/Documents/Adelaide/quoter"
)  # regrettably using this quick fix
import real_networks.sims_scripts.read_networks as read

networks_dict = {
    "Adolescent health": read.read_adolescent,
    "Arxiv CondMat": read.read_arxiv_CondMat,
    "Arxiv GrQc": read.read_arxiv_GrQc,
    "CKM physicians": read.read_ckm,
    "Dolphins": read.read_dolphins,
    "Email Spain": read.read_email,
    "Email Enron": read.read_enron,
    "Email Eu Core": read.read_Eu_Core,
    "Freeman's EIES": read.read_Freemans,
    "Golden Age": read.read_golden,
    "Hypertext": read.read_hypertext,
    "Kapferer tailor": read.read_kapf,
    "Les Miserables": read.read_lesmis,
    "Marvel": read.read_Marvel,
    "Hollywood music": read.read_movies,
    "Network science": read.read_netscience,
    "NFL": read.read_NFL,
    "Intra-organizational": read.read_org,
    "Web of Trust": read.read_pgp,
    "Sampson's monastery": read.read_Sampson,
    "Terrorist": read.read_terrorist,
    "UC Irvine": read.read_UC_Irvine,
}

q = 0.9
T = 1000
trials_list = list(range(300))
small_networks = [
    "CKM physicians",
    "Dolphins",
    "Email Spain",
    "Freeman's EIES",
    "Golden Age",
    "Kapferer tailor",
    "Les Miserables",
    "Hollywood music",
    "Sampson's monastery",
    "Terrorist",
]

### PLOT 1 split into links which are at distance 1 & average over all
data = np.zeros((len(small_networks), 14))
datadir = "../../data-NEW/data"
for i, name in enumerate(small_networks):
    print(name)

    os.chdir("../")  # <--this is a mess. Change this!!
    G = read.read_any(name)
    os.chdir("analyses-2019-10-29")

    nnodes = nx.number_of_nodes(G)
    nedges = nx.number_of_edges(G)
    data[i, 0] = nnodes
    data[i, 1] = nedges
    data[i, 2] = nedges / (nnodes * (nnodes - 1) / 2)
    data[i, 3] = 2 * nedges / nnodes
    data[i, 4] = max(list(nx.degree(G, G.nodes()).values()))
    data[i, 5] = min(list(nx.degree(G, G.nodes()).values()))
    data[i, 6] = nx.degree_assortativity_coefficient(G)
    data[i, 7] = nx.transitivity(G)
    data[i, 8] = nx.average_clustering(G)
    data[i, 9] = nx.average_shortest_path_length(G)

    count = (
        0  # the total number of edges involved in the computation (across all trials)
    )
    for trial in trials_list:
        outdir = os.path.join(datadir, name)
        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name, q, T, trial)
        edata = pd.read_csv(os.path.join(outdir, outfile), sep=" ")

        data[i, 10] += np.sum(edata["hx"].values)
        data[i, 11] += np.sum(np.power(edata["hx"].values, 2))
        edata["ECC"].loc[edata["ECC"] == 2] = 1  # call undefined ECC to  be 1
        data[i, 12] += np.sum(edata["ECC"].values)
        count += len(edata["hx"].values)

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
df_names = pd.DataFrame({"network": small_networks})
df_stats = pd.DataFrame(data=data, columns=cols)
df = pd.concat([df_names, df_stats], axis=1)
df[["network"] + cols].to_csv("real_networks-links_only.csv", index=False)
