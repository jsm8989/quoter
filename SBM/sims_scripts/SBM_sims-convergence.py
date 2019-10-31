import os, sys
from make_SBM import *
from quoter_model import *
import random
import itertools

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


def write_data(G,outdir,outfile):
    """
        Compute and write data from quoter model simulations.
    """

    # compute edge data
    seeds = [0] 

    times = np.array([100,200,300,400,500,1000,1500,2000])*nx.number_of_nodes(G)
    
    sources = []
    targets = []
    quoteProba_list = []
    hx_list = []
    dist_list = []
    times_list = []
    for n1 in seeds:
        nA = list(range(1,251))
        nB = list(range(int(N/2),250+int(N/2)))
##        for n2 in G.nodes():
        for n2 in nA + nB:
            if n1 != n2:
                # compute quote probability once
                if n1 in G.predecessors(n2):
                    quoteProba = 1/len(G.predecessors(n2))
                else:
                    quoteProba = 0
                    
                # compute distance once
                try:
                    dist = nx.shortest_path_length(G,source=n1,target=n2)
                except:
                    dist = -1
                        
                for t in times:
                    sources.append(n1)
                    targets.append(n2)
                    times_list.append(t)
                    quoteProba_list.append(quoteProba)
                    dist_list.append(dist)

                    past_target = get_past_words_and_times(G.node[n2]["words"],G.node[n2]["times"],t)
                    past_source = get_past_words_and_times(G.node[n1]["words"],G.node[n1]["times"],t) 
                    
                    time_tweets_target = words_to_tweets(*past_target)
                    time_tweets_source = words_to_tweets(*past_source)
                    hx = timeseries_cross_entropy(time_tweets_target, time_tweets_source, please_sanitize=False)
                    hx_list.append(hx)
                    
        
    # write edge data
    with open(outdir + outfile, "w") as f:
        f.write("alter ego time quoteProb hx distance\n") # header
        for i in range(len(targets)):
            f.write("%i %i %i %0.8f %0.8f %i\n" % (sources[i],targets[i],times_list[i],quoteProba_list[i], hx_list[i], dist_list[i]))
        
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
    q_list = [0.5]
    T = 2000
    trials_list = list(range(300))
    mu_list = np.arange(0.1,0.51,0.1)
    
    params = itertools.product(q_list,mu_list,trials_list)
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for q,mu,trial in params:
        outdir = "../data_convergence/"
        outfile = "N%i_mu%0.2f_M%i_q%0.2f_T%i_sim%i.txt" % (N,mu,M,q,T,trial)
        if not os.path.isfile(os.path.join(outdir, outfile)):
            G = make_SBM_simple(N,mu,M).to_directed()
            quoter_model_sim(G, q, T, outdir, outfile, write_data)



    
