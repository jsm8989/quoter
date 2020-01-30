import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import bltools as blt

dir1 = "small_world/processing"
dir2 = "real_networks/processing/analyses-2019-10-29"
dir3 = "real_networks/processing"

a = 1.25
fig = plt.figure(figsize=(8*a,5*a), constrained_layout=True)

gs = GridSpec(4, 4, figure=fig)

ax1 = fig.add_subplot(gs[0, 0:2]) # SW: hx vs p
ax2 = fig.add_subplot(gs[1, 0:2]) # WattsStrogatz
ax3 = fig.add_subplot(gs[0:2, 2:4]) # x-swap: hx vs transitivity + inset

# x-swap other properties
ax4 = fig.add_subplot(gs[2, 0]) 
ax5 = fig.add_subplot(gs[2, 1]) 
ax6 = fig.add_subplot(gs[3, 0]) 
ax7 = fig.add_subplot(gs[3, 1])

ax8 = fig.add_subplot(gs[2:4, 2:4]) # our clustering experiment


# Small world networks: hx vs rewiring probability
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
legend = plt.legend(title=r"$N, k$", ncol=2, fontsize=9,
           bbox_to_anchor=(0.35,0.37),
           prop={'size': 7}, labelspacing=0, handlelength=1, handletextpad=0.4, borderaxespad=0.25)
plt.setp(legend.get_title(),fontsize='small')

# Small world networks: Watts Strogatz plot
plt.sca(ax2)

WS = pd.read_csv(f"{dir1}/WattsStrogatz-SW-plot.csv")
T = WS["transitivity"].values[1:] / WS["transitivity"].values[0]
L = WS["ASPL"].values[1:] / WS["ASPL"].values[0]
plt.plot(WS["p"].values[1:], T, "o", label=r"$C(p)/C(0)$")
plt.plot(WS["p"].values[1:], L, "o", label=r"$L(p)/L(0)$")
plt.xscale("log")
plt.xlabel(r"Rewiring probability, $p$")
plt.legend()

### (1,2): Real networks: vary the number of edges added in ``CKM physicians``
##df1 = pd.read_csv(f"{dir2}/real_networks-links_only.csv")
##df2 = pd.read_csv(f"{dir2}/CKM-links_only-EDGE.csv")
##df3 = pd.read_csv(f"{dir2}/CKM-links_only-TRIANGLE.csv")
##
##no_edges = df1["average_hx"].loc[df1["network"]=="CKM physicians"].values
##
##eps1 = np.append([0],df2["epsilon"].values)
##eps2 = np.append([0],df3["epsilon"].values)
##hx1 = np.append([no_edges],df2["average_hx"].values)
##hx2 = np.append([no_edges],df3["average_hx"].values)
##
##plt.plot(100*eps1, hx1, 'o-', color='c')
##plt.plot(100*eps2, hx2, 'o-', color='r')
##label2 = mlines.Line2D([], [], color='c', marker='o', linestyle='None',
##                          markersize=6, label='Edges added randomly')
##label3 = mlines.Line2D([], [], color='r', marker='o', linestyle='None',
##                          markersize=6, label='Triangle completion')
##plt.legend(handles=[label2,label3], fontsize=9, labelspacing=0, handlelength=1, handletextpad=0.4, borderaxespad=0.25, loc='lower right')
##plt.xlabel(r"Percent increase in edges")
##plt.ylabel(r"$\langle h_\times \rangle$")
##plt.text(0.025, 0.925, "CKM Physicians", transform=ax2.transAxes)




# Real networks: x-swap
plt.sca(ax3)
df1 = pd.read_csv(f"{dir3}/real_networks-links_only.csv") #original
df2 = pd.read_csv(f"{dir3}/real_networks-xswap-5x.csv") #xswap

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

dd = 0.02
dx,dy = 0.07+dd, -0.13+dd
a = a/2
wi,hi = a*0.4-dd,a*0.4*0.8-dd
axins = inset_axes(ax3, width="100%", height="100%",
           bbox_to_anchor=(.65+dx, .3+dy, wi,hi),
           bbox_transform=ax3.transAxes, loc="center")
plt.plot(df1["average_hx"],df2["average_hx"],"o")
plt.plot(df1["average_hx"],df1["average_hx"],"-")
plt.xlabel(r"original")
plt.ylabel(r"x-swap")
plt.annotate(r"$\langle h_\times \rangle$", (3.235, 3.3))
##plt.title(r"$\langle h_\times \rangle$")

# Real networks: x-swap properties
df1 = pd.read_csv(f"{dir3}/real_networks-links_only.csv") #original
df2 = pd.read_csv(f"{dir3}/real_networks-xswap-5x.csv") #xswap
stats = ["transitivity", "ASPL","Q", "degree_assortativity"]
labels = ["Transitivity", "ASPL", r"Modularity", "Assortativity"]
for stat,label,ax in zip(stats,labels,[ax4,ax5,ax6,ax7]):
    plt.sca(ax)
    plt.plot(df1[stat],df2[stat],'C0o')
    plt.plot(df1[stat],df1[stat],'C1-')
    plt.gca().set_title(label, fontsize=10, pad=-9)



### Real networks: adding edges vs adding triangles
plt.sca(ax8)

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


##blt.letter_subplots(axes=[ax1,ax2,ax3,ax4,ax5,ax6], xoffset=-0.2)
#plt.tight_layout(w_pad=0, h_pad=0)
plt.savefig("figure3tentative-clustering.pdf")
plt.show()


