import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

N = 200
q_list = [0.5]
T = 1000
trials_list = list(range(150))

k_list = np.arange(2,22,2)

# DENSITY VERSUS AVERAGE CROSS ENTROPY
##for q in q_list:
##        data = np.zeros((5,len(k_list)))
##        for i,x in enumerate(k_list):
##                print(q,x)
##                hx_list = []
##                deg = 0
##                dens = 0
##                clus = 0
##                count = 0
##                
##                for trial in trials_list:
##                        efile = "../data_ER/edge/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
##                        gfile = "../data_ER/graph/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
##
##                        if os.path.isfile(efile):  
##                                edata = pd.read_csv(efile, sep = " ")
##                                gdata = pd.read_csv(gfile, sep = " ")
##                                hx_list.extend(edata["hx"].values)
##
##                                deg += gdata["average_degree"].values[0]
##                                dens += gdata["density"].values[0]
##                                clus += gdata["transitivity"].values[0]
##                                count += 1
##                               
##                                        ##    "nodes edges density average_degree min_indegree max_indegree " +
##                                        ##   "min_outdegree max_outdegree transitivity average_clustering " +
##                                        ##  "average_shortest_path_length assortativity "
##
##                data[0,i] = np.mean(hx_list)
##                data[1,i] = np.std(hx_list)
##                data[2,i] = dens/count
##                data[3,i] = clus/count
##                data[4,i] = deg/count
##
##        df = pd.DataFrame({"hx_avg":data[0,:],"hx_std":data[1,:],
##                      "density":data[2,:],"transitivity":data[3,:],
##                      "average_degree":data[4,:]})
##        df = df.to_csv("hx_ER_q%0.1f.csv" % q,index=False)

fig,ax = plt.subplots(1,3,figsize=(8,4),sharey=False)
for i,q in enumerate([1,0.9,0.5]):
    data = pd.read_csv("hx_ER_q%0.1f.csv" % q)
    plt.sca(ax[i])
    plt.plot(k_list,data["hx_avg"].values)
    if i == 1:
        plt.xlabel(r"$\langle k \rangle$")
    if i == 0:
        plt.ylabel(r"$\langle h_\times\rangle$")
    plt.title(r"Noise $1-q = %0.1f$" % (1-q))
plt.tight_layout()    
plt.show()
