import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

##k_list = np.round(np.logspace(0,3,21)[1:])
k_list = list(range(1,11))
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
##            file = "../data-smallk/%s_k%i_q%0.1f_T%i_sim%i.txt" % (graph,k,q,T,trial)
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



# PLOT for k=90,91,92,...100
##data = pd.read_csv("scaling-largek.csv")
##star = data.loc[(data["graph"]=="star") & (data["quote_length"]==5)]
##clique = data.loc[(data["graph"]=="clique") & (data["quote_length"]==5)]
##plt.plot(star["ego_degree"],star["total_matches"],'o-',label="star")
##plt.plot(clique["ego_degree"],clique["total_matches"],'o-',label="clique")
##plt.legend()
##plt.xlabel("ego degree")
##plt.ylabel("total matches (average per trial)")
####plt.xscale('log')
####plt.yscale('log')
##plt.show()


# PLOT for k=1,10,100,1000. This is messy
data = pd.read_csv("scaling-smallk.csv") # get k=1,10
data2 = pd.read_csv("scaling-largek.csv") # get k=100
data3 = pd.read_csv("scaling-k1000.csv") # get k=1000

ql = 5
star1 = data.loc[(data["ego_degree"] == 1) & (data["graph"]=="star") & (data["quote_length"]==ql)]
clique1 = data.loc[(data["ego_degree"] == 1) & (data["graph"]=="clique") & (data["quote_length"]==ql)]
star10 = data.loc[(data["ego_degree"] == 10) & (data["graph"]=="star") & (data["quote_length"]==ql)]
clique10 = data.loc[(data["ego_degree"] == 10) & (data["graph"]=="clique") & (data["quote_length"]==ql)]
star100 = data2.loc[(data2["ego_degree"] == 100) & (data2["graph"]=="star") & (data2["quote_length"]==ql)]
clique100 = data2.loc[(data2["ego_degree"] == 100) & (data2["graph"]=="clique") & (data2["quote_length"]==ql)]
star1000 = data3.loc[(data3["ego_degree"] == 1000) & (data3["graph"]=="star") & (data3["quote_length"]==ql)]
clique1000 = data3.loc[(data3["ego_degree"] == 1000) & (data3["graph"]=="clique") & (data3["quote_length"]==ql)]

stardeg = np.concatenate([star1["ego_degree"].values,
                          star10["ego_degree"].values,
                          star100["ego_degree"].values,
                          star1000["ego_degree"].values])
starmat = np.concatenate([star1["total_matches"].values,
                          star10["total_matches"].values,
                          star100["total_matches"].values,
                          star1000["total_matches"].values])
cliquedeg = np.concatenate([star1["ego_degree"].values,
                          star10["ego_degree"].values,
                          star100["ego_degree"].values,
                          star1000["ego_degree"].values])
cliquemat = np.concatenate([clique1["total_matches"].values,
                          clique10["total_matches"].values,
                          clique100["total_matches"].values,
                          clique1000["total_matches"].values])
starmat = np.divide(starmat,[1,10,100,1000])
cliquemat = np.divide(cliquemat,[1,10,100,1000])
##plt.plot(star1["ego_degree"],star1["total_matches"],'o-',label="star")
##plt.plot(clique["ego_degree"],clique["total_matches"],'o-',label="clique")
plt.plot(stardeg,starmat,'o-',label="star")
plt.plot(cliquedeg,cliquemat,'o-',label="clique")
plt.legend()
plt.xlabel("ego degree")
plt.ylabel("total matches (average per trial)")
plt.xscale('log')
##plt.yscale('log')
plt.show()


