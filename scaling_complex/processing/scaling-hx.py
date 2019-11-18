import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

k_list = np.round(np.logspace(0,3,11)[1:])
graphs = ["star","clique"]
q = 0.5
T = 1000
trials_list = list(range(500))


##for graph in graphs:
##    hx_avg = []
##    hx_std = []
##    for k in k_list:
##        hx_trial = []
##        for trial in trials_list:
##            if trial % 100 == 0:
##                print(graph,k,trial)
##                
##            file = "../data-hx/%s_k%i_q%0.1f_T%i_sim%i.txt" % (graph,k,q,T,trial)
##            try:
##                data = pd.read_csv(file, sep = " ")
##            except:
##                print("no data", k, trial)
##            else:    
##                hx_trial.extend(data["hx"].values)
##            
##        hx_avg.append(np.mean(hx_trial))
##        hx_std.append(np.std(hx_trial))
##    df = pd.DataFrame(data={"k":k_list,"hx_avg":hx_avg,"hx_std":hx_std})
##    df = df.to_csv("scaling-hx-%s.csv" % graph,index=False)


star = pd.read_csv("scaling-hx-star.csv")
clique = pd.read_csv("scaling-hx-clique.csv")

plt.plot(k_list[:-1],star["hx_std"].values[:-1],'o',label="star")
plt.plot(k_list[:-1],clique["hx_std"].values[:-1],'o',label="clique")
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel("Standard deviation cross-entropy")
plt.xscale('log')
plt.legend()
plt.show()





