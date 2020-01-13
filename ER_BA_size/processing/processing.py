import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

N_list = [50,70,98,136,190,264,368,514,716,1000]
q = 0.5
T = 1000
trials_list = list(range(100))
k = 8

##x = k # ER
x = int(k/2) # BA

##data = np.zeros((5,len(N_list)))
##for i,N in enumerate(N_list):
##    hx_list = []
##    deg = 0
##    dens = 0
##    clus = 0
##    assort = 0
##    count = 0
##    for trial in trials_list:
##        efile = "../data_BA/edge/N%i_m%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
##        gfile = "../data_BA/graph/N%i_m%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
##        if os.path.isfile(efile):  
##            edata = pd.read_csv(efile, sep = " ")
##            gdata = pd.read_csv(gfile, sep = " ")
##            hx_list.extend(edata["hx"].values)
##
##            deg += gdata["average_degree"].values[0]
##            dens += gdata["density"].values[0]
##            clus += gdata["transitivity"].values[0]
##            count += 1
##    
##    data[0,i] = np.mean(hx_list)
##    data[1,i] = np.var(hx_list)
##    data[2,i] = dens/count
##    data[3,i] = clus/count
##    data[4,i] = deg/count
##    
##    print(N, "done")
##
##df = pd.DataFrame({"N":N_list,"hx_avg":data[0,:],"hx_var":data[1,:],
##                   "density":data[2,:],"transitivity":data[3,:],
##                   "average_degree":data[4,:]})
##df.to_csv("hx_BA.csv",index=False)

### PLOT: Network size vs average hx
ER = pd.read_csv("hx_ER.csv")
BA = pd.read_csv("hx_BA.csv")

fig,ax = plt.subplots(1,2,figsize=(10,4),sharey=False)

plt.sca(ax[0])
plt.plot(ER["N"],ER["hx_avg"],'ko',label="ER")
plt.plot(BA["N"],BA["hx_avg"],'ro',label="BA")
plt.xlabel(r"$N$")
plt.xscale("log")
plt.ylabel(r"$\langle h_\times \rangle$")
plt.legend()

plt.sca(ax[1])
plt.plot(ER["N"],ER["hx_var"],'ko')
plt.plot(BA["N"],BA["hx_var"],'ro')
plt.xlabel(r"$N$")
plt.xscale("log")
plt.ylabel("Variance cross-entropy")

plt.tight_layout()
plt.show()






