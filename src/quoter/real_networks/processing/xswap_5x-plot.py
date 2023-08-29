import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

# load data
df1 = pd.read_csv("real_networks-links_only.csv") #original
df2 = pd.read_csv("real_networks-xswap-5x.csv") #xswap

plt.plot(df1["average_hx"],df2["average_hx"],"o")
plt.plot(df1["average_hx"],df1["average_hx"],"-")
plt.show()

stats = ["transitivity", "Q", "diameter", "ASPL"]

fig,ax = plt.subplots(2,2,figsize=(10,6),sharey=True)
ax = ax.flatten()
for i,stat in enumerate(stats):
    plt.sca(ax[i])
    for j in range(len(df1["network"].values)):
        t1 = df1[stat].values[j]
        t2 = df2[stat].values[j]
        h1 = df1["average_hx"].values[j]
        h2 = df2["average_hx"].values[j]
        
        plt.plot([t2,t1],[h2,h1],"r-")
        plt.plot(t1,h1,"ko")
        plt.plot(t2,h2,"ro")


    if i == 0:
        label1 = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
                                  markersize=6, label='Real network')
        label2 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                                  markersize=6, label='x-swap')
        plt.legend(handles=[label1,label2])
    plt.xlabel(stat)
    if  i in [0,2]:
        plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
        
plt.tight_layout()
plt.show()

# Transivity vs {density, modularity, diameter, ASPL}
stats = ["density", "Q", "diameter", "ASPL"]
fig,ax = plt.subplots(2,2,figsize=(10,6),sharey=False)
ax = ax.flatten()
for i,stat in enumerate(stats):
    plt.sca(ax[i])
    for j in range(len(df1["network"].values)):
        x = df1["transitivity"].values[j]
        y = df1[stat].values[j]        
        plt.plot(x,y,'ko')

    plt.ylabel(stat)
    if i in [2,3]:
        plt.xlabel("transitivity")
        
plt.tight_layout()
plt.show()


