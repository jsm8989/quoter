import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

N = 100
q = 0.5
T = 1000
trials_list = list(range(200))

##param_list = np.arange(5,51,5) # for ER
param_list = [ 3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA

data = np.zeros((7,len(param_list)))
for i,x in enumerate(param_list):
    hx_list = []
    deg = 0
    dens = 0
    ASPL = 0
    clus = 0
    assort = 0
    count = 0
    for trial in trials_list:
        efile = "../data_BA/edge/N%i_m%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
        gfile = "../data_BA/graph/N%i_m%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
        if os.path.isfile(efile):  
            edata = pd.read_csv(efile, sep = " ")
            gdata = pd.read_csv(gfile, sep = " ")
            hx_list.extend(edata["hx"].values)

            deg += gdata["average_degree"].values[0]
            dens += gdata["density"].values[0]
            ASPL += gdata["average_shortest_path_length"].values[0]
            clus += gdata["transitivity"].values[0]
            assort += gdata["assortativity"].values[0]
            count += 1
            
    ##    "nodes edges density average_degree min_indegree max_indegree " +
    ##   "min_outdegree max_outdegree transitivity average_clustering " +
    ##  "average_shortest_path_length assortativity "
    
    data[0,i] = np.mean(hx_list)
    data[1,i] = np.std(hx_list)
    data[2,i] = ASPL/count
    data[3,i] = dens/count
    data[4,i] = clus/count
    data[5,i] = assort/count
    data[6,i] = deg/count
    
    print(x, "done")

df = pd.DataFrame({"hx_avg":data[0,:],"hx_std":data[1,:],"ASPL":data[2,:],
                   "density":data[3,:],"transitivity":data[4,:],
                   "assortativity":data[5,:],"average_degree":data[6,:]})
df = df.to_csv("hx_BA-1.csv",index=False)




