import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

import bltools as blt

dir1 = "small_world/processing"
dir2 = "real_networks/processing/analyses-2019-10-29"

a = 1.2
fig, ax = plt.subplots(1,3,figsize=(8*a,3*a))

# (1,1): Small world networks: hx vs transitivity
SW = pd.read_csv(f"{dir1}/small_world.csv")
plt.sca(ax[0])
plt.plot(SW["C"],SW["hx_avg"],'o-')
plt.xlabel("Transitivity")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")


### (1,2): Real networks: adding edges vs adding triangles
df1 = pd.read_csv(f"{dir2}/real_networks-links_only.csv")
df2 = pd.read_csv(f"{dir2}/real_networks-links_only-EDGE.csv")
df3 = pd.read_csv(f"{dir2}/real_networks-links_only-TRIANGLE.csv")

plt.sca(ax[1])
for i in range(len(df1["network"].values)):
    t1 = df1["transitivity"].values[i]
    t2 = df2["transitivity"].values[i]
    t3 = df3["transitivity"].values[i]
    h1 = df1["average_hx"].values[i]
    h2 = df2["average_hx"].values[i]
    h3 = df3["average_hx"].values[i]
    plt.plot([t2,t1,t3],[h2,h1,h3],"k-")
    plt.plot(t1,h1,"o", color='black')
    plt.plot(t2,h2,"o", color='c')
    plt.plot(t3,h3,"o", color='r')

      
label1 = mlines.Line2D([], [], color='black', marker='o', linestyle='None', markersize=6, label='Original network')
label2 = mlines.Line2D([], [], color='c',  marker='o', linestyle='None', markersize=6, label='Edges added randomly')
label3 = mlines.Line2D([], [], color='r',   marker='o', linestyle='None', markersize=6, label='Triangle completion')
plt.legend(handles=[label1,label2,label3], fontsize=9, labelspacing=0, handlelength=1, handletextpad=0.4, borderaxespad=0.25)
plt.xlabel("Transitivity")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")


# (1,3): Real networks: vary the number of edges added
df1 = pd.read_csv(f"{dir2}/real_networks-links_only.csv")
df2 = pd.read_csv(f"{dir2}/CKM-links_only-EDGE.csv")
df3 = pd.read_csv(f"{dir2}/CKM-links_only-TRIANGLE.csv")

no_edges = df1["average_hx"].loc[df1["network"]=="CKM physicians"].values

eps1 = np.append([0],df2["epsilon"].values)
eps2 = np.append([0],df3["epsilon"].values)
hx1 = np.append([no_edges],df2["average_hx"].values)
hx2 = np.append([no_edges],df3["average_hx"].values)

plt.sca(ax[2])
plt.plot(100*eps1, hx1, 'o-', color='c')
plt.plot(100*eps2, hx2, 'o-', color='r')
label2 = mlines.Line2D([], [], color='c', marker='o', linestyle='None',
                          markersize=6, label='Edges added randomly')
label3 = mlines.Line2D([], [], color='r', marker='o', linestyle='None',
                          markersize=6, label='Triangle completion')
#plt.legend(handles=[label2,label3])
plt.xlabel(r"Percent increase in edges")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.text(0.025, 0.925, "CKM Physicians", transform=ax[2].transAxes)

blt.letter_subplots(axes=ax, xoffset=-0.275)
plt.tight_layout(w_pad=0.25)
plt.savefig("figure3.pdf")
##plt.show()





