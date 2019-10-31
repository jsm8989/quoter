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
    
    # edges between
    eb_all = set(itertools.product(A,B))
    eb_present = eb_all & edges
    eb_sample = random.sample(eb_present,500)
    
    # edges within
    ew_all = set(itertools.combinations(A,2)) | set(itertools.combinations(B,2))
    ew_present = ew_all & edges
    ew_sample = random.sample(ew_present,500)
    
    sources = []
    targets = []
    quoteProba_list = []
    hx_list = []
    for e in eb_sample + ew_sample:
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
        
    # write edge data
    with open(outdir + outfile, "w") as f:
        f.write("alter ego quoteProb hx\n") # header
        for i in range(len(targets)):
            f.write("%i %i %0.8f %0.8f\n" % (sources[i],targets[i],quoteProba_list[i], hx_list[i]))
        
##    # write edgelist for SBM
##    nx.write_edgelist(G, os.path.join(outdir, "edgelist_" + outfile), delimiter=" ", data=False)

        
if __name__ == "__main__":

    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

    N = 2000
    M = 10000
    q_list = [0.5,0.1,0.9]
    T = 1000
    trials_list = list(range(300))
    mu_list = np.arange(0.05,0.51,0.05)
    
    params = itertools.product(q_list,mu_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for q,mu,trial in params:
        outdir = "../data_links/"
        outfile = "N%i_mu%0.2f_M%i_q%0.2f_T%i_sim%i.txt" % (N,mu,M,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, outfile)):
            G = make_SBM_simple(N,mu,M).to_directed()
            quoter_model_sim(G, q, T, outdir, outfile, write_data)



    
