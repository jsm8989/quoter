import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, PercentFormatter

N = 100
q = 0.5
T = 1000
trial = 0
k = 12

data = "../data_ER/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,k,q,T,trial)
df = pd.read_csv(data, sep = " ")

times_to_save = np.arange(1,1000,10)*N
words_to_save = range(1,10+1)[:5]
# since ER networks are random, we can just choose the first "N" as a random sample
nodes_to_save = [1,2]

node = 1
fig, ax = plt.subplots(len(words_to_save),1,figsize=(8,6),sharex=True)
for i,w in enumerate(words_to_save):
    plt.sca(ax[i])
    data_w = df.loc[(df["word"]==w) & (df["node"]==2)]
    data_w_t = data_w["time"].values
    data_w_t = 100*data_w_t/max(data_w_t)
    plt.plot(data_w_t, data_w["freq"].values, "k-", label="observed")
    plt.plot(data_w_t, data_w["zipf"].values, "r--", label="zipf")

    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    plt.xlim(np.array([-.01,1.01])*100) 
    plt.xticks([0,50,100])

    if i == 0:
        plt.legend()

fig.text(0.04, 0.5, 'Frequency', va='center', rotation='vertical')
plt.xlabel("Simulation Time")
plt.gca().xaxis.set_major_formatter(PercentFormatter())
plt.savefig("stationary-dist.pdf")
plt.show()
