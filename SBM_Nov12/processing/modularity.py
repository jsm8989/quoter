import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import scipy.stats
import random

N= 1000
q=0.5
T=1000
p_list = np.arange(0.1,0.71,0.1)
mu_list = np.arange(0.1,0.91,0.1)
trials_list = list(range(200))

##W = []
##B = []
##mod = []
##p_data = []
##mu_data = []
##for i,p in enumerate(p_list):
##    for j,mu in enumerate(mu_list):
##        print(i,j)
##        for trial in trials_list:
##            
##            efile = "../data/edge/N%i_p%0.3f_mu%0.4f_q%0.2f_T%i_sim%i.txt" % (N,p,mu,q,T,trial)
##            gfile = "../data/graph/N%i_p%0.3f_mu%0.4f_q%0.2f_T%i_sim%i.txt" % (N,p,mu,q,T,trial)
##            try:
##                edata = pd.read_csv(efile, sep = " ")
##                gdata = pd.read_csv(gfile, sep = " ")
##            except:
##                print("No data", p,mu,trial)
##
##            else:
##                
##                block1 = list(range(0,int(N/2)))
##                block2 = list(range(int(N/2),N))
##
##                tW = edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block1))].values.tolist()
##                tW.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block2))].values.tolist())
##                W.append(np.mean(tW))
##                tB = edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block2))].values.tolist()
##                tB.extend(edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block1))].values.tolist())
##                B.append(np.mean(tB))
##
##                mod.append(gdata["modularity"].values[0])
##                p_data.append(p)
##                mu_data.append(mu)
##df = pd.DataFrame(data={"p":p_data,"mu":mu_data,"hx_w":W,
##                        "hx_b":B,"modularity":mod})
##df = df.to_csv("sbm_q%0.1f_modularity.csv" % q, index=False)




## PLOT: modularity vs hx
data =  pd.read_csv("sbm_q%0.1f_modularity.csv" % q)
W = data["hx_w"].values
B = data["hx_b"].values
mod = data["modularity"].values
##sample = random.sample(range(len(mod)),1000) # take a sample
X = mod
Y = W
        
binned_stat = scipy.stats.binned_statistic
# nice builtin function!
y_bins,bin_edges, misc = binned_stat(X,Y, statistic="mean", bins=10)
x_bins = (bin_edges[:-1]+bin_edges[1:])/2

s_bins,bin_edges, misc = binned_stat(X,Y, statistic=np.std, bins=10)


plt.plot(X,Y, 'o', alpha=0.5)
plt.plot(x_bins, y_bins, "-", linewidth=3, markersize=12)

# Now, plot the std as errorbars! (check out the docstring)
plt.errorbar( x_bins, y_bins, yerr=s_bins,
fmt="none", # only show errorbars
elinewidth=5,
ecolor='C1',
zorder=5 # plot bars ABOVE scatter
)

plt.xlabel("Modularity, $Q$")
plt.ylabel("Average cross-entropy")
plt.title("Within edges")
plt.show()


# PLOT: modularity vs p,mu
##data =  pd.read_csv("sbm_q%0.1f_modularity.csv" % q)
##p_data = data["p"].values
##mu_data = data["mu"].values
##mod = data["modularity"].values
##plt.scatter(p_data,mu_data,c=mod,s=50,alpha=0.75)
##plt.xlabel("$p$")
##plt.ylabel("$\mu$")
##cb = plt.colorbar()
##cb.set_label("Modularity", rotation=270)
##plt.show()


