import numpy as np
import pandas as pd
from read_networks import *
from make_configMod import *

##small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
##              "Golden Age", "Kapferer tailor", "Les Miserables",
##              "Hollywood music", "Sampson's monastery", "Terrorist"]
small_networks = ["CKM physicians", "Dolphins", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]
attempts = list(range(10))


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

df = pd.read_csv("transivity-assortativity.csv")
df1 = df[df.xswap=="no"]
df2 = df[df.xswap=="yes"]
for i,name in enumerate(small_networks):
    plt.plot(df2["degree_assortativity"].values-df1["degree_assortativity"].values,
             df2["transitivity"].values-df1["transitivity"].values,
             "ko")
plt.xlabel("Change in transitivity (xswap - original)")
plt.ylabel("Change in assortativity (xswap - original)")
plt.show()






