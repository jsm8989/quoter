import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

N=200
k=6
p_list = np.concatenate(([0],np.logspace(-4,0,8)))  
trials = 3
stats=[]
for p in p_list:
	trial_clustering = []
	trial_ASPL = []
	for trial in range(trials):
		G = nx.watts_strogatz_graph(n=N,k=k,p=p)
		trial_clustering.append(nx.transitivity(G))
		trial_ASPL.append(nx.average_shortest_path_length(G))
	stats.append([np.mean(trial_clustering), np.mean(trial_ASPL)])

stats = np.array(stats)
df = pd.DataFrame(data={"p":p_list,"transitivity":stats[:,0],"ASPL":stats[:,1]})
df.to_csv("WattsStrogatz-SW-plot.csv",index=False)
plt.plot(p_list, stats[1:,0]/stats[0,0], 'o', label=r"$C(p)/C(0)$")
plt.plot(p_list, stats[1:,1]/stats[0,1], 'o', label=r"$L(p)/L(0)$")
print("clustering",stats[:,0])
print("ASPL",stats[:,1])
plt.legend()
plt.xlabel(r"$p$")
plt.xscale("log")
plt.show()
