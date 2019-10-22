import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

N = 100
q = 0.5
T = 1000

trials_list = list(range(50))
nA = nB = 100
nAB_list = list(range(5,nA+1,5)) 


datadir = "../data_clustering/"

# Scatterplot of ego degree vs alter degree colored by cross-entropy
hx_avg = np.zeros(len(nAB_list))
for i,nAB in enumerate(nAB_list):
    hx_sum = 0
    count = 0
    for trial in trials_list:
        nfile = datadir + "node/nA%i_nB%i_nAB%i_q%0.1f_T%i_sim%i.txt" % (nA,nB,nAB,q,T,trial)
        efile = datadir + "edge/nA%i_nB%i_nAB%i_q%0.1f_T%i_sim%i.txt" % (nA,nB,nAB,q,T,trial)
        ndata = pd.read_csv(nfile, sep = " ")
        edata = pd.read_csv(efile, sep = " ")
        
        hx_sum += edata["hx"].loc[(edata["ego"] == 0) & (edata["alter"] == 1)].iloc[0]
        count += 1
        
    hx_avg[i] = hx_sum/count

df = pd.DataFrame({"nAB":nAB_list,"hx":hx_avg})
df = df.to_csv("fix_degree_vary_nAB.csv",index=False)



