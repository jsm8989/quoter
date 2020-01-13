# -*- coding: utf-8 -*-

# add_triangle_sims.py
# Tyson Pond
# Last Modified: 2019-12-19

from quoter_model import *
from read_networks import *
from make_configMod import *
from edge_clustering_coeff import *
import os, sys
import numpy as np
import networkx as nx

def create_data_subdirs(datadir, subdirs):
    """ Create a directory for each real world network in which
        simulation data is stored.

        datadir (string) = name for root folder of real-world networks data
        subdirs (list of strings) = list of folder names of each real-world network
    """
    if not os.path.isdir(datadir):
        os.mkdir(datadir)
        
    for f in subdirs:
        path = os.path.join(datadir,f)
        if not os.path.isdir(path):
            os.mkdir(path)

            
def write_data(G,outdir,outfile,edge_sample_file):
    """
        Compute and write data from quoter model simulations.
    """

    # graph skeleton for calculating clustering, transitivity, ASPL, etc.
    H = nx.Graph(G)
    
    # compute edge data
    edges = []
    with open(edge_sample_file, "r") as f:
        for line in f:
            line = line.rstrip().split()
            edges.append((int(line[0]), int(line[1])))
    
    # compute edge data
    for e in edge_sample:
        # compute all cross entropies. e[0] = alter, e[1] = ego 
        time_tweets_target = words_to_tweets(G.node[e[1]]["words"],G.node[e[1]]["times"])
        time_tweets_source = words_to_tweets(G.node[e[0]]["words"],G.node[e[0]]["times"])
        hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
        G[e[0]][e[1]]["hx"] = hx

        # also record quote probability
        G[e[0]][e[1]]["quoteProb"] = 1/len(G.predecessors(e[1]))

        # also record edge embeddeness & edge clustering coefficient
        triangles, deg0, deg1, ECC = edge_clustering_coeff(H,e[0],e[1],return_info=True)
        G[e[0]][e[1]]["tri"] = triangles
        G[e[0]][e[1]]["deg0"] = deg0
        G[e[0]][e[1]]["deg1"] = deg1
##        G[e[0]][e[1]]["ECC"] = ECC


    # compute graph data
    nnodes = nx.number_of_nodes(H)
    nedges = nx.number_of_edges(H)
    dens = nedges/(nnodes*(nnodes-1)/2)
    indegs = list(G.in_degree(G.nodes()).values())
    outdegs = list(G.out_degree(G.nodes()).values())
    ccs = sorted(nx.connected_components(H), key=len, reverse=True)

##    try: # error is raised if graph is disconnected
##        avg_shortest_path = nx.average_shortest_path_length(H)
##    except:
##        avg_shortest_path = 0
    
    data_tuple = (nnodes,nedges,dens,np.mean(indegs), np.min(indegs), np.max(indegs),
                      np.min(outdegs), np.max(outdegs), nx.transitivity(H), nx.average_clustering(H), 
                    len(ccs), len(ccs[0])) # note avg_in == avg_out, so we only need to record one

    # write graph data -- ASPL, assortativity are not calculated
    with open(outdir + "graph/" + outfile, "w") as f:
        f.write("nodes edges density average_degree min_indegree max_indegree " +
                "min_outdegree max_outdegree transitivity average_clustering " +
                "number_of_components largest_component\n") # header
        
        f.write("%i %i %0.8f %0.8f %i %i %i %i %0.8f %0.8f %i %i" % data_tuple)

    # write edge data
    with open(outdir + "edge/" + outfile, "w") as f:
        f.write("alter ego quoteProb hx triangles alter_deg ego_deg\n") # header
        for e in edge_sample:
            f.write("%i %i %0.8f %0.8f %i %i %i\n" % (e[0], e[1], G[e[0]][e[1]]["quoteProb"], G[e[0]][e[1]]["hx"],
                                             G[e[0]][e[1]]["tri"],G[e[0]][e[1]]["deg0"],G[e[0]][e[1]]["deg1"]))


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

##    # write edgelist for configuration model
##    nx.write_edgelist(G, os.path.join(outdir, "edgelist_" + outfile), delimiter=" ", data=False)





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

small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]



if __name__ == '__main__':
##    create_data_subdirs("../data_clustering", small_networks)
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

    
    q = 0.5
    T = 1000
    trials_list = list(range(300))

    small_networks = ["CKM physicians"] ## 1 network -- how does number of edges change?
    epsilon_list = np.arange(0.05,0.41,0.05)
    
    params = []
    for name in small_networks:
        for eps in epsilon_list:
            for trial in trials_list:
                params.append((name,eps,trial))
            
    #parameters to keep for this job
    params = [(name,eps,trial) for i,(name,eps,trial) in enumerate(params) if i % NUMJOBS == JOBNUM]

    for name,eps,trial in params:
        outdir = os.path.join("../data/vary_n-edges", name)
        outfile = "TRIANGLE_%s_eps%0.2f_q%0.1f_T%i_sim%i.txt" % (name,eps,q,T,trial)
        efile = "%s_q%0.1f_T%i_sim%i.txt" % (name,0.5,1000,trial)
        edge_sample_file = os.path.join("../data/edge_sample", name, efile)
        if not os.path.isfile(os.path.join(outdir,outfile)):
            G0 = read_any(name)
            nedges = nx.number_of_edges(G0)
            n = min(int( nedges*eps ),len(list(nx.non_edges(G0))))
            G1 = add_triangles3(G0,n)
            G = nx.DiGraph(G1)
            quoter_model_sim(G, q, T, outdir, outfile, write_data, None, edge_sample_file)

