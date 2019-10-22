import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

q = 0.5
T = 1000
trials_list = list(range(100))
nAB = 9

nA_list=np.arange(10,101,1)
nB_list=np.arange(10,101,1)
nAgrid, nBgrid = np.meshgrid(nA_list,nB_list)
nAparams = np.diag(np.fliplr(nAgrid))[:int((len(nA_list)-1)/2)+1]
nBparams = np.diag(np.fliplr(nBgrid))[:int((len(nA_list)-1)/2)+1]

datadir = "../data_fix_dens_vary_clus/"


# Plot 1 -- scatterplot of (ego degree,alter degree) colored by cross-entropy
hx_avg = np.zeros(len(nAparams))
C = np.zeros(len(nAparams))
for i,(nA,nB) in enumerate(zip(nAparams,nBparams)):
    hx_sum = 0
    count = 0
    for trial in trials_list:
        gfile = datadir + "graph/nA%i_nB%i_nAB%i_q%0.1f_T%i_sim%i.txt" % (nA,nB,nAB,q,T,trial)
        efile = datadir + "edge/nA%i_nB%i_nAB%i_q%0.1f_T%i_sim%i.txt" % (nA,nB,nAB,q,T,trial)

        gdata = pd.read_csv(gfile, sep = " ")
        edata = pd.read_csv(efile, sep = " ")

        hx1 = edata["hx"].loc[(edata["ego"] == 1) & (edata["alter"] == 0)].iloc[0]
        hx_sum += hx1
        count += 1
    
    hx_avg[i] = hx_sum/count
    C[i] = gdata["transitivity"].values[0]

df = pd.DataFrame({"nA":nAparams,"nB":nBparams,"transitivity":C,"hx":hx_avg})
df = df.to_csv("fix_density_vary_transitivity.csv",index=False)

