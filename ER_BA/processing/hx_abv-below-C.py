import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os

N = 100
q = 0.5
T = 1000

datadir = "../data_ER/"

trials_list = list(range(200))

param_list = np.arange(5,51,5) # for ER
##param_list = [3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA

def get_data(kind="above"):
    hx_avg = np.zeros(len(param_list))
    for i,x in enumerate(param_list):
        count = 0
        for trial in trials_list:
            nfile = datadir + "node/" + "N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
            efile = datadir + "edge/" + "N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
            gfile = datadir + "graph/" + "N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
            if os.path.isfile(nfile) and os.path.isfile(efile) and os.path.isfile(gfile):  
                ndata = pd.read_csv(nfile, sep = " ")
                edata = pd.read_csv(efile, sep = " ")
                gdata = pd.read_csv(gfile, sep = " ")
                
                egos = ndata["node"].values
                C = gdata["average_clustering"].values[0]
                
                for ego in egos:
                    ego_C = ndata["C"].loc[ndata["node"] == ego].iloc[0]

                    if kind == "above":
                        if ego_C > C:
                            ego_hxs = edata["hx"].loc[edata["ego"] == ego].values
                            hx_avg[i] += np.sum(ego_hxs)
                            count += len(ego_hxs)

                    else: 
                        if ego_C < C:
                            ego_hxs = edata["hx"].loc[edata["ego"] == ego].values
                            hx_avg[i] += np.sum(ego_hxs)
                            count += len(ego_hxs)

        hx_avg[i] /= count

        print("%0.2f percent done" % ((i+1)/(len(param_list)) ))
              

    return hx_avg

abv = get_data("above")
blw = get_data("below")
df=pd.DataFrame({"above_average_C": abv, "below_average_C": blw})
df = df.to_csv('hx_abv-blw-C_ER.csv', index=False)

    

