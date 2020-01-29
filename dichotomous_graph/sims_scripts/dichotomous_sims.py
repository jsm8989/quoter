import networkx as nx # version 1.11
import numpy as np
import math
import random
import os, sys
from quoter_model import *
import itertools

def make_dichotomous_graph(n1,n2,k1,k2):
    deg_seq = [k1]*n1 + [k2]*n2
    
    if sum(deg_seq) % 2 == 1:
        deg_seq[-1] += 1
    
    
    G = nx.configuration_model(deg_seq)

    # remove multiple edges
    G=nx.Graph(G)

    # remove self-loops
    G.remove_edges_from(G.selfloop_edges())

    return G


if __name__ == '__main__':
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

    k1_list = np.concatenate((np.arange(4,36,4),np.arange(2,18,2)))
    k2_list = np.concatenate((64-np.arange(4,36,4),32-np.arange(2,18,2)))
    k1k2 = zip(k1_list,k2_list)
    n_list = [250, 500]
    q = 0.9
    T = 1000

    trials_list = list(range(500))
    
    params = itertools.product(n_list,k1k2,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for n,(k1,k2),trial in params:
        n1 = n2 = n
        outdir = "../data2/"
        outfile = "N1%i_N2%i_k1%i_k2%i_q%0.1f_T%i_sim%i.txt" % (n1,n2,k1,k2,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, "edge", outfile)): # avoid re-doing & overwriting
            G0 = make_dichotomous_graph(n1,n2,k1,k2)
            G = nx.DiGraph(G0) # convert to directed
            quoter_model_sim(G, q, T, outdir, outfile)

            
