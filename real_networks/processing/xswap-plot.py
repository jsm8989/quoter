import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches

# load data
df1 = pd.read_csv("analyses-2019-10-29/real_networks-links_only.csv") #original
df2 = pd.read_csv("real_networks-xswap.csv") #xswap

# calculation for errorbar
def sample_var(x1,x2,n):
    return (n*x2 - n*np.power(x1,2))/(n-1)
var1 = sample_var(df1["average_hx"].values,df1["average_hxsquared"].values,df1["count"].values)
var2 = sample_var(df2["average_hx"].values,df2["average_hxsquared"].values,df2["count"].values)

for i in range(len(df1["network"].values)):
    t1 = df1["transitivity"].values[i]
    t2 = df2["transitivity"].values[i]
    h1 = df1["average_hx"].values[i]
    h2 = df2["average_hx"].values[i]
    
    plt.plot([t2,t1],[h2,h1],"r-")
    plt.errorbar(t1,h1,yerr=var1[i],fmt="ko")
    plt.errorbar(t2,h2,yerr=var2[i],fmt="ro")


label1 = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
                          markersize=6, label='Real network')
label2 = mlines.Line2D([], [], color='red', marker='o', linestyle='None',
                          markersize=6, label='x-swap')
plt.legend(handles=[label1,label2])
plt.xlabel("Transitivity")
plt.ylabel("Cross-entropy")
plt.show()
