import numpy as np
import pandas as pd
import os

N = 200
k = 6
T = 1000
q_list = [0, .1, .2, .3, .4, .5, .6, .7, .8, .9] + [.99, .999, .9999]
lam_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
p_list = [0,1]
trials_list = list(range(100))

# q-lambda colored by hx
for p in p_list:
    data = np.zeros((len(q_list),len(lam_list)))
    for i,q in enumerate(q_list):
        for j,lam in enumerate(lam_list):
            print("starting: q%0.4f lambda%i" % (q,lam))
            hx_list = []
            for trial in trials_list:
                efile = "../data_SW-NEW/edge/N%i_p%0.1f_q%0.4f_lam%i_T%i_sim%i.txt" % (N,p,q,lam,T,trial)

                if os.path.isfile(efile):  
                        edata = pd.read_csv(efile, sep = " ")
                        hx_list.extend(edata["hx"].values)
                        
            data[i,j] = np.mean(hx_list)

    df = pd.DataFrame(data=data)
    df.to_csv("hx_SW-NEW_p%0.1f.csv" % p, header=False, index=False)





        
        
