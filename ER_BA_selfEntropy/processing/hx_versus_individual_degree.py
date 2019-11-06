import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

N = 100
q_list = [0.1,0.5,0.9]
T = 1000
trials_list = list(range(200))

##param_list = np.arange(5,51,5) # for ER
param_list = [ 3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA



### AVERAGE NODE ENTROPY VS INDIVIDUAL DEGREE k_i

##for q in q_list:
##    h_list = []
##    deg_list = []
##    for i,x in enumerate(param_list):
##        for trial in trials_list:
##            nfile = "../data_BA/node/N%i_m%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
##            if os.path.isfile(nfile):  
##                ndata = pd.read_csv(nfile, sep = " ")
##                
##                h_list.extend(ndata["h"].values)
##                deg_list.extend(ndata["indegree"].values)
##            
####        data[0,i] = np.mean(h_list)
##        
##        print(x, "done")
##    deg_unq = np.sort(np.unique(deg_list))
##    data = np.zeros((len(deg_unq),2))
##    for i,deg in enumerate(deg_unq):
##        data[i,0] = deg
##        data[i,1] = np.mean([h for h,d in zip(h_list,deg_list) if d==deg])
##        
##
##    df = pd.DataFrame({"degree":data[:,0],"h_avg":data[:,1]})
##    df = df.to_csv("h_BA_q%0.1f_degree.csv" % q,index=False)


### PLOT: DENSITY VERSUS AVERAGE NODE ENTROPY
ER1 = pd.read_csv("h_ER_q0.1_degree.csv")
ER2 = pd.read_csv("h_ER_q0.5_degree.csv")
ER3 = pd.read_csv("h_ER_q0.9_degree.csv")
BA1 = pd.read_csv("h_BA_q0.1_degree.csv")
BA2 = pd.read_csv("h_BA_q0.5_degree.csv")
BA3 = pd.read_csv("h_BA_q0.9_degree.csv")

fig, axes = plt.subplots(1, 3, figsize=(10,3), sharey=False)
axes = axes.flatten()
plt.sca(axes[0])
plt.plot(ER1["degree"],ER1["h_avg"],'ko',label="ER")
plt.plot(BA1["degree"],BA1["h_avg"],'ro',label="BA",alpha=0.3)
plt.xlabel("Degree")
plt.ylabel("Average node entropy")
plt.title(r"$q = 0.1$")
plt.legend()

plt.sca(axes[1])
plt.plot(ER2["degree"],ER2["h_avg"],'ko')
plt.plot(BA2["degree"],BA2["h_avg"],'ro',alpha=0.3)
plt.xlabel("Degree")
plt.title(r"$q = 0.5$")

plt.sca(axes[2])
plt.plot(ER3["degree"],ER3["h_avg"],'ko')
plt.plot(BA3["degree"],BA3["h_avg"],'ro',alpha=0.3)
plt.xlabel("Degree")
plt.title(r"$q = 0.9$")

plt.tight_layout()
plt.show()



