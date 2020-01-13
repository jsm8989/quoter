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

    N = 200
    k = 6
    q = 0.9
    T = 1000
    q_list = [0, .2, .4, .6, .8, .9, .99, .999, .9999]
    lam_list = [1, 2, 4, 6, 8]
    p_list = [0,1]
    trials_list = list(range(150))
    
    params = itertools.product(q_list,lam_list,p_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for q,lam,p,trial in params:
        outdir = "../data_SW/"
        outfile = "N%i_p%0.1f_q%0.4f_lam%i_T%i_sim%i.txt" % (N,p,q,lam,T,trial)
        if not os.path.isfile(os.path.join(outdir, "edge", outfile)): # avoid re-doing & overwriting
            G0 = nx.watts_strogatz_graph(n=N,k=k,p=p)
            G = nx.DiGraph(G0) # convert to directed
            quoter_model_sim(G, q, lam, T, outdir, outfile)

            
