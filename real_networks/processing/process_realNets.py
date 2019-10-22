import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

q = 0.5
T = 1000
trials_list = list(range(100))

folders = next(os.walk("../data_real/"))[1]
##hx_list = np.zeros(len(folders))
##for i,folder in enumerate(folders):
##    hx_sum = 0
##    count = 0
##    for trial in trials_list:
##        efile = "../data_real/%s/edge/q%0.1f_T%i_sim%i.txt" % (folder,q,T,trial)
##        if os.path.isfile(efile):  
##            edata = pd.read_csv(efile, sep = " ")
##            hx_sum += np.sum(edata["hx"].values)
##            count += len(edata["hx"].values)
##            
##    hx_list[i] = hx_sum/count
##    
##    print(folder, "done")
##
##np.savetxt("hx_realnets.csv",hx_list)










def make_plot(stat,n):
    hx_list = np.loadtxt("hx_realnets.csv")
    plt.subplot(2,2,n)
    for i,folder in enumerate(folders):
        gfile = "../data_real/%s/graph/q%0.1f_T%i_sim0.txt" % (folder,q,T)
        gdata = pd.read_csv(gfile, sep = " ")

        statvalue = gdata[stat].values[0] 
    ##    "nodes edges density average_degree min_indegree max_indegree " +
    ##   "min_outdegree max_outdegree transitivity average_clustering " +
    ##  "average_shortest_path_length assortativity "
        plt.plot(statvalue,hx_list[i],'ko')
        plt.xlabel(stat)
        if n == 1 or n == 3:
            plt.ylabel("Mean cross-entropy")

fig = plt.figure()
make_plot("average_shortest_path_length",1)
make_plot("density",2)
make_plot("transitivity",3)
make_plot("assortativity",4)
plt.tight_layout()
plt.show()
    
