import os
import networkx as nx
import numpy as np
import random
import itertools
import quoter.quoter_model as qm
from processing.make_SBM import make_SBM_simple


## write edgelist for SBM
# nx.write_edgelist(G, os.path.join(outdir, "edgelist_" + outfile), delimiter=" ", data=False)


if __name__ == "__main__":
    N = 200
    M = 1000
    q = 0.5
    T = 1000
    mu_list = np.arange(0.05, 0.51, 0.05)
    trials_list = range(200)

    params_init = itertools.product(mu_list, trials_list)
    params = [P for i, P in enumerate(params_init)]

    for mu, trial in params:
        outdir = "output/"
        outfile = "N%i_mu%0.4f_M%i_q%0.2f_T%i_sim%i.txt" % (N, mu, M, q, T, trial)

        if not os.path.isfile(f"{outdir}edge-{outfile}"):
            G0 = make_SBM_simple(N, mu, M)
            G = nx.DiGraph(G0)  # convert to directed
            qm.quoter_model_sim(G, q, T, outdir, outfile, SBM_graph=True)
