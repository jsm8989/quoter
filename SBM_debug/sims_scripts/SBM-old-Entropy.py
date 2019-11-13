import os, sys
from make_SBM import *
from quoter_model import *
import random
import itertools

def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """
    N = nx.number_of_nodes(G)
    m = int(N/2)
    A = range(0,m)
    B = range(m,N)
    
    edges = set(G.edges())
    
    # edges within
    W_all = set(itertools.combinations(A,2)) | set(itertools.combinations(B,2))
    W_edges = W_all & edges
    W_nonedges = W_all - W_edges
    W_edges_sample = random.sample(W_edges,min(250,len(W_edges)))

    # edges between
    B_all = set(itertools.product(A,B))
    B_edges = B_all & edges
    B_nonedges = B_all - B_edges
    B_edges_sample = random.sample(B_edges,min(250,len(B_edges)))

    full_sample = W_edges_sample + B_edges_sample 
    
    sources = []
    targets = []
    quoteProba_list = []
    hx_list = []
    dist_list = []
    for e in full_sample:
        s = e[0]
        t = e[1]
        sources.append(s)
        targets.append(t)

        time_tweets_source = words_to_tweets(G.node[s]["words"],G.node[s]["times"])
        time_tweets_target = words_to_tweets(G.node[t]["words"],G.node[t]["times"])
        hx = timeseries_cross_entropy_fix(time_tweets_target, time_tweets_source, please_sanitize=False)
        hx_list.append(hx)
        
        # also record quote probability
        if s in G.predecessors(t):
            quoteProba = 1/len(G.predecessors(t))
        else:
            quoteProba = 0
        quoteProba_list.append(quoteProba)

        # also record distance between nodes
        try:
            dist = nx.shortest_path_length(G,source=s,target=t)
        except:
            dist = -1
        dist_list.append(dist)
        
    # write edge data
    with open(outdir + outfile, "w") as f:
        f.write("alter ego quoteProb hx distance\n") # header
        for i in range(len(targets)):
            f.write("%i %i %0.8f %0.8f %i\n" % (sources[i],targets[i],quoteProba_list[i], hx_list[i], dist_list[i]))
            
##    # write edgelist for SBM
##    nx.write_edgelist(G, os.path.join(outdir, "edgelist_" + outfile), delimiter=" ", data=False)

        
if __name__ == "__main__":

    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

##    N = 2000
##    q_list = [0.5,0.1,0.9]
##    T = 1000
##    trials_list = list(range(300))
##    p = 0.01
##    mu_list = np.linspace(p/10, p, 10)

    N = 40
    q = 0.5
    T = 1000
    trials_list = list(range(50))
    p_list = [0.2,0.4,0.6,0.8]
    mu_list = [0.2,0.4,0.6,0.8]
    
    params = itertools.product(p_list,mu_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for p,mu,trial in params:
        outdir = "../data-old-Entropy/"
        outfile = "N%i_p%0.3f_mu%0.4f_q%0.2f_T%i_sim%i.txt" % (N,p,mu,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, outfile)):
            G = make_SBM3(N,p,mu).to_directed()
            quoter_model_sim(G, q, T, outdir, outfile, write_data)



    
