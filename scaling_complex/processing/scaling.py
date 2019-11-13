import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

##k_list = np.round(np.logspace(0,3,21)[1:])
k_list = list(range(90,101))
graphs = ["star","clique"]
q = 0.5
T = 1000
##trials_list = list(range(200))
trials_list = list(range(2000))

##df = []
##for graph in graphs:
##    for k in k_list:
##        QL_dict = {}
##        for trial in trials_list:
##            if trial % 500 == 0:
##                print(graph,k,trial)
##                
##            file = "../data-largek/%s_k%i_q%0.1f_T%i_sim%i.txt" % (graph,k,q,T,trial)
##            data = np.loadtxt(file, skiprows=1)
####            Ns = np.mean(data["total_matches"].values)
##
##
####            for QL,M in zip(data["quote_length"].values,data["total_matches"].values):
##            for QL,M in zip(data[:,1],data[:,2]):
##                if QL in QL_dict:
##                    QL_dict[QL] += M
##                else:
##                    QL_dict[QL] = M
##        
##        for QL in QL_dict:
##            QL_dict[QL] /= len(trials_list)
##
##        QL_sorted = {QL:QL_dict[QL] for QL in sorted(QL_dict.keys())}
##        df.extend([[graph,k,QL,M] for QL,M in zip(list(QL_sorted.keys()),list(QL_sorted.values()))])
##
##cols = ["graph","ego_degree","quote_length","total_matches"]
##pd_df = pd.DataFrame(data=df,columns=cols)
##pd_df[cols].to_csv("scaling-smallk.csv",index=False)




data = pd.read_csv("scaling-largek.csv")
star = data.loc[(data["graph"]=="star") & (data["quote_length"]==5)]
clique = data.loc[(data["graph"]=="clique") & (data["quote_length"]==5)]
plt.plot(star["ego_degree"],star["total_matches"],'o-',label="star")
plt.plot(clique["ego_degree"],clique["total_matches"],'o-',label="clique")
plt.legend()
plt.xlabel("ego degree")
plt.ylabel("total matches (average per trial)")
##plt.xscale('log')
##plt.yscale('log')
plt.show()


