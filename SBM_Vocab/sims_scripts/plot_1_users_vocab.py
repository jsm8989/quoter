import os, sys
from make_SBM import *
from quoter_model import *
import random
import itertools
from edge_clustering_coeff import *
from modularity import *

def get_past_words_and_times(W1,T1,t2):
    prevW1 = []
    prevT1 = []
    for w1, t1 in zip(W1,T1):
        if t1 <= t2:
            prevW1.append(w1)
            prevT1.append(t1)
        else:
            break # no need to keep comparing times since the lists are ordered
    return prevW1,prevT1

def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """
    N = nx.number_of_nodes(G)
    # we'll look at user 0 in block A and user N-1 in block B
    W0 = G.node[0]["words"]
    T0 = G.node[0]["times"]
    W1 = G.node[N-1]["words"]
    T1 = G.node[N-1]["times"]

    with open(os.path.join(outdir,outfile),"w") as f:
        f.write("user time word\n")
        for t,w in zip(T0,W0):
            f.write("%i %i %i\n" % (0,t,w))
        for t,w in zip(T1,W1):
            f.write("%i %i %i\n" % (1,t,w))

if __name__ == "__main__":
    N = 2000
    M = 10000
    q = 0.9
    T = 1000
    mu_list = [0.05,0.5]
    trial = 0
    
    for mu in mu_list:
        outdir = "../1uservocab/"
        outfile = "N%i_mu%0.2f_M%i_q%0.1f_T%i_sim%i.txt" % (N,mu,M,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, outfile)):
            G0 = make_SBM_simple(N,mu,M)
            G = nx.DiGraph(G0) # convert to directed
            quoter_model_sim(G, q, T, outdir, outfile, write_data)



    
