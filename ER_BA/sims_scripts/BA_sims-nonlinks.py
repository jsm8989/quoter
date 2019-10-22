# -*- coding: utf-8 -*-

# BA_sims.py
# Tyson Pond
# Last Modified: 2019-10-14

from quoter_model import *
import os, sys
import numpy as np
import networkx as nx

def read_edgelist(file):
    with open(file,"r") as f:
        skip = next(f)
        elist = []
        for line in f:
            line = line.rstrip().split()
            elist.append((int(line[0]),int(line[1])))
        G = nx.Graph()
        G.add_edges_from(elist)
    return G

def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """
    # compute edge data
    edges = []
    for node1 in G.nodes():
        for node2 in G.nodes():
            if node1 != node2:
                edges.append((node1,node2))

    np.random.shuffle(edges)
    edges = edges[:2000] # 2000 RANDOM EDGES
    
    quoteProba_list = []
    hx_list = []
    dist_list = []
    for e in edges: 
        # compute all cross entropies. e[0] = alter, e[1] = ego 
        time_tweets_target = words_to_tweets(G.node[e[1]]["words"],G.node[e[1]]["times"])
        time_tweets_source = words_to_tweets(G.node[e[0]]["words"],G.node[e[0]]["times"])
        hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
        hx_list.append(hx)
        
        # also record quote probability
        quoteProba = 1/len(G.predecessors(e[1]))
        quoteProba_list.append(quoteProba)
        
        # also record distance between nodes
        try:
            dist = nx.shortest_path_length(G,source=e[0],target=e[1])
        except:
            dist = -1
        dist_list.append(dist)

    
    # write edge data
    with open(os.path.join(outdir, outfile), "w") as f:
        f.write("alter ego quoteProb hx distance\n") # header
        for i,e in enumerate(edges):
            f.write("%i %i %0.8f %0.8f %i\n" % (e[0], e[1], quoteProba_list[i], hx_list[i], dist_list[i]))

if __name__ == '__main__':
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1
    
    q = 0.5
    T = 1000

    edgelists = next(os.walk("../data_BA/edge/"))[2]
    params = list(range(len(edgelists)))

    #parameters to keep for this job
    params = [filenum for i,filenum in enumerate(params) if i % NUMJOBS == JOBNUM]

    for filenum in params:
        elist = next(os.walk("../data_BA/edge/"))[2][filenum]
        outdir = "../data_BA-nonlinks/"
        outfile = elist
        if not os.path.isfile(os.path.join(outdir, outfile)): # avoid re-doing & overwriting
            G = read_edgelist(os.path.join("../data_BA/edge/",elist)).to_directed()
            quoter_model_sim(G, q, T, outdir, outfile, write_data)
          
