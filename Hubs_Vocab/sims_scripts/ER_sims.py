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

    N = 1000
    q = 0.5
    T = 1000

##    alpha_list = [(1.5,2.5),(2.5,1.5)]
    alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5),(1.5,2.0),(2.5,2.0)]

    k_list = np.arange(2,51,2)
    trials_list = list(range(200))
    
    params = itertools.product(k_list,alpha_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for k,(alpha,hub_alpha),trial in params:
        outdir = "../data_ER-Dec2/"
        outfile = "N%i_k%i_A%0.1f_HA%0.1f_q%0.1f_T%i_sim%i.txt" % (N,k,alpha,hub_alpha,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, "edge", outfile)): # avoid re-doing & overwriting
            G0 = nx.erdos_renyi_graph(N, k/(N-1))
            G = nx.DiGraph(G0) # convert to directed
            quoter_model_sim(G, q, T, outdir, outfile, alpha, hub_alpha)

            
