import networkx as nx # version 1.11
import numpy as np
import math
import random
import os, sys
from quoter_model import *
import itertools

def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """

    
    # compute all cross entropies. e[0] = alter, e[1] = ego 
    time_tweets_target = words_to_tweets(G.node[1]["words"],G.node[1]["times"])
    time_tweets_source = words_to_tweets(G.node[0]["words"],G.node[0]["times"])
    hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
    h_e = timeseries_cross_entropy(time_tweets_target, time_tweets_target, please_sanitize=False)
    h_a = timeseries_cross_entropy(time_tweets_source, time_tweets_source, please_sanitize=False)

    # write data 
    with open(outdir + outfile, "w") as f:
        f.write("hx h_e h_a\n")
        f.write("%0.8f %0.8f %0.8f" % (hx,h_e,h_a))

if __name__ == '__main__':
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

    q_list = np.linspace(0,1,20)
    T = 1000
    lam_list = [3,6,9]
    
##    alpha_list = [(1.5,1.5),(1.5,2.0),(2.0,2.0),(2.5,2.0),(2.0,1.5),(2.0,2.5)]

    # these are the alpha's used in QM paper Figure 3 to get d=1/z in [2,4,8]
    alpha_list = [1.26501, 0.648447, 0.352434] 
    trials_list = list(range(100))
    
    params = itertools.product(q_list,alpha_list,lam_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for q,alpha,lam,trial in params:
        outdir = "../data/"
        alpha_alter=alpha_ego=alpha
        outfile = "Aa%0.1f_Ae%0.1f_q%0.3f_T%i_lam%i_sim%i.txt" % (alpha_alter,alpha_ego,q,T,lam,trial)
        if not os.path.isfile(os.path.join(outdir, outfile)): # avoid re-doing & overwriting
            G = nx.DiGraph()
            G.add_edge(0,1)
            quoter_model_sim(G, q, T, lam, outdir, outfile, alpha_alter, alpha_ego, write_data)

            
