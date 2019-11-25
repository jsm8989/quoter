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

    length = 20
    width = 20
    q = 0.9
    T = 1000

    trials_list = list(range(300))
    
##    params = itertools.product(trials_list)
    params = trials_list
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for trial in params:
        outdir = "../data_grid/"
        outfile = "length%i_width%i_q%0.1f_T%i_sim%i.txt" % (length,width,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, "edge", outfile)): # avoid re-doing & overwriting
            G0 = nx.grid_graph(dim=[length,width])
            A = nx.adjacency_matrix(G0).todense()
            G1 = nx.from_numpy_matrix(A,create_using=nx.Graph())
            G = nx.DiGraph(G1) # convert to directed
            quoter_model_sim(G, q, T, outdir, outfile)

            
