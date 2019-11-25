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
    edges = random.sample(G.edges(),min(500,nx.number_of_edges(G)))
    nonedges = random.sample(list(nx.non_edges(G)),min(500,len(list(nx.non_edges(G)))) )
    
    edge_sample = edges + nonedges
    alter_list, ego_list, qp_list, hx_list, dist_list=[],[],[],[],[]
    tri_list, alter_degs, ego_degs = [],[],[]

    for e in edge_sample:
        # compute cross entropies. e[0] = alter, e[1] = ego 
        time_tweets_target = words_to_tweets(G.node[e[1]]["words"],G.node[e[1]]["times"])
        time_tweets_source = words_to_tweets(G.node[e[0]]["words"],G.node[e[0]]["times"])
        hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
        hx_list.append(hx)
        alter_list.append(e[0])
        ego_list.append(e[1])

        # also record quote probability
        qp_list.append(1/len(G.predecessors(e[1])))

        # also record edge embeddeness & edge clustering coefficient
        triangles, deg0, deg1, ECC = edge_clustering_coeff(H,e[0],e[1],return_info=True)
        tri_list.append(triangles)
        alter_degs.append(deg0)
        ego_degs.append(deg1)

        # also record distance between nodes
        try:
            dist = nx.shortest_path_length(G,source=e[0],target=e[1])
        except:
            dist = -1
        dist_list.append(dist)
        
    # compute graph data
    nnodes = nx.number_of_nodes(H)
    nedges = nx.number_of_edges(H)
    dens = nedges/(nnodes*(nnodes-1)/2)
    indegs = list(G.in_degree(G.nodes()).values())
    outdegs = list(G.out_degree(G.nodes()).values())
    ccs = sorted(nx.connected_components(H), key=len, reverse=True)
    
    data_tuple = (nnodes,nedges,dens,np.mean(indegs), np.min(indegs), np.max(indegs),
                      np.min(outdegs), np.max(outdegs), nx.transitivity(H), nx.average_clustering(H),
                    nx.degree_assortativity_coefficient(H), 
                    len(ccs), len(ccs[0])) # note avg_in == avg_out, so we only need to record one

    # write graph data
    with open(outdir + "graph/" + outfile, "w") as f:
        f.write("nodes edges density average_degree min_indegree max_indegree " +
                "min_outdegree max_outdegree transitivity average_clustering " +
                "assortativity " +
                "number_of_components largest_component\n") # header
        
        f.write("%i %i %0.8f %0.8f %i %i %i %i %0.8f %0.8f %0.8f %i %i" % data_tuple)

    # write edge data
    with open(outdir + "edge/" + outfile, "w") as f:
        f.write("alter ego quoteProb hx distance triangles alter_deg ego_deg\n") # header
        for i in range(len(hx_list)):
            data_tuple = (alter_list[i],ego_list[i],qp_list[i],hx_list[i],dist_list[i],tri_list[i],alter_degs[i],ego_degs[i])
            f.write("%i %i %0.8f %0.8f %i %i %i %i\n" % data_tuple)
    
    # write node data
    with open(outdir + "node/" + outfile, "w") as f:
        f.write("node indegree outdegree C h\n") # header
        for node in G.nodes():
            time_tweets_target = words_to_tweets(G.node[node]["words"],G.node[node]["times"])
            time_tweets_source = words_to_tweets(G.node[node]["words"],G.node[node]["times"])
            h = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
            indeg = G.in_degree(node)
            outdeg = G.out_degree(node)
            C = nx.clustering(H, node)
            f.write("%i %i %i %0.8f %0.8f\n" % (node,indeg,outdeg,C,h))

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

        



