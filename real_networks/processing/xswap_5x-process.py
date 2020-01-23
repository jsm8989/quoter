import numpy as np
import pandas as pd
import os
from read_networks import *
import community
from modularity import get_modularity

small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]
q = 0.5
T = 1000
trials_list = list(range(300))

def sample_var(x1,x2,n):
    return (n*x2 - n*np.power(x1,2))/(n-1)


# Process data
data = np.zeros((len(small_networks),8))
for i,name in enumerate(small_networks):
    # get edge data
    count = 0
    for trial in trials_list:
        print(name,trial)
        efile = "../data_xswap-5x/%s/edge_%s_q%0.1f_T%i_sim%i.txt" % (name,name,q,T,trial)
        gfile = "../data_xswap-5x/%s/graph_%s_q%0.1f_T%i_sim%i.txt" % (name,name,q,T,trial)

        if os.path.isfile(efile) and os.path.isfile(gfile):
            edata = pd.read_csv(efile, sep = " ")
            gdata = pd.read_csv(gfile, sep = " ")

            data[i,0] += gdata["transitivity"].values[0]
            data[i,1] += gdata["average_clustering"].values[0]
            data[i,2] += gdata["diameter"].values[0]
            data[i,3] += gdata["ASPL"].values[0]
            data[i,4] += gdata["Q"].values[0]

            hx = edata["hx"].values
            data[i,5] += np.sum(hx)
            data[i,6] += np.sum(np.power(hx,2))
            count += len(hx)
        else:
            print("missing data", name, trial)

    data[i,:5] /= len(trials_list)
    data[i,[5,6]] /= count
    data[i,7] = count

# write to csv
cols = ["transitivity","average_clustering","diameter","ASPL","Q",
        "average_hx","average_hxsquared","count"]
df_names = pd.DataFrame({"network": small_networks})
df_stats = pd.DataFrame(data=data,columns=cols)
df = pd.concat([df_names,df_stats],axis=1)
df[["network"] + cols].to_csv("real_networks-xswap-5x.csv",index=False)


# Calculate diameter & modularity for original real networks since we never did this
##data = np.zeros((len(small_networks),2))
##for i,network in enumerate(small_networks):
##    print(network)
##    H = read_any(network)
##    data[i,0] = nx.diameter(H)
##    partition = community.best_partition(H)
##    data[i,1] = get_modularity(H,partition)
##
##### write to csv
##cols = ["diameter","modularity"]
##df_names = pd.DataFrame({"network": small_networks})
##df_stats = pd.DataFrame(data=data,columns=cols)
##df = pd.concat([df_names,df_stats],axis=1)
##df[["network"] + cols].to_csv("real_networks-modularity.csv",index=False)
    







