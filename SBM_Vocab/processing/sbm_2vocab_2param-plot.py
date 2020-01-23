import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5)]
mu = 0.15

fig, ax = plt.subplots(1,3,figsize=(10,6),sharey=True)
for i,alpha in enumerate(alpha_list):
    plt.sca(ax[i])
    alpha_A = alpha[0]
    alpha_B = alpha[1]

    # load data
    data =  pd.read_csv("sbm_2param_aA%0.1f_aB%0.1f.csv" % (alpha_A,alpha_B))

    # what to plot on the x-axis? within-block connection prob, modularity, ?
    #x = data["p"].values
    x = np.linspace(-.2,.3,11)

    plt.plot(x,data["AB"].values,'o-',label=r"$h_\times(A|B)$") # these are reversed oops
    plt.plot(x,data["BA"].values,'o-',label=r"$h_\times(B|A)$") # ...
    plt.plot(x,data["AA"].values,'o-',label=r"$h_\times(A|A)$")
    plt.plot(x,data["BB"].values,'o-',label=r"$h_\times(B|B)$")
    plt.plot(x,data["hx_w"].values,'o-',label="within")
    plt.plot(x,data["hx_b"].values,'o-',label="between")
    
    plt.title(r"$\alpha_A = %0.1f, \alpha_B = %0.1f$" % (alpha_A,alpha_B))
    plt.xlabel(r"Modularity, $Q$")
    if i == 0:
        plt.legend()
        plt.ylabel("Average cross-entropy")

plt.tight_layout()
plt.show()
