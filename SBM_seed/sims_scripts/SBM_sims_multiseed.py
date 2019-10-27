import os, sys
from make_SBM import *
from quoter_model import *

def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """

    # compute edge data
    seeds = range(10)
    
    sources = []
    targets = []
    quoteProba_list = []
    hx_list = []
    dist_list = []
    for n1 in seeds:
        for n2 in G.nodes():
            if n1 != n2:
                sources.append(n1)
                targets.append(n2)
                
                time_tweets_target = words_to_tweets(G.node[n2]["words"],G.node[n2]["times"])
                time_tweets_source = words_to_tweets(G.node[n1]["words"],G.node[n1]["times"])
                hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
                hx_list.append(hx)
                
                # also record quote probability
                if n1 in G.predecessors(n2):
                    quoteProba = 1/len(G.predecessors(n2))
                else:
                    quoteProba = 0
                quoteProba_list.append(quoteProba)

                # also record distance between nodes
                try:
                    dist = nx.shortest_path_length(G,source=n1,target=n2)
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

    N = 100
    q_list = np.arange(0,0.21, 0.05)
    T = 1000
    trials_list = list(range(300))
    mu_list = np.arange(0.05,0.51,0.05)
    
    params = []
    for q in q_list:
        for mu in mu_list:
            for trial in trials_list:
                params.append((q,mu,trial))

    params = [(q,mu,trial) for i,(q,mu,trial) in enumerate(params) if i % NUMJOBS == JOBNUM]

    for q,mu,trial in params:
        outdir = "../data_vary_q-multiseed/"
        outfile = "N%i_mu%0.2f_q%0.2f_T%i_sim%i.txt" % (N,mu,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, outfile)):
            G = make_SBM_simple(N,mu).to_directed()
            quoter_model_sim(G, q, T, outdir, outfile, write_data)



    
