import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

k = 50
graphs = ["star","clique"]
q_list = np.arange(0,1.01,0.1)
T = 1000
trials_list = list(range(500))


##for graph in graphs:
##    hx_avg = []
##    hx_std = []
##    for q in q_list:
##        hx_trial = []
##        for trial in trials_list:
##            if trial % 100 == 0:
##                print(graph,q,trial)
##                
##            file = "../data-vary-q/%s_k%i_q%0.1f_T%i_sim%i.txt" % (graph,k,q,T,trial)
##            try:
##                data = pd.read_csv(file, sep = " ")
##            except:
##                print("no data", q, trial)
##            else:    
##                hx_trial.extend(data["hx"].values)
##            
##        hx_avg.append(np.mean(hx_trial))
##        hx_std.append(np.std(hx_trial))
##    df = pd.DataFrame(data={"q":q_list,"hx_avg":hx_avg,"hx_std":hx_std})
##    df = df.to_csv("scaling-hx-vs-q%s.csv" % graph,index=False)
##
##
star = pd.read_csv("scaling-hx-star-vs-q.csv")
clique = pd.read_csv("scaling-hx-clique-vs-q.csv")

plt.plot(q_list,star["hx_avg"],'o',label="star")
plt.plot(q_list,clique["hx_avg"],'o',label="clique")
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel("Average cross-entropy")
plt.legend()
plt.show()





