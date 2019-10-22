import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import os

folders = ['Arxiv_ca-GrQc','adolescent_health','email_network','terrorists',
           'dolphins','lesmis','kapfdata','movies','Sampson','GoldenAge',
           'NFL2009_network','Freemans_EIES']
trials_list = list(range(100))

q = 0.5
T = 1000

hx_avg = np.zeros(len(folders))
hx_sd = np.zeros(len(folders))
for i,folder in enumerate(folders):
    hx_list = []
    for j,trial in enumerate(trials_list):
        efile = "../data_real/%s/edge/q%0.1f_T%i_sim%i.txt" % (folder,q,T,trial)
        try:
            edata = pd.read_csv(efile, sep = " ")
        except:
            pass
        else:
            hx_list.extend(edata["hx"].values)
            
    hx_avg[i] = np.mean(hx_list)
    hx_sd[i] = np.var(hx_list)
    print(folder, "done")

d = {"network":[f for f in folders],"hx_avg":[avg for avg in hx_avg],
      "hx_sd":[sd for sd in hx_sd]}     
df = pd.DataFrame(d)
df = df.to_csv("hx_real-networks.csv",index=False)








