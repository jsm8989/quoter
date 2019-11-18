import os, sys
from make_SBM import *
import random
import itertools

if __name__ == "__main__":

    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

    N = 1000
    p = 0.4
    # Mathematica code to generate this sequence:
    # Reverse[Table[\[Mu] /. NSolve[q[0.4, \[Mu], 1000] == K, \[Mu]], {K, 
    # 0.00, 0.40, 0.025}]]
    mu_seq = [0.0444, 0.0570857, 0.0705176, 0.0847636, 0.0999,
              0.116013, 0.1332, 0.151572, 0.171257, 0.1924, 0.215169,
              0.23976, 0.2664, 0.295357, 0.326945, 0.361543, 0.3996]
    trials_list = list(range(1000))
    
    params = trials_list
    params = [P for i,P in enumerate(params) if i % NUMJOBS == JOBNUM]

    for trial in params:
        make_growing_SBM(N,p,mu_seq,trial)



    
