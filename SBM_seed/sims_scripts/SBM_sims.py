import os, sys
from make_SBM import *
from quoter_model import *

def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """

    # write edge data
    with open(outdir + outfile, "w") as f:
        f.write("alter ego quoteProb hx\n") # header
        
        # compute edge data
        for node in G.nodes():
            time_tweets_target = words_to_tweets(G.node[node]["words"],G.node[node]["times"])
            time_tweets_source = words_to_tweets(G.node[0]["words"],G.node[0]["times"])
            hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)

            # also record quote probability
            if 0 in G.predecessors(node):
                quoteProba = 1/len(G.predecessors(node))
            else:
                quoteProba = 0

            f.write("%i %i %0.8f %0.8f\n" % (0, node, quoteProba, hx) )

if __name__ == "__main__":

    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

    N = 100
    q = 0.5
    T = 1000
    trials_list = list(range(500))
    mu_list = np.arange(0.05,0.51,0.05)
    
    params = []
    for mu in mu_list:
        for trial in trials_list:
            params.append((mu,trial))

    params = [(mu,trial) for i,(mu,trial) in enumerate(params) if i % NUMJOBS == JOBNUM]

    for mu,trial in params:
        outdir = "../data/"
        outfile = "N%i_mu%0.2f_q%0.1f_T%i_sim%i.txt" % (N,mu,q,T,trial)
        G0 = make_SBM_simple(N,mu)
        G = G0.to_directed()
        quoter_model_sim(G, q, T, outdir, outfile, write_data)



    
