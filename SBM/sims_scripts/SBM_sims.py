import os, sys
from make_SBM import *
from quoter_model import *

if __name__ == "__main__":

    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

##    JOBNUM = 0
##    NUMJOBS = 1

    N = 60
    q = 0.5
    T = 1000
    trials_list = list(range(150))
    mu_list = np.arange(0.05,0.51,0.05)
    
    params = []
    for mu in mu_list:
        for trial in trials_list:
            params.append((mu,trial))

    params = [(mu,trial) for i,(mu,trial) in enumerate(params) if i % NUMJOBS == JOBNUM]

    for mu,trial in params:
        outdir = "../data/"
        outfile = "N%i_mu%0.2f_q%0.1f_T%i_sim%i.txt" % (N,mu,q,T,trial)
        G = make_SBM_simple(N,mu).to_directed()
        quoter_model_sim(G, q, T, outdir, outfile)



    
