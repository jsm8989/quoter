import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import os

fig, ax = plt.subplots(1,3,figsize=(8,4))

# (1,1): hx vs transitivity
os.chdir("small_world/processing")
data = pd.read_csv("small_world.csv")
plt.sca(ax[0])
plt.plot(data["C"],data["hx_avg"],'o-')
plt.xlabel("Transitivity")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")

### (1,2): ADDING EDGES VS TRIANGLES
os.chdir("../../real_networks/processing/analyses-2019-10-29")
df1 = pd.read_csv("real_networks-links_only.csv")
df2 = pd.read_csv("real_networks-links_only-EDGE.csv")
df3 = pd.read_csv("real_networks-links_only-TRIANGLE.csv")

plt.sca(ax[1])
for i in range(len(df1["network"].values)):
    t1 = df1["transitivity"].values[i]
    t2 = df2["transitivity"].values[i]
    t3 = df3["transitivity"].values[i]
    h1 = df1["average_hx"].values[i]
    h2 = df2["average_hx"].values[i]
    h3 = df3["average_hx"].values[i]
    plt.plot(t1,h1,"ko")
    plt.plot(t2,h2,"co")
    plt.plot(t3,h3,"ro")

    plt.plot([t2,t1,t3],[h2,h1,h3],"k-")
    
      
label1 = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
                          markersize=6, label='Real network')
label2 = mlines.Line2D([], [], color='cyan', marker='o', linestyle='None',
                          markersize=6, label='Edge added randomly')
label3 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                          markersize=6, label='Triangle completion')
plt.legend(handles=[label1,label2,label3])
plt.xlabel("Transitivity")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")


# (1,3): vary the number of edges added
df1 = pd.read_csv("real_networks-links_only.csv")
df2 = pd.read_csv("CKM-links_only-EDGE.csv")
df3 = pd.read_csv("CKM-links_only-TRIANGLE.csv")

no_edges = df1["average_hx"].loc[df1["network"]=="CKM physicians"].values

eps1 = np.append([0],df2["epsilon"].values)
eps2 = np.append([0],df3["epsilon"].values)
hx1 = np.append([no_edges],df2["average_hx"].values)
hx2 = np.append([no_edges],df3["average_hx"].values)

plt.sca(ax[2])
plt.plot(eps1, hx1, 'co-')
plt.plot(eps2, hx2, 'ro-')
label2 = mlines.Line2D([], [], color='cyan', marker='o', linestyle='None',
                          markersize=6, label='Edge added randomly')
label3 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                          markersize=6, label='Triangle completion')
plt.legend(handles=[label2,label3])
plt.xlabel(r"Percent increase in number of edges, $\epsilon$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")

plt.tight_layout()
plt.savefig("../../../figure3.pdf")
plt.show()





