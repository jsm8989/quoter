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
    nbrs = G.predecessors(0)
    hx_list = []
    ego_list = []
    alter_list = []
    for source in nbrs:
        ego_list.append(0)
        alter_list.append(source)
                          
        source = G.node[source]
        time_tweets_target = words_to_tweets(target["words"],target["times"])
        time_tweets_source = words_to_tweets(source["words"],source["times"])
        hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
        hx_list.append(hx)
        
        
    with open(os.path.join(outdir,outfile), "w") as f:
        f.write("alter ego hx\n")
        for i in range(len(hx_list)):
            f.write("%i %i %0.8f\n" % (alter_list[i], ego_list[i], hx_list[i]))
             
if __name__ == '__main__':
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1
    
    k = 50
    graph_dict = {"star": make_star, "clique": make_clique}
    q_list = np.arange(0,1.01,0.1) 
    T = 1000
    trials_list = list(range(500))

    params = itertools.product( list(graph_dict.keys()), q_list, trials_list )

    #parameters to keep for this job
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for graph,q,trial in params:
        k = int(k)
        outdir = "../data-vary-q/"
        outfile = "%s_k%i_q%0.1f_T%i_sim%i.txt" % (graph,k,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, outfile)): # avoid re-doing & overwriting
##            G = graph_dict[graph](k).to_directed()
            G = graph_dict[graph](k)
            quoter_model_sim(G, q, T, outdir, outfile, write_data)





