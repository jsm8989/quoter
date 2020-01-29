from quoter_model import *
from read_networks import *
from make_configMod import *
from edge_clustering_coeff import *
import os, sys
import numpy as np
import networkx as nx
import community
from modularity import get_modularity

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

            
def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """
    edges = G.edges()
    n_edges_to_sample = min(len(edges),      500)
    edges_to_sample = np.array(edges)[np.random.choice(range(len(edges)),
                                                       size=n_edges_to_sample,
                                                       replace=False)]

    
    quoteProba_list = []
    hx_list = []
    dist_list = []
    triangles_list = []
    deg_u_list = []
    deg_v_list = []
    ECC_list = []

    H = G.to_undirected()
    for e in edges_to_sample:
        # compute all cross entropies. e[0] = alter, e[1] = ego
        
        time_tweets_target = words_to_tweets(G.node[e[1]]["words"],G.node[e[1]]["times"])
        time_tweets_source = words_to_tweets(G.node[e[0]]["words"],G.node[e[0]]["times"])
        hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
        hx_list.append(hx)
        
        
        # also record quote probability
        quoteProba = 1/len(G.predecessors(e[1]))
        quoteProba_list.append(quoteProba)


        # also record edge clustering info
        triangles, deg_u, deg_v, ECC = edge_clustering_coeff(H,e[0],e[1],return_info=True)
        triangles_list.append(triangles)
        deg_u_list.append(deg_u)
        deg_v_list.append(deg_v)
        ECC_list.append(ECC) 

    # compute graph data beforehand (it takes a long time)
    transitivity = nx.transitivity(H)
    avg_clustering = nx.average_clustering(H)
    diameter = nx.diameter(H)
    ASPL = nx.average_shortest_path_length(H)
    partition = community.best_partition(H)
    Q = get_modularity(H,partition)
    
    # write edge data
    with open(os.path.join(outdir,"edge_" + outfile), "w") as f:
        f.write("alter ego quoteProb hx triangles d_u d_v ECC\n") # header
        for i,e in enumerate(edges_to_sample):
            f.write("%i %i %0.8f %0.8f %i %i %i %0.4f\n" % (e[0], e[1], quoteProba_list[i], hx_list[i],
                                                triangles_list[i], deg_u_list[i], deg_v_list[i], ECC_list[i]))


    # write graph data (transitivity & average clustering)
    
    with open(os.path.join(outdir,"graph_" + outfile), "w") as f:
        f.write("transitivity average_clustering diameter ASPL Q\n")
        f.write("%0.4f %0.4f %i %0.4f %0.4f\n" % (transitivity,avg_clustering,
                                            diameter,ASPL,Q))
    # write edgelist for configuration model
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
##    create_data_subdirs("../data_xswap-5x", small_networks)
    
    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

    
    q = 0.9
    T = 1000
    trials_list = list(range(300))
    
    params = []
    for name in small_networks:
        for trial in trials_list:
            params.append((name,trial))
            
    #parameters to keep for this job
    params = [(name,trial) for i,(name,trial) in enumerate(params) if i % NUMJOBS == JOBNUM]

    for name,trial in params:
        outdir = os.path.join("../data-NEW/data_xswap-5x", name)
        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
        if not os.path.isfile(os.path.join(outdir,outfile)):
            G0 = read_any(name)
            nedges = nx.number_of_edges(G0)
            G1 = xswap(G0,5*nedges)
            G = nx.DiGraph(G1)
            quoter_model_sim(G, q, T, outdir, outfile, write_data, None)

