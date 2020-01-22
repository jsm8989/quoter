import networkx as nx # version 1.11
import numpy as np
import math
import random
import os, sys
from quoter_model import *
import itertools

if __name__ == '__main__':
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

    N = 100
    q_list = [0, 0.1, .2, 0.3, .4, 0.5, .6, 0.7, .8, .9, .99, .999, .9999, 1]
    lam_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    k_list = [5, 10, 15, 20, 25]
    T = 1000
    trials_list = list(range(100))
    
    params = itertools.product(q_list,lam_list,k_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for q,lam,k,trial in params:
        outdir = "../data_ER/"
        outfile1 = "N%i_k%i_q%0.1f_lam%i_T%i_sim%i.txt" % (N,k,q,lam,T,trial)
        outfile = "N%i_k%i_q%0.4f_lam%i_T%i_sim%i.txt" % (N,k,q,lam,T,trial)
        b1 = os.path.isfile(os.path.join(outdir, "edge", outfile1))
        b2 = os.path.isfile(os.path.join(outdir, "edge", outfile))
        if not (b1 or b2): # avoid re-doing & overwriting
            G0 = nx.erdos_renyi_graph(N, k/(N-1))
            G = nx.DiGraph(G0) # convert to directed
            quoter_model_sim(G, q, lam, T, outdir, outfile)

            
