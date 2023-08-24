import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import sys

sys.path.append(
    "/home/jimjam/Documents/Adelaide/quoter"
)  # regrettably using this quick fix
from real_networks.sims_scripts.read_networks import read_any, small_networks
from real_networks.sims_scripts.make_configMod import xswap

##attempts = list(range(10))


##assort_avg = []
##for i,name in enumerate(small_networks):
##    assort_trial = []
##    for attempt in attempts:
##        print(name,attempt)
##        G0 = read_any(name)
##        nedges = nx.number_of_edges(G0)
##        G = xswap(G0,nedges)
##        assort_trial.append(nx.degree_assortativity_coefficient(G))
##
##    assort_avg.append(np.mean(assort_trial))
##
### write to csv
##cols = ["degree_assortativity"]
##df_names = pd.DataFrame({"network": small_networks})
##df_stats = pd.DataFrame(data=assort_avg, columns=cols)
##df = pd.concat([df_names,df_stats],axis=1)
##df[["network"] + cols].to_csv("real_networks-xswap-assort.csv",index=False)
##

# TODO
df = pd.read_csv("transitivity-assortativity.csv")
df1 = df.loc[df["xswap"] == "no"]
df2 = df.loc[df["xswap"] == "yes"]

for j in range(len(df1["network"].values)):
    t1 = df1["degree_assortativity"].values[j]
    t2 = df2["degree_assortativity"].values[j]
    h1 = df1["average_hx"].values[j]
    h2 = df2["average_hx"].values[j]

    plt.plot([t2, t1], [h2, h1], "r-")
    plt.plot(t1, h1, "ko")
    plt.plot(t2, h2, "ro")


label1 = mlines.Line2D(
    [],
    [],
    color="black",
    marker="o",
    linestyle="None",
    markersize=6,
    label="Real network",
)
label2 = mlines.Line2D(
    [], [], color="red", marker="o", linestyle="None", markersize=6, label="x-swap"
)
plt.legend(handles=[label1, label2])
plt.xlabel("Assortativity")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.show()
