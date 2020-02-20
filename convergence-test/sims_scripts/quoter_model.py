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
from collections import Counter

def words_to_tweets(words,times):
    # Convert (words,times) array to a smaller array of (tweets,times)  
    unique_times =  list(sorted(set(times)))
    tweets = []
    for unq_t in unique_times:
        tweet = [w for w,t in zip(words,times) if t == unq_t]
        tweets.append(tweet)

    return [(t,w) for t,w in zip(unique_times, tweets)]

def get_past_words_and_times(W1,T1,t2):
    prevW1 = []
    prevT1 = []
    for w1, t1 in zip(W1,T1):
        if t1 <= t2:
            prevW1.append(w1)
            prevT1.append(t1)
        else:
            break # no need to keep comparing times since the lists are ordered
    return prevW1,prevT1


def write_all_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """
    
    times_to_save = np.arange(1,1000,10)*nx.number_of_nodes(G)
    words_to_save = range(1,10+1)
    # since ER networks are random, we can just choose the first "N" as a random sample
    nodes_to_save = [1,2]

    # vocabulary distribution
    alpha = 1.5
    z = 1000
    vocab = np.arange(1,z+1)
    weights = vocab**(-alpha)
    weights /= weights.sum()
       
    with open(outdir + outfile, "a+") as f:
        f.write("node word time freq zipf\n") # header
        for n in nodes_to_save:
            for t in times_to_save:
                prev_words, _ = get_past_words_and_times(G.node[n]["words"],G.node[n]["times"],t)
                for w in words_to_save:
                    ct = Counter(prev_words)
                    freq_w = ct[w]/len(prev_words)
                    zipf_freq_w = weights[w-1] # word 1 corresponds to index 0 
                    f.write("%i %i %i %0.4f %0.4f\n" % (n, w, t, freq_w, zipf_freq_w))
    
def quoter_model_sim(G,q,T,outdir,outfile,write_data=write_all_data,dunbar=None):
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
        outdir (string) -- Name of directory for data to be stored in
        outfile (string) -- Name of file for this simulation
        write_data (function) -- Can specify what data to compute & write.
        dunbar (int or None) -- If int, limit in-degree to dunbar's number
    """      
    
    # vocabulary distribution
    alpha = 1.5
    z = 1000
    vocab = np.arange(1,z+1)
    weights = vocab**(-alpha)
    weights /= weights.sum()

    # limit IN-DEGREE to just dunbar's number
    if dunbar:
        for node in G.nodes():
            nbrs = G.predecessors(node) 
            if len(nbrs) > dunbar:
                    nbrs_rmv = random.sample(nbrs, len(nbrs) - dunbar)
                    G.remove_edges_from( [(nbr,node) for nbr in nbrs_rmv] )
    
    # create initial tweet for each user
    startWords = 20
    for node in G.nodes():
        newWords = np.random.choice(vocab, size=startWords, replace=True, p=weights).tolist()
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
            newWords = np.random.choice(vocab, size=tweetLength, replace=True, p=weights).tolist()

        G.node[node]["words"].extend(newWords)
        G.node[node]["times"].extend([t]*len(newWords))

    # save data
    write_data(G,outdir,outfile)

        



