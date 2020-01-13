import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

k1_list = np.arange(4,36,4)
n1 = n2 = 250
q = 0.9
T = 1000

trials_list = list(range(150))

# DENSITY VERSUS AVERAGE CROSS ENTROPY
##data = np.zeros((6,len(k1_list)))
##for i,k1 in enumerate(k1_list):
##    k2 = 64 - k1
##    print(k1)
##    hx_list = []
##    deg = 0
##    dens = 0
##    clus = 0
##    count = 0
##        
##    for trial in trials_list:
##            efile = "../data/edge/N1%i_N2%i_k1%i_k2%i_q%0.1f_T%i_sim%i.txt" % (n1,n2,k1,k2,q,T,trial)
##            gfile = "../data/graph/N1%i_N2%i_k1%i_k2%i_q%0.1f_T%i_sim%i.txt" % (n1,n2,k1,k2,q,T,trial)
##
##            if os.path.isfile(efile):  
##                    edata = pd.read_csv(efile, sep = " ")
##                    gdata = pd.read_csv(gfile, sep = " ")
##                    hx_list.extend(edata["hx"].values)
##
##                    deg += gdata["average_degree"].values[0]
##                    dens += gdata["density"].values[0]
##                    clus += gdata["transitivity"].values[0]
##                    count += 1
##
##    data[0,i] = np.mean(hx_list)
##    data[1,i] = np.var(hx_list)
##    data[2,i] = dens/count
##    data[3,i] = clus/count
##    data[4,i] = deg/count
##    data[5,i] = k1/k2
##
##df = pd.DataFrame({"hx_avg":data[0,:],"hx_std":data[1,:],
##              "density":data[2,:],"transitivity":data[3,:],
##              "average_degree":data[4,:],"degree_ratio":data[5,:]})
##df = df.to_csv("hx.csv",index=False)


data = pd.read_csv("hx.csv")
##plt.plot(data["degree_ratio"].values, data["average_degree"].values)
plt.plot(data["degree_ratio"].values, data["hx_std"].values)
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Variance of $h_\times$")
plt.show()
