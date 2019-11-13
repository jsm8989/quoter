# -*- coding: utf-8 -*-

# scaling_sims.py
# Tyson Pond
# Last Modified: 2019-11-05

import networkx as nx # version 1.11
import numpy as np
import math
import random
import os, sys
from quoter_model import *
import itertools
import collections

def make_star(k):
    """ important: 0 is the center, k neighbors (k+1 vertices in total) """
    G = nx.DiGraph()
    G.add_edges_from([(i,0) for i in range(1,k+1)])
    return G

def make_clique(k):
    """ k neighbors (k+1 vertices in total) """
    G = nx.DiGraph()

    # star part, edges only in 1 direction
    G.add_edges_from([(i,0) for i in range(1,k+1)])

    # clique part (bidirectional)
    edges1 = set(itertools.combinations(range(1,k+1),2))
    edges2 = set(e[::-1] for e in edges1)
    G.add_edges_from(edges1 | edges2)
    
    return G

def write_data(G,outdir,outfile):
    target = G.node[0]
    lenW = len(target["words"])

    data = []
    for t in target["quote_times"]:
        quote = [target["words"][i] for i in range(lenW) if target["times"][i]==t]
        total_matches = 0
        for i in range(1,nx.number_of_nodes(G)):
            source = G.node[i]
            
            matches = [1 for j in range(len(source["words"])-len(quote)-1) if source["words"][j:j+len(quote)] == quote]
            total_matches += sum(matches)
        data.append([t,len(quote),total_matches])

    with open(os.path.join(outdir,outfile),"w") as f:
        f.write("time quote_length total_matches\n")
        for line in data:
            f.write("%i %i %i\n" % (line[0],line[1],line[2]))

if __name__ == '__main__':
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1
##    k_list = [2,3,4]
    
##    k_list = np.round(np.logspace(0,3,21)[1:])
    k_list = [1000]
    graph_dict = {"star": make_star, "clique": make_clique}
    q = 0.5
    T = 1000
    trials_list = list(range(2000))

    params = itertools.product( list(graph_dict.keys()), k_list, trials_list )

    #parameters to keep for this job
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for graph,k,trial in params:
        k = int(k)
        outdir = "../data-k1000/"
        outfile = "%s_k%i_q%0.1f_T%i_sim%i.txt" % (graph,k,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, outfile)): # avoid re-doing & overwriting
##            G = graph_dict[graph](k).to_directed()
            G = graph_dict[graph](k)
            quoter_model_sim(G, q, T, outdir, outfile, write_data)





