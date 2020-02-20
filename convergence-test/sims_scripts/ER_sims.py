import networkx as nx # version 1.11
import numpy as np
import math
import random
import os, sys
from quoter_model import *
import itertools

if __name__ == '__main__':

    N = 100
    q = 0.5
    T = 1000
    trial = 0
    k = 12
    
    outdir = "../data_ER/"
    outfile = "N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,k,q,T,trial)
    if not os.path.isfile(os.path.join(outdir, outfile)): # avoid re-doing & overwriting
        G = nx.erdos_renyi_graph(N, k/(N-1)).to_directed() # bidirectional
        quoter_model_sim(G, q, T, outdir, outfile)

            
