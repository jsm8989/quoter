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

    # JOBNUM = 0
    # NUMJOBS = 1

    N = 200
    q = 0.5
    T = 1000
    k = 8
    alpha = 2
    trials_list = list(range(300))
    delta_list = np.arange(0,1.05,.05)

    params = itertools.product(delta_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for delta_alpha,trial in params:
        outdir = "../data_ER/"
        outfile = "N%i_k%i_q%0.1f_T%i_a%0.1f_delta%0.2f_sim%i.txt" % (N,k,q,T,alpha,delta_alpha,trial)
        if not os.path.isfile(os.path.join(outdir, outfile)): # avoid re-doing & overwriting
            G = nx.erdos_renyi_graph(N, k/(N-1)).to_directed() # bidirectional
            quoter_model_sim(G, q, T, alpha, delta_alpha, outdir, outfile)

            