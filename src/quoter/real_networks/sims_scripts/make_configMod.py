# -*- coding: utf-8 -*-

# make_configMod.py
# Tyson Pond
# Last Modified: 2019-10-21

import networkx as nx
import numpy as np
import sys

sys.path.append("/home/jimjam/Documents/Adelaide/quoter")
from real_networks.sims_scripts.read_networks import (
    read_any,
    networks_dict,
    small_networks,
)
import random


def make_configMod(G):
    degree_seq = list(G.degree().values())
    if sum(degree_seq) % 2 != 0:
        degree_seq[0] += 1

    G = nx.configuration_model(degree_seq, create_using=nx.Graph())

    return G


def add_edges(G, n):
    """Take a graph G and add n edges randomly"""
    H = G.copy()
    nonedges = np.array(list(nx.non_edges(H)))
    to_add = np.random.choice(range(len(nonedges)), size=n, replace=False)
    H.add_edges_from(nonedges[to_add][:])
    return H


def add_triangles(G, n):
    """Take a graph G and add n edges which complete triangles.
    Of the edges which complete triangles, the edges are chosen at random.
    This is a randomized version of the first implementation. This may
    take a long time for extremely dense networks (a more exhaustive search
    like implementation 1 or 2 may be necessary) or for a large number
    of added edges.
    """
    H = G.copy()
    nodes = H.nodes()
    count = 0
    trial = 0
    while count < n:
        n1 = random.choice(nodes)
        nbrs = nx.neighbors(H, n1)
        if len(nbrs) >= 2:
            n2, n3 = random.sample(nbrs, k=2)
            if (n2, n3) not in H.edges() and (n3, n2) not in H.edges():
                H.add_edge(n2, n3)
                count += 1
        ##        print(trial)
        trial += 1
    return H


def xswap(G, n_steps):
    H = G.copy()
    count = 0
    while count < n_steps:
        H_temp = H.copy()
        edges = list(H_temp.edges())
        e1_ind, e2_ind = random.sample(range(len(edges)), k=2)  # choose 2 edges
        e1 = edges[e1_ind]  # edge 1
        e2 = edges[e2_ind]  # edge 2
        n1_ind = random.choice([0, 1])  # choose one node from edge 1
        n2_ind = random.choice([0, 1])  # choose one node from edge 2
        new_e1 = (e1[n1_ind], e2[1 - n2_ind])  # SWAP them (this is shorthand notation)
        new_e2 = (e1[1 - n1_ind], e2[n2_ind])

        # this if-statement avoids multiple edges
        if (
            new_e1 not in edges
            and new_e1[::-1] not in edges
            and new_e2 not in edges
            and new_e2[::-1] not in edges
        ):
            H_temp.remove_edges_from([e1, e2])
            H_temp.add_edge(*new_e1)
            H_temp.add_edge(*new_e2)

            # this if-statement avoids network fragmentation
            if nx.number_connected_components(H_temp) == 1:
                H = H_temp  # update the actual network
                count += 1

    return H


if __name__ == "__main__":
    G = read_any("CKM physicians")
    Gx = xswap(G, 20)
    print(nx.number_of_nodes(G), nx.number_of_nodes(Gx))
    print(nx.number_of_edges(G), nx.number_of_edges(Gx))
    print(nx.number_connected_components(G), nx.number_connected_components(Gx))
    print(nx.density(G), nx.density(Gx))
    print(nx.transitivity(G), nx.transitivity(Gx))
##    for name in small_networks:
##        print(name)
##        G0 = read_any(name)
##        nnodes = nx.number_of_nodes(G0)
##        nedges = nx.number_of_edges(G0)
##        n = min(int(nedges*0.25),len(list(nx.non_edges(G0))))
##        G1 = add_edges(G0,n)
##        G2 = add_triangles3(G0,n)
##        print(nx.transitivity(G0),nx.density(G0))
##        print(nx.transitivity(G1),nx.density(G1))
##        print(nx.transitivity(G2),nx.density(G2))

##    before = []
##    after = []
##    for name in networks_dict:
##        print(name)
##        G0 = read_any(name)
##        before.append(nx.transitivity(G0))
##
##
##        G = make_configMod(G0)
##        after.append(nx.transitivity(G))
##
##    for i,name in enumerate(networks_dict.keys()):
##        print(name.ljust(15), "\t", before[i], "\t", after[i])
