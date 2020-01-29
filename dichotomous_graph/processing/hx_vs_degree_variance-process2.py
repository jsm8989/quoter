import numpy as np
import pandas as pd
import os

# There's something glitchy with this script. Works if you manually set
# N = [250] and rerun, but otherwise outputs a matrix of zeros.


# Uncomment this to process avg degree = 64
##k1_list = np.arange(4,36,4) # k1+k2=64
##k2_list = 64-np.arange(4,36,4)
##K = 64

k1_list = np.arange(2,18,2) # k1+k2=32
k2_list = 32-np.arange(2,18,2)
K = 32

k1k2_list = zip(k1_list,k2_list)

n_list = [250,500]
q = 0.9
T = 1000
trials_list = list(range(500))

for n in n_list:
    n1 = n2 = n
    data = np.zeros((7,len(k1_list)))
    for i,(k1,k2) in enumerate(k1k2_list):
        print(n,k1,k2)
        hx_list = []
        deg = 0
        dens = 0
        clus = 0
        count = 0
            
        for trial in trials_list:
                efile = "../data2/edge/N1%i_N2%i_k1%i_k2%i_q%0.1f_T%i_sim%i.txt" % (n1,n2,k1,k2,q,T,trial)
                gfile = "../data2/graph/N1%i_N2%i_k1%i_k2%i_q%0.1f_T%i_sim%i.txt" % (n1,n2,k1,k2,q,T,trial)

                if os.path.isfile(efile) and os.path.isfile(gfile):  
                        edata = pd.read_csv(efile, sep = " ")
                        gdata = pd.read_csv(gfile, sep = " ")
                        
                        hx_list.extend(edata["hx"].values)

                        deg += gdata["average_degree"].values[0]
                        dens += gdata["density"].values[0]
                        clus += gdata["transitivity"].values[0]
                        count += 1
                else:
                    print("no data", n, k1, k2, trial)

        data[0,i] = np.mean(hx_list)
        data[1,i] = np.var(hx_list)
        data[2,i] = dens/count
        data[3,i] = clus/count
        data[4,i] = deg/count
        data[5,i] = k1/k2
        data[6,i] = k1**2/4 + k2**2/4 - k1*k2/2

    df = pd.DataFrame({"hx_avg":data[0,:],"hx_var":data[1,:],
                  "density":data[2,:],"transitivity":data[3,:],
                  "average_degree":data[4,:],"degree_ratio":data[5,:],
                       "degree_variance":data[6,:]})

        
    df.to_csv("hx_dichotomous_n%i_k1k2%i.csv" % (n,K), index=False)

