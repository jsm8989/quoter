import networkx as nx # version 1.11
import numpy as np
import math
import random
import os, sys
from quoter_model_uniform import *
import itertools

def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """

    # compute all cross entropies. e[0] = alter, e[1] = ego 
    time_tweets_target = words_to_tweets(G.node[1]["words"],G.node[1]["times"])
    time_tweets_source = words_to_tweets(G.node[0]["words"],G.node[0]["times"])

    # Experiment 1: usual cross-entropies
    hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
    # h_e = timeseries_cross_entropy(time_tweets_target, time_tweets_target, please_sanitize=False)
    # h_a = timeseries_cross_entropy(time_tweets_source, time_tweets_source, please_sanitize=False)

    # write cross-entropies
    with open(outdir + outfile, "w") as f:
        f.write("hx\n")
        f.write("%0.8f" % hx)
        # f.write("hx h_e h_a\n")
        # f.write("%0.8f %0.8f %0.8f" % (hx,h_e,h_a))

    # Experiment 2: write Lambdas
    # lambdas = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False, get_lambdas = True)
    # with open(outdir + outfile, "w") as f:
    #     f.write("lambda\n")
    #     for x in lambdas:
    #         f.write("%i\n" % x)


    # Experiment 3: write ``2nd order'' Lambdas
    # RR, RQ, QR, QQ = [], [], [], []
    # RRt, RQt, QRt, QQt = [], [], [], []

    # # get unique time indices
    # unq_times, unq_times_inds = [], []
    # for i,t in enumerate(G.node[1]["times"]):
    #     if t not in unq_times:
    #         unq_times.append(t)
    #         unq_times_inds.append(i)

    # # print(unq_times,unq_times_inds,G.node[1]["times"])
    # for ii,i in enumerate(unq_times_inds): # time index of first message
    #     if ii+1 < len(unq_times_inds): 
    #         t = G.node[1]["times"][i]
    #         L = lambdas[i]
    #         j = unq_times_inds[ii+1] # time index of second message
    #         if (G.node[1]["Q"][i] == 0) and (G.node[1]["Q"][j] == 0):
    #             RR.append(L)
    #             RRt.append(t)
    #         elif (G.node[1]["Q"][i] == 0) and (G.node[1]["Q"][j] == 1):
    #             RQ.append(L)
    #             RQt.append(t)
    #         elif (G.node[1]["Q"][i] == 1) and (G.node[1]["Q"][j] == 0):
    #             QR.append(L)
    #             QRt.append(t)
    #         elif (G.node[1]["Q"][i] == 1) and (G.node[1]["Q"][j] == 1):
    #             QQ.append(L)
    #             QQt.append(t)

    # with open(outdir + outfile, "w") as f:
    #     f.write("lambda time label\n")
    #     for i,(alist,blist) in enumerate(zip([RR,RQ,QR,QQ],[RRt,RQt,QRt,QQt])):
    #         if i == 0:
    #             label = "RR"
    #         elif i == 1:
    #             label = "RQ"
    #         elif i == 2:
    #             label = "QR"
    #         else:
    #             label = "QQ"
    #         for x,y in zip(alist,blist):
    #             f.write("%0.8f %i %s\n" % (x,y,label))

        
if __name__ == '__main__':
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

    # JOBNUM = 0
    # NUMJOBS = 1

    # Parameters from paper
    q_list = np.linspace(0,1,20)
    T = 1000
    lam_list = [3,6,9]
    z_list = [2,4,8]
    trials_list = list(range(100))

    # Parameters for 2nd order approx: QR, RQ, RR, QQ
    # q_list = [0.25, 0.5, 0.75]
    # T = 2000
    # lam_list = [3]
    # z_list = [8]
    # trials_list = list(range(300))

    # Testing out "longest run of heads" predictions for Lambda_R and Lambda_Q
    # q_list = [1] 
    # T = 20000
    # lam_list = [3]
    # z_list = [2,8]
    # trials_list= list(range(500))
    
    params = itertools.product(q_list,z_list,lam_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for q,z,lam,trial in params:
        z_alter = z_ego = z
        outdir = "../data_QMpaper-NEW/"
        outfile = "z%i_q%0.3f_T%i_lam%i_sim%i.txt" % (z,q,T,lam,trial)
        if not os.path.isfile(os.path.join(outdir, outfile)): # avoid re-doing & overwriting
            G = nx.DiGraph()
            G.add_edge(0,1)
            quoter_model_sim(G, q, T, lam, outdir, outfile, z_alter, z_ego, write_data)

            
