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

    N_list = [200,400]
    k_list = [6,12]
    q = 0.9
    T = 1000

    p_list = np.logspace(-4,0,8)
    trials_list = list(range(500))
    
    params = itertools.product(N_list,k_list,p_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for N,k,p,trial in params:
        outdir = "../data_clustering2/"
        outfile = "N%i_k%i_p%0.4f_q%0.1f_T%i_sim%i.txt" % (N,k,p,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, "edge", outfile)): # avoid re-doing & overwriting
            G0 = nx.watts_strogatz_graph(n=N,k=k,p=p)
            G = nx.DiGraph(G0) # convert to directed
            quoter_model_sim(G, q, T, outdir, outfile)

            
