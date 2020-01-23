import numpy as np
import pandas as pd
import os

small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]
q = 0.5
T = 1000
trials_list = list(range(300))


# Process data
data = np.zeros((len(small_networks),5))
for i,name in enumerate(small_networks):
    # get edge data
    count = 0
    for trial in trials_list:
        print(name,trial)
        efile = "../data_xswap/%s/edge_%s_q%0.1f_T%i_sim%i.txt" % (name,name,q,T,trial)
        gfile = "../data_xswap/%s/graph_%s_q%0.1f_T%i_sim%i.txt" % (name,name,q,T,trial)

        if os.path.isfile(efile) and os.path.isfile(gfile):
            edata = pd.read_csv(efile, sep = " ")
            gdata = pd.read_csv(gfile, sep = " ")

            data[i,0] += gdata["transitivity"].values[0]
            data[i,1] += gdata["average_clustering"].values[0]

            hx = edata["hx"].values
            data[i,2] += np.sum(hx)
            data[i,3] += np.sum(np.power(hx,2))
            count += len(hx)
        else:
            print("missing data", name, trial)

    data[i,:2] /= len(trials_list)
    data[i,[2,3]] /= count
    data[i,4] = count

# write to csv
cols = ["transitivity","average_clustering",
        "average_hx","average_hxsquared","count"]
df_names = pd.DataFrame({"network": small_networks})
df_stats = pd.DataFrame(data=data,columns=cols)
df = pd.concat([df_names,df_stats],axis=1)
df[["network"] + cols].to_csv("real_networks-xswap2.csv",index=False)






