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

    p_list = np.arange(0, 1.01, 0.1)
    trials_list = list(range(300))
    
    params = itertools.product(p_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for p,trial in params:
        outdir = "../data_uniform/"
        outfile = "N%i_p%0.1f_q%0.1f_T%i_sim%i.txt" % (N,p,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, "edge", outfile)): # avoid re-doing & overwriting
            G0 = nx.watts_strogatz_graph(n=N,k=k,p=p)
            G = nx.DiGraph(G0) # convert to directed
            quoter_model_sim(G, q, T, outdir, outfile)

            
