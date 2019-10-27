# -*- coding: utf-8 -*-

# big_networks_sims.py
# Tyson Pond
# Last Modified: 2019-10-21

from quoter_model import *
from read_networks import *
import os, sys
import numpy as np
import networkx as nx

def create_data_subdirs(datadir, subdirs):
    if not os.path.isdir(datadir):
        os.mkdir(datadir)
        
    for f in subdirs:
        path = os.path.join(datadir,f)
        if not os.path.isdir(path):
            os.mkdir(path)


def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """
    # compute edge data
    edges = []
    for node1 in G.nodes():
        for node2 in G.nodes():
            if node1 != node2:
                edges.append((node1,node2))
    
    np.random.shuffle(edges)
    edges = edges[:min(len(edges),2000)] # 2000 RANDOM EDGES
    
    quoteProba_list = []
    hx_list = []
    dist_list = []
    for e in edges: 
        # compute all cross entropies. e[0] = alter, e[1] = ego 
        time_tweets_target = words_to_tweets(G.node[e[1]]["words"],G.node[e[1]]["times"])
        time_tweets_source = words_to_tweets(G.node[e[0]]["words"],G.node[e[0]]["times"])
        hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
        hx_list.append(hx)
        
        # also record quote probability
        quoteProba = 1/len(G.predecessors(e[1]))
        quoteProba_list.append(quoteProba)
        
        # also record distance between nodes
        try:
            dist = nx.shortest_path_length(G,source=e[0],target=e[1])
        except:
            dist = -1
        dist_list.append(dist)

    # write edge data
    with open(os.path.join(outdir,outfile), "w") as f:
        f.write("alter ego quoteProb hx distance\n") # header
        for i,e in enumerate(edges):
            f.write("%i %i %0.8f %0.8f %i\n" % (e[0], e[1], quoteProba_list[i], hx_list[i], dist_list[i]))



networks_dict = {"Adolescent health": read_adolescent,
                "Arxiv CondMat": read_arxiv_CondMat,
##                "Arxiv GrQc": read_arxiv_GrQc,
                "CKM physicians": read_ckm,
                "Dolphins": read_dolphins,
                "Email Spain": read_email,
                "Email Enron": read_enron,
##                "Email Eu Core": read_Eu_Core,
                "Freeman's EIES": read_Freemans,
                "Golden Age": read_golden,
##                "Hypertext": read_hypertext,
                "Kapferer tailor": read_kapf,
                "Les Miserables": read_lesmis,
##                "Marvel": read_Marvel, 
                "Hollywood music": read_movies,
##                "Network science": read_netscience,
##                "NFL": read_NFL,
##                "Intra-organizational": read_org,
##                "Web of Trust": read_pgp,
                "Sampson's monastery": read_Sampson,
                "Terrorist": read_terrorist}
##                "UC Irvine": read_UC_Irvine

big_networks = ["Adolescent health", "Arxiv CondMat", "Email Enron"]


if __name__ == '__main__':
##    create_data_subdirs("../data", big_networks)
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

    
    q = 0.5
    T = 1000

    trials_list = list(range(500))

    params = []
    for name in big_networks:
        for trial in trials_list:
            params.append((name,trial))
            
    #parameters to keep for this job
    params = [(name,trial) for i,(name,trial) in enumerate(params) if i % NUMJOBS == JOBNUM]

    for name,trial in params:
        outdir = os.path.join("../data/", name)
        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
        if not os.path.isfile(os.path.join(outdir,outfile)):
            G = read_any(name).to_directed()
            quoter_model_sim(G, q, T, outdir, outfile, write_data)   

