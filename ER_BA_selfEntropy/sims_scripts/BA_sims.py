# -*- coding: utf-8 -*-

# BA_sims.py
# Tyson Pond
# Last Modified: 2019-10-14

from quoter_model import *
import os, sys
import numpy as np
import networkx as nx
import itertools

# this function is to help find parameters 'm' such that the ACTUAL average
# degree (2m-2m^2/N) is actually close to the DESIRED average degree
def closest (num, arr):
    curr = arr[0]
    i = 0
    for j,val in enumerate(arr):
        if abs (num - val) < abs (num - curr):
            curr = val
            i = j
    return i


if __name__ == '__main__':
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1
    
    N = 100
    q = 0.5
    T = 1000

    q_list = [0.1, 0.5, 0.9]
    trials_list = list(range(200))

    # this whole block here is just to find 'm' such that the ACTUAL average
    # degree (2m-2m^2/N) is actually close to the DESIRED average degree. 
    # We could just loop over all 'actual k', but that would take longer
    desired_k = np.arange(5,51,5)
    m_list = np.arange(1,50.1,1) # candidate 'm's
    actual_k = [2*m-2*m**2/N for m in m_list] # actual degree for each candidate 'm'
    # for each desired k, find index of 'm' in m_list which has closest actual k
    ind = [closest(k,[2*m-2*m**2/N for m in m_list]) for k in desired_k]
    # best 'm's
    m_list = m_list[ind]
    print(m_list)

    
    params = itertools.product(q_list,m_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for q,m0,trial in params:
        m = int(m0)
        outdir = "../data_BA/"
        outfile = "N%i_m%i_q%0.1f_T%i_sim%i.txt" % (N,m,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, "edge", outfile)): # avoid re-doing & overwriting
            G = nx.barabasi_albert_graph(n=N,m=m).to_directed() # bidirectional
            quoter_model_sim(G, q, T, outdir, outfile)
          