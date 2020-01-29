import networkx as nx # version 1.11
import numpy as np
import math
import random
import os, sys
from quoter_model import *
import itertools

def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """

    # graph skeleton for calculating clustering, transitivity, ASPL, etc.
    H = nx.Graph(G)

    # compute edge data
    edge_sample = random.sample(G.edges(),min(500,nx.number_of_edges(G)))
    
    # compute edge data
    for e in edge_sample:
        # compute all cross entropies. e[0] = alter, e[1] = ego 
        time_tweets_target = words_to_tweets(G.node[e[1]]["words"],G.node[e[1]]["times"])
        time_tweets_source = words_to_tweets(G.node[e[0]]["words"],G.node[e[0]]["times"])
        hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
        G[e[0]][e[1]]["hx"] = hx

        # also record quote probability
        G[e[0]][e[1]]["quoteProb"] = 1/len(G.predecessors(e[1]))

        # also record edge embeddeness & edge clustering coefficient
        triangles, deg0, deg1, ECC = edge_clustering_coeff(H,e[0],e[1],return_info=True)
        G[e[0]][e[1]]["tri"] = triangles
        G[e[0]][e[1]]["deg0"] = deg0
        G[e[0]][e[1]]["deg1"] = deg1

    # write edge data
    with open(outdir + "edge/" + outfile, "w") as f:
        f.write("alter ego quoteProb hx triangles alter_deg ego_deg\n") # header
        for e in edge_sample:
            f.write("%i %i %0.8f %0.8f %i %i %i\n" % (e[0], e[1], G[e[0]][e[1]]["quoteProb"], G[e[0]][e[1]]["hx"],
                                             G[e[0]][e[1]]["tri"],G[e[0]][e[1]]["deg0"],G[e[0]][e[1]]["deg1"]))



if __name__ == '__main__':
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

    N = 200
    k = 6
    T = 1000
    q_list = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9] + [.99, .999, .9999]
    lam_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    p_list = [0,1]
    trials_list = list(range(100))
    
    params = itertools.product(q_list,lam_list,p_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for q,lam,p,trial in params:
        outdir = "../data_SW-NEW/"
        outfile = "N%i_p%0.1f_q%0.4f_lam%i_T%i_sim%i.txt" % (N,p,q,lam,T,trial)
        if not os.path.isfile(os.path.join(outdir, "edge", outfile)): # avoid re-doing & overwriting
            G0 = nx.watts_strogatz_graph(n=N,k=k,p=p)
            G = nx.DiGraph(G0) # convert to directed
            quoter_model_sim(G, q, lam, T, outdir, outfile, write_data=write_data)

            
