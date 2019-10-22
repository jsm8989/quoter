import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

N = 100
q = 0.5
T = 1000
trials_list = list(range(200))

param_list = np.arange(5,51,5) # for ER
##param_list = [ 3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA

data = np.zeros((10,len(param_list)))
for i,x in enumerate(param_list):
    hx_list1 = []
    hx_list2 = []
    hx_list3 = []
    hx_list4 = []
    hx_list5 = []
    deg = 0
    dens = 0
    ASPL = 0
    clus = 0
    assort = 0
    count = 0
    for trial in trials_list:
        efile = "../data_ER-nonlinks/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
        gfile = "../data_ER/graph/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
        if os.path.isfile(efile):  
            edata = pd.read_csv(efile, sep = " ")
            gdata = pd.read_csv(gfile, sep = " ")
            
            hx_list1.extend(edata["hx"].loc[edata["distance"]==1].values)
            hx_list2.extend(edata["hx"].loc[edata["distance"]==2].values)
            hx_list3.extend(edata["hx"].loc[edata["distance"]==3].values)
            hx_list4.extend(edata["hx"].loc[edata["distance"]==4].values)
            hx_list5.extend(edata["hx"].loc[edata["distance"]==5].values)
            
            deg += gdata["average_degree"].values[0]
            dens += gdata["density"].values[0]
            ASPL += gdata["average_shortest_path_length"].values[0]
            clus += gdata["transitivity"].values[0]
            assort += gdata["assortativity"].values[0]
            count += 1
            
    ##    "nodes edges density average_degree min_indegree max_indegree " +
    ##   "min_outdegree max_outdegree transitivity average_clustering " +
    ##  "average_shortest_path_length assortativity "
    
    data[0,i] = np.mean(hx_list1)
    data[1,i] = np.mean(hx_list2)
    data[2,i] = np.mean(hx_list3)
    data[3,i] = np.mean(hx_list4)
    data[4,i] = np.mean(hx_list5)
    data[5,i] = ASPL/count
    data[6,i] = dens/count
    data[7,i] = clus/count
    data[8,i] = assort/count
    data[9,i] = deg/count
    
    print(x, "done")

df = pd.DataFrame({"hx1":data[0,:],"hx2":data[1,:],"hx3":data[2,:],
                   "hx4":data[3,:],"hx5":data[4,:],"ASPL":data[5,:],
                   "density":data[6,:],"transitivity":data[7,:],
                   "assortativity":data[8,:],"average_degree":data[9,:]})
df = df.to_csv("hx_ER-Distance.csv",index=False)




