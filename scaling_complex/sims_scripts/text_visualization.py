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
import pandas as pd
import matplotlib.pyplot as plt

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

def words_to_tweets(words,times):
    # Convert (words,times) array to a smaller array of (tweets,times)  
    unique_times =  list(sorted(set(times)))
    tweets = []
    for unq_t in unique_times:
        tweet = [w for w,t in zip(words,times) if t == unq_t]
        tweets.append(tweet)

    return [(t,w) for t,w in zip(unique_times, tweets)]

def write_data(G,outdir,outfile):

    with open(os.path.join(outdir,outfile),"w") as f:
        f.write("node time word\n")
        for node in G.nodes():
            for t,w in zip(G.node[node]["times"],G.node[node]["words"]):
                f.write("%i %i %i\n" % (node,t,w))

if __name__ == '__main__':
    pass
####    try:
####        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
####    except IndexError:
####        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )
##
##    JOBNUM = 0
##    NUMJOBS = 1
##
##    k_list = [5]
##    graph_dict = {"star": make_star, "clique": make_clique}
##    q = 0.5
##    T = 1000
##    trials_list = [0]
##
##    params = itertools.product( list(graph_dict.keys()), k_list, trials_list )
##
##    #parameters to keep for this job
##    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]
##
##    for graph,k,trial in params:
##        k = int(k)
##        outdir = "../text_visualization/"
##        outfile = "%s_k%i_q%0.1f_T%i_sim%i.txt" % (graph,k,q,T,trial)
##        if not os.path.isfile(os.path.join(outdir, outfile)): # avoid re-doing & overwriting
##            G = graph_dict[graph](k)
##            quoter_model_sim(G, q, T, outdir, outfile, write_data)
    k = 5
    q = 0.5
    T = 1000
    trial = 0
    graph = "star"
    file = "../text_visualization/%s_k%i_q%0.1f_T%i_sim%i.txt" % (graph,k,q,T,trial)
    data = pd.read_csv(file, delimiter = " ")

    # node to plot
    node = 0

    # Plot all words vs time
##    data = data.loc[data["node"] == node]
##    plt.plot(data["time"], data["word"],'ko')
##    plt.xlabel("time")
##    plt.ylabel("word")
##    plt.show()

    # Zoom in on words 1-9
    data = data.loc[(data["node"] == node) & (data["word"] <= 9)]
    plt.plot(data["time"].values, data["word"].values,'ko')
    plt.xlabel("time")
    plt.ylabel("word")
    plt.show()

