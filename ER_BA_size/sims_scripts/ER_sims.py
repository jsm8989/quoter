# -*- coding: utf-8 -*-

# ER_sims.py
# Tyson Pond
# Last Modified: 2019-10-14

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

    N_list = [50,70,98,136,190,264,368,514,716,1000]
    k = 8
    q = 0.5
    T = 1000

    trials_list = list(range(100))
##    trials_list = list(range(200))
    
    params = itertools.product(N_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for N,trial in params:
        outdir = "../data_ER/"
        outfile = "N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,k,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, "edge", outfile)): # avoid re-doing & overwriting
            G0 = nx.erdos_renyi_graph(N, k/(N-1))
            G = nx.DiGraph(G0) # convert to directed
            quoter_model_sim(G, q, T, outdir, outfile)

            
