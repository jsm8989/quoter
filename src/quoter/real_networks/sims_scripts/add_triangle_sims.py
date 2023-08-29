# -*- coding: utf-8 -*-

# add_triangle_sims.py
# Tyson Pond
# Last Modified: 2019-10-24

from read_networks import read_any, networks_dict, small_networks
from make_configMod import add_triangles

import os, sys
import numpy as np
import networkx as nx

sys.path.append("/home/jimjam/Documents/Adelaide/quoter")
import src.quoter.quoter_model as qm


def create_data_subdirs(datadir, subdirs):
    """Create a directory for each real world network in which
    simulation data is stored.

    datadir (string) = name for root folder of real-world networks data
    subdirs (list of strings) = list of folder names of each real-world network
    """
    if not os.path.isdir(datadir):
        os.mkdir(datadir)

    for f in subdirs:
        path = os.path.join(datadir, f)
        if not os.path.isdir(path):
            os.mkdir(path)


def write_data(G, outdir, outfile, edge_sample_file):
    """
    Compute and write data from quoter model simulations.
    """
    # compute edge data
    edges = []
    with open(edge_sample_file, "r") as f:
        for line in f:
            line = line.rstrip().split()
            edges.append((int(line[0]), int(line[1])))

    quoteProba_list = []
    hx_list = []
    dist_list = []
    triangles_list = []
    deg_u_list = []
    deg_v_list = []
    ECC_list = []

    H = nx.Graph(G)
    for e in edges:
        # compute all cross entropies. e[0] = alter, e[1] = ego

        time_tweets_target = qm.words_to_tweets(
            G.node[e[1]]["words"], G.node[e[1]]["times"]
        )
        time_tweets_source = qm.words_to_tweets(
            G.node[e[0]]["words"], G.node[e[0]]["times"]
        )
        hx = qm.timeseries_cross_entropy(
            time_tweets_target, time_tweets_source, please_sanitize=False
        )
        hx_list.append(hx)

        # also record quote probability
        quoteProba = 1 / len(G.predecessors(e[1]))
        quoteProba_list.append(quoteProba)

        ##        # also record distance between nodes
        ##
        ##        try:
        ##            dist = nx.shortest_path_length(G,source=e[0],target=e[1])
        ##        except:
        ##            dist = -1
        ##        dist_list.append(dist)

        # also record edge clustering info
        triangles, deg_u, deg_v, ECC = qm.edge_clustering_coeff(
            H, e[0], e[1], return_info=True
        )
        triangles_list.append(triangles)
        deg_u_list.append(deg_u)
        deg_v_list.append(deg_v)
        ECC_list.append(ECC)

    # write edge data
    with open(os.path.join(outdir, outfile), "w") as f:
        f.write("alter ego quoteProb hx triangles d_u d_v ECC\n")  # header
        for i, e in enumerate(edges):
            f.write(
                "%i %i %0.8f %0.8f %i %i %i %0.4f\n"
                % (
                    e[0],
                    e[1],
                    quoteProba_list[i],
                    hx_list[i],
                    triangles_list[i],
                    deg_u_list[i],
                    deg_v_list[i],
                    ECC_list[i],
                )
            )


if __name__ == "__main__":
    ##    create_data_subdirs("../data-NEW/data_clustering", small_networks)

    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0])

    ##    JOBNUM = 0
    ##    NUMJOBS = 1

    q = 0.9
    T = 1000
    trials_list = list(range(300))

    ##    small_networks = ["CKM physicians"] ## 1 network -- how does number of edges change?
    ##    epsilon_list = np.arange(0.05,0.41,0.05)
    eps = 0.25

    params = []
    for name in small_networks:
        ##        for eps in epsilon_list:
        for trial in trials_list:
            params.append((name, trial))

    # parameters to keep for this job
    params = [P for i, P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for name, trial in params:
        ##        outdir = os.path.join("../data_separate_link-nonlink/data_CKM_vary_n-edges", name)
        ##        outfile = "TRIANGLE_%s_eps%0.2f_q%0.1f_T%i_sim%i.txt" % (name,eps,q,T,trial)
        outdir = os.path.join("../data-NEW/data_clustering", name)
        outfile = "TRIANGLE_%s_q%0.1f_T%i_sim%i.txt" % (name, q, 1000, trial)
        efile = "%s_q%0.1f_T%i_sim%i.txt" % (name, q, 1000, trial)
        edge_sample_file = os.path.join("../data-NEW/edge_sample", name, efile)
        if not os.path.isfile(os.path.join(outdir, outfile)):
            G0 = read_any(name)
            nnodes = nx.number_of_nodes(G0)
            nedges = nx.number_of_edges(G0)
            n = min(int(nedges * eps), len(list(nx.non_edges(G0))))
            G1 = add_triangles(G0, n)
            G = nx.DiGraph(G1)
            qm.quoter_model_sim(
                G, q, T, outdir, outfile, write_data, None, edge_sample_file
            )
