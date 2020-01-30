import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import bltools as blt

dir1 = "small_world/processing"
dir2 = "real_networks/processing/analyses-2019-10-29"
dir3 = "real_networks/processing"

a = 1.25
fig = plt.figure(figsize=(8*a,5*a), constrained_layout=True)

gs = GridSpec(4, 6, figure=fig)

ax1 = fig.add_subplot(gs[0:2, 0:2])
ax2 = fig.add_subplot(gs[0:2, 2:4])
ax3 = fig.add_subplot(gs[0:2, 4:6])
ax4 = fig.add_subplot(gs[2:4, 0:2])
ax5 = fig.add_subplot(gs[2:4, 2:4])

ax6 = fig.add_subplot(gs[2, 4]) 
ax7 = fig.add_subplot(gs[2, 5]) 
ax8 = fig.add_subplot(gs[3, 4]) 
ax9 = fig.add_subplot(gs[3, 5]) 


# (1,1): Small world networks: hx vs rewiring probability
# ax1 = plt.subplot(2, 3, 1)
plt.sca(ax1)

N_list = [200,400]
k_list = [6,12]

N_style = ["C0", "C1"]
k_style = ["o-", "x-"]

# hx versus p
for i,N in enumerate(N_list):
    for j,k in enumerate(k_list):
        data = pd.read_csv(f"{dir1}/small_world_N%i_k%i_q0.5.csv" % (N,k))
        plt.plot(data["p"], data["hx_avg"], N_style[i] + k_style[j], label="%i, %i" % (N,k))
        
plt.xlabel(r"Rewiring probability, $p$")
plt.ylabel(r"$\langle h_\times \rangle$")
plt.xscale("log")
plt.legend(title=r"$N, k$", ncol=2, fontsize=9, labelspacing=0, handlelength=1, handletextpad=0.4, borderaxespad=0.25)



# (1,2): Real networks: vary the number of edges added in ``CKM physicians``
#ax2 = plt.subplot(2, 3, 2)
plt.sca(ax2)

df1 = pd.read_csv(f"{dir2}/real_networks-links_only.csv")
df2 = pd.read_csv(f"{dir2}/CKM-links_only-EDGE.csv")
df3 = pd.read_csv(f"{dir2}/CKM-links_only-TRIANGLE.csv")

no_edges = df1["average_hx"].loc[df1["network"]=="CKM physicians"].values

eps1 = np.append([0],df2["epsilon"].values)
eps2 = np.append([0],df3["epsilon"].values)
hx1 = np.append([no_edges],df2["average_hx"].values)
hx2 = np.append([no_edges],df3["average_hx"].values)

plt.plot(100*eps1, hx1, 'o-', color='c')
plt.plot(100*eps2, hx2, 'o-', color='r')
label2 = mlines.Line2D([], [], color='c', marker='o', linestyle='None',
                          markersize=6, label='Edges added randomly')
label3 = mlines.Line2D([], [], color='r', marker='o', linestyle='None',
                          markersize=6, label='Triangle completion')
plt.legend(handles=[label2,label3], fontsize=9, labelspacing=0, handlelength=1, handletextpad=0.4, borderaxespad=0.25, loc='lower right')
plt.xlabel(r"Percent increase in edges")
plt.ylabel(r"$\langle h_\times \rangle$")
plt.text(0.025, 0.925, "CKM Physicians", transform=ax2.transAxes)

### (1,3): Real networks: adding edges vs adding triangles
# ax3 = plt.subplot(2, 3, 3)
plt.sca(ax3)

df1 = pd.read_csv(f"{dir2}/real_networks-links_only.csv")
df2 = pd.read_csv(f"{dir2}/real_networks-links_only-EDGE.csv")
df3 = pd.read_csv(f"{dir2}/real_networks-links_only-TRIANGLE.csv")

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
plt.ylabel(r"$\langle h_\times \rangle$")

# (2,1): Real networks: x-swap
#ax4 = plt.subplot(2, 3, 4)
plt.sca(ax4)
df1 = pd.read_csv(f"{dir3}/real_networks-links_only.csv") #original
df2 = pd.read_csv(f"{dir3}/real_networks-xswap-5x.csv") #xswap

plt.plot(df1["average_hx"],df2["average_hx"],"o")
plt.plot(df1["average_hx"],df1["average_hx"],"-")
plt.xlabel(r"$\langle h_\times \rangle$ original")
plt.ylabel(r"$\langle h_\times \rangle$ x-swap")

# (2,2): Real networks: x-swap
#ax5 = plt.subplot(2, 3, 5)
plt.sca(ax5)
for j in range(len(df1["network"].values)):
        t1 = df1["transitivity"].values[j]
        t2 = df2["transitivity"].values[j]
        h1 = df1["average_hx"].values[j]
        h2 = df2["average_hx"].values[j]
        
        plt.plot([t2,t1],[h2,h1],"r-")
        plt.plot(t1,h1,"ko")
        plt.plot(t2,h2,"ro")
label1 = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
                                  markersize=6, label='Original network')
label2 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                          markersize=6, label='x-swap')
plt.legend(handles=[label1,label2], fontsize=9, labelspacing=0, handlelength=1, handletextpad=0.4, borderaxespad=0.25)
plt.ylabel(r"$\langle h_\times \rangle$")
plt.xlabel("Transitivity")

# (2,3): Real networks: x-swap
Ids = [17,18,23,24]
df1 = pd.read_csv(f"{dir3}/real_networks-links_only.csv") #original
df2 = pd.read_csv(f"{dir3}/real_networks-xswap-5x.csv") #xswap
stats = ["transitivity", "ASPL","Q", "degree_assortativity"]
labels = ["Transitivity", "ASPL", r"Modularity", "Assortativity"]
for stat,label,ax in zip(stats,labels,[ax6,ax7,ax8,ax9]):
    plt.sca(ax)
    plt.plot(df1[stat],df2[stat],'C0o')
    plt.plot(df1[stat],df1[stat],'C1-')
    plt.gca().set_title(label, fontsize=10, pad=-5)


blt.letter_subplots(axes=[ax1,ax2,ax3,ax4,ax5,ax6], xoffset=-0.2)
#plt.tight_layout(w_pad=0, h_pad=0)
##plt.savefig("figure3-clustering.pdf")
plt.show()


plt#plt.show()
