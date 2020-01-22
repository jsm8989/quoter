import os, sys
from make_SBM import *
from quoter_model import *
import random
import itertools
from edge_clustering_coeff import *
from modularity import *

def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """

    # graph skeleton for calculating clustering, transitivity, ASPL, etc.
    H = G.to_undirected()

    N = nx.number_of_nodes(G)
    m = int(N/2)
    A = range(0,m)
    B = range(m,N)
    
    edges = list(G.edges())
    random.shuffle(edges)

    w_sample = list()
    i = 0
    while len(w_sample) < 250:
        e = edges[i]
        if (e[0] in A and e[1] in A) or (e[0] in B and e[1] in B):
            w_sample.append(e)
        i += 1

    b_sample = list()
    i = 0
    while len(b_sample) < 250:
        e = edges[i]
        if (e[0] in A and e[1] in A) or (e[0] in B and e[1] in B):
            pass
        else:
            b_sample.append(e)
        i += 1

    full_sample = w_sample + b_sample
    
    sources = []
    targets = []
    quoteProba_list = []
    hx_list = []
##    dist_list = []
    triangles_list = []
    deg0_list = []
    deg1_list = []
    for e in full_sample:
        s = e[0]
        t = e[1]
        sources.append(s)
        targets.append(t)

        time_tweets_source = words_to_tweets(G.node[s]["words"],G.node[s]["times"])
        time_tweets_target = words_to_tweets(G.node[t]["words"],G.node[t]["times"])
        hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
        hx_list.append(hx)
        
        # also record quote probability
        if s in G.predecessors(t):
            quoteProba = 1/len(G.predecessors(t))
        else:
            quoteProba = 0
        quoteProba_list.append(quoteProba)

##        # also record distance between nodes
##        try:
##            dist = nx.shortest_path_length(G,source=s,target=t)
##        except:
##            dist = 0
##        dist_list.append(dist)
        
        # also record edge embeddeness & edge clustering coefficient
        triangles, deg0, deg1, _ = edge_clustering_coeff(H,e[0],e[1],return_info=True)
        triangles_list.append(triangles)
        deg0_list.append(deg0)
        deg1_list.append(deg1)
        
    # write edge data
    with open(outdir + "edge/" + outfile, "w") as f:
        f.write("alter ego quoteProb hx triangles alter_deg ego_deg\n") # header
        for i in range(len(targets)):
            f.write("%i %i %0.8f %0.8f %i %i %i\n" % (sources[i],targets[i],quoteProba_list[i], hx_list[i],
                                             triangles_list[i], deg0_list[i], deg1_list[i]))
    # compute graph data
    nnodes = nx.number_of_nodes(H)
    nedges = nx.number_of_edges(H)
    dens = nedges/(nnodes*(nnodes-1)/2)
    indegs = list(G.in_degree(G.nodes()).values())
    outdegs = list(G.out_degree(G.nodes()).values())
    ccs = sorted(nx.connected_components(H), key=len, reverse=True)    
    comm_dict = {x:0 for x in A}
    comm_dict.update({x:1 for x in B})
    Q = get_modularity(H,comm_dict)

    data_tuple = (nnodes,nedges,dens,np.mean(indegs), np.min(indegs), np.max(indegs),
                      np.min(outdegs), np.max(outdegs), nx.transitivity(H), nx.average_clustering(H),
                    nx.degree_assortativity_coefficient(H), 
                    len(ccs), len(ccs[0]),Q) # note avg_in == avg_out, so we only need to record one

    # write graph data
    with open(outdir + "graph/" + outfile, "w") as f:
        f.write("nodes edges density average_degree min_indegree max_indegree " +
                "min_outdegree max_outdegree transitivity average_clustering " +
                "assortativity " +
                "number_of_components largest_component modularity\n") # header
        
        f.write("%i %i %0.8f %0.8f %i %i %i %i %0.8f %0.8f %0.8f %i %i %0.6f" % data_tuple)

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
            
##    # write edgelist for SBM
##    nx.write_edgelist(G, os.path.join(outdir, "edgelist_" + outfile), delimiter=" ", data=False)

            


if __name__ == "__main__":

    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

    N = 100
    q = 0.9
    T = 1000
    alpha_list = [(2.0,1.5),(2.0,2.5),(2.0,2.0)]

    # this combination generates modularity = [-.20,-.15,-.10,...,.20,.25,.30]
    p_list = [0.0655977,0.0824176,0.102041,0.125232,0.153061,
              0.187075,0.229592,0.284257,0.357143,0.459184,0.612245]

    mu = 0.15
    
    trials_list = list(range(300))

    
    params = itertools.product(alpha_list,p_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for (alpha_A,alpha_B),p,trial in params:
        outdir = "../data-Jan20/"
        outfile = "N%i_p%0.2f_mu%0.2f_aA%0.1f_aB_%0.1f_q%0.1f_T%i_sim%i.txt" % (N,p,mu,alpha_A,alpha_B,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, "edge/", outfile)):
            G0 = make_SBM3(N,p,mu)
            G = nx.DiGraph(G0) # convert to directed
            quoter_model_sim(G, q, T,outdir, outfile,  alpha_A, alpha_B, write_data)



    
