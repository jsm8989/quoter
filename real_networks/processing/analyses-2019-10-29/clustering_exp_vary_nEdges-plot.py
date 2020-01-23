import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

df1 = pd.read_csv("real_networks-links_only.csv")
df2 = pd.read_csv("CKM-links_only-EDGE.csv")
df3 = pd.read_csv("CKM-links_only-TRIANGLE.csv")

no_edges = df1["average_hx"].loc[df1["network"]=="CKM physicians"].values
plt.plot([0] + df2["epsilon"].values, no_edges + df2["average_hx"],'co-')
plt.plot([0] + df3["epsilon"].values, no_edges + df3["average_hx"],'ro-')
label2 = mlines.Line2D([], [], color='cyan', marker='o', linestyle='None',
                          markersize=6, label='Edge added randomly')
label3 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                          markersize=6, label='Triangle completion')
plt.legend(handles=[label2,label3])
plt.xlabel(r"Percent increase in number of edges, $\epsilon$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.show()
