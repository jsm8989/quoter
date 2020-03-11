# -*- coding: utf-8 -*-

# quoter_model.py
# Tyson Pond
# Last Modified: 2019-10-08

import networkx as nx # version 1.11
import numpy as np
import math
import random
import os, sys
from CrossEntropy import *
from edge_clustering_coeff import *

def words_to_tweets(words,times):
    # Convert (words,times) array to a smaller array of (tweets,times)  
    unique_times =  list(sorted(set(times)))
    tweets = []
    for unq_t in unique_times:
        tweet = [w for w,t in zip(words,times) if t == unq_t]
        tweets.append(tweet)

    return [(t,w) for t,w in zip(unique_times, tweets)]

def write_all_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """

    # graph skeleton for calculating clustering, transitivity, ASPL, etc.
    H = G.to_undirected()
    
    # compute edge data
    edge_sample = random.sample(G.edges(),min(300,nx.number_of_edges(G)))
    
    for e in edge_sample:
        # compute cross entropies. e[0] = alter, e[1] = ego 
        time_tweets_target = words_to_tweets(G.node[e[1]]["words"],G.node[e[1]]["times"])
        time_tweets_source = words_to_tweets(G.node[e[0]]["words"],G.node[e[0]]["times"])
        hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
        G[e[0]][e[1]]["hx"] = hx

        # also record quote probability
        G[e[0]][e[1]]["quoteProb"] = 1/len(G.predecessors(e[1]))

##        try: # error is raised if graph is disconnected
##        avg_shortest_path = nx.average_shortest_path_length(H)
##        except:
##        avg_shortest_path = 0

        # also record edge embeddeness & edge clustering coefficient
        triangles, deg0, deg1, ECC = edge_clustering_coeff(H,e[0],e[1],return_info=True)
        G[e[0]][e[1]]["tri"] = triangles
        G[e[0]][e[1]]["deg0"] = deg0
        G[e[0]][e[1]]["deg1"] = deg1
##        G[e[0]][e[1]]["ECC"] = ECC


    # write edge data
    with open(outdir + outfile, "w") as f:
        f.write("alter ego quoteProb hx triangles alter_deg ego_deg\n") # header
        for e in edge_sample:
            f.write("%i %i %0.8f %0.8f %i %i %i\n" % (e[0], e[1], G[e[0]][e[1]]["quoteProb"], G[e[0]][e[1]]["hx"],
                                             G[e[0]][e[1]]["tri"],G[e[0]][e[1]]["deg0"],G[e[0]][e[1]]["deg1"]))
    

def zipf_words(alpha,z,size):
    vocab = np.arange(1,z+1)
    weights = vocab**(-alpha)
    weights /= weights.sum()
    newWords = np.random.choice(vocab, size=size, replace=True, p=weights).tolist()
    return newWords

def quoter_model_sim(G,q,T,alpha,delta_alpha,outdir,outfile,write_data=write_all_data):
    """ Simulate the quoter model on a graph G. Nodes take turns generating content according to two
        mechanisms: (i) creating new content from a specified vocabulary distribution (ii) quoting
        from a neighbor's past text.

        [1] Bagrow, J. P., & Mitchell, L. (2018). The quoter model: A paradigmatic model of the social
        flow of written information. Chaos: An Interdisciplinary Journal of Nonlinear Science, 28(7),
        075304.

        G (networkx DiGraph) -- Directed graph to simulate quoter model on
        q (float) -- Quote probability
        T (int) -- Number of time-steps to simulate for. T=1000 really means 1000*nx.number_of_nodes(G),
                   i.e. each node will have 'tweeted' ~1000 times
        alpha (float) -- Mean Zipf exponent for everyone (must be > 0)
        delta_alpha (float) -- Zipf exponents are drawn uniformly from interval (alpha-delta_alpha,alpha+delta_alpha).
                            must have delta_alpha < alpha so that exponents are not negative. 
        outdir (string) -- Name of directory for data to be stored in
        outfile (string) -- Name of file for this simulation
        write_data (function) -- Can specify what data to compute & write.
    """      
    assert (alpha > 0) and (delta_alpha < alpha), print("require alpha > 0 and delta_alpha < alpha")
    # initialize vocabulary distributions
    z = 1000
    low = alpha-delta_alpha
    high = alpha+delta_alpha
    for node in G.nodes():
        G.node[node]["a"] = np.random.uniform(low, high)

    
    # create initial tweet for each user
    startWords = 20
    for node in G.nodes():
        newWords = zipf_words(G.node[node]["a"],z,startWords)
        G.node[node]["words"] = newWords
        G.node[node]["times"] = [0]*len(newWords)

    # simulate quoter model
    for t in range(1,T*nx.number_of_nodes(G)):
        node = random.choice(G.nodes())

        # length of tweet
        tweetLength = np.random.poisson(lam=3)

        # quote with probability q, provided ego has alters to quote from
        nbrs = G.predecessors(node) 
        if random.random() < q and len(nbrs) > 0:
            # pick a neighbor to quote from (simplifying assumption: uniformly at random from all neighbors)
            user_copied = random.choice(nbrs)

            # find a valid position in the neighbor's text to quote from
            words_friend = G.node[user_copied]["words"]
            numWords_friend = len(words_friend)
            copy_pos_start = random.choice( list(range(max( 0, numWords_friend-tweetLength))) )
            copy_pos_end = min( numWords_friend-1, copy_pos_start + tweetLength)
            newWords = words_friend[copy_pos_start: copy_pos_end]
            
        else: # new content
            newWords = zipf_words(G.node[node]["a"],z,tweetLength)

        G.node[node]["words"].extend(newWords)
        G.node[node]["times"].extend([t]*len(newWords))

    # save data
    write_data(G,outdir,outfile)

        



