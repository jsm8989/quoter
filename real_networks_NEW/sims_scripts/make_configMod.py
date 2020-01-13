# -*- coding: utf-8 -*-

# make_configMod.py
# Tyson Pond
# Last Modified: 2019-10-21

import networkx as nx
import numpy as np
from read_networks import *
import matplotlib.pyplot as plt
import random


def make_configMod(G):
    degree_seq = list(G.degree().values())
    if sum(degree_seq) % 2 != 0:
        degree_seq[0] += 1

    G=nx.configuration_model(degree_seq,create_using=nx.Graph())

    return G


def add_edges(G,n):
    """ Take a graph G and add n edges randomly """
    H = G.copy()
    nonedges = np.array(list(nx.non_edges(H)))
    to_add = np.random.choice(range(len(nonedges)), size=n, replace=False)
    H.add_edges_from(nonedges[to_add][:])
    return H

def add_triangles(G,n,max_tries):
    """ Take a graph G and add n edges which complete triangles.
        Of the edges which complete triangles, the edges are chosen at random.
        This implementation results in a random node having very high
        local clustering coefficient.
    """
    H = G.copy() 
    nodes = H.nodes()
    degree = list(H.degree().values())
    i_degree2plus = [i for i,deg in enumerate(degree) if deg >= 2] # index of nodes with degree >= 2
    np.random.shuffle(i_degree2plus)
    nonedges = list(map(set,nx.non_edges(H))) # map to set so {u,v} = {v,u}
    count = 0 # number of edges added
    tries = 0 # number of "steps" tried
    for i1 in i_degree2plus:
        n1 = nodes[i1]
        nbrs = nx.neighbors(H,n1)
        np.random.shuffle(nbrs)
        for i2 in range(len(nbrs)-1):
            n2 = nbrs[i2]
            for i3 in range(i2+1,len(nbrs)):
                n3 = nbrs[i3]
                if {n2,n3} in nonedges:
                    H.add_edge(n2,n3)
                    nonedges.remove({n2,n3})
                    count += 1
                tries += 1
##                print(count,tries)
                if count >= n or tries >= max_tries:
                    return H
    return H


##def add_triangles2(G,n):
##    """ Take a graph G and add n edges which complete triangles.
##        Of the edges which complete triangles, the edges are chosen at random.
##        This implementation requires first building A HUGE list of all possible
##        edges that could be added (i.e. would complete a triangle),
##        and then randomly picking from this list. Not computationally feasible
##        even for small networks.
##    """
##    H = G.copy() 
##    nodes = H.nodes()
##    degree = list(H.degree().values())
##    i_degree2plus = [i for i,deg in enumerate(degree) if deg >= 2] # index of nodes with degree >= 2
##    nonedges = list(map(set,nx.non_edges(H))) # map to set so {u,v} = {v,u}
##    to_add = []
##    for i1 in i_degree2plus:
##        n1 = nodes[i1]
##        nbrs = nx.neighbors(H,n1)
##        for i2 in range(len(nbrs)-1):
##            n2 = nbrs[i2]
##            for i3 in range(i2+1,len(nbrs)):
##                n3 = nbrs[i3]
##                if {n2,n3} in nonedges:
##                    to_add.append((n2,n3))
##                    nonedges.remove({n2,n3})
##                print(i1,i2,i3)        
##    to_add = np.array(to_add)[np.random.choice(range(len(to_add)),size=n,replace=False)]
##    H.add_edges_from(to_add)
##    return H     



def add_triangles3(G,n):
    """ Take a graph G and add n edges which complete triangles.
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
        nbrs = nx.neighbors(H,n1)
        if len(nbrs) >= 2:
            n2,n3 = random.sample(nbrs,k=2)
            if (n2,n3) not in H.edges() and (n3,n2) not in H.edges():
                H.add_edge(n2,n3)
                count += 1
##        print(trial)
        trial += 1
    return H 

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
##                "UC Irvine": read_UC_Irvine

small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]





if __name__ == "__main__":
    for name in small_networks:
        print(name)
        G0 = read_any(name)
        nnodes = nx.number_of_nodes(G0)
        nedges = nx.number_of_edges(G0)
        n = min(int(nedges*0.25),len(list(nx.non_edges(G0))))
        G1 = add_edges(G0,n)
        G2 = add_triangles3(G0,n)
        print(nx.transitivity(G0),nx.density(G0))
        print(nx.transitivity(G1),nx.density(G1))
        print(nx.transitivity(G2),nx.density(G2))
    
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

