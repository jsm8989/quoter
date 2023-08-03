import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import bltools as blt


dir1 = "ER_BA_selfEntropy/processing"
dir2 = "small_world/processing"

fig, ax = plt.subplots(1,2,figsize=(7,3),sharey=True)

# ER BA
plt.sca(ax[0])
N = 100
ERparam = np.arange(5,51,5) # k used for ER
BAparam = [ 3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # m used for BA
BAparam = [2*m - 2*m**2/N for m in BAparam] # EXACT k for BA
q_list = [0.1,0.5,0.9]

q_style = ["o-","x-","s-"]
for i,q in enumerate(q_list):
    ER = pd.read_csv(f"{dir1}/hx_ER_q%0.1f.csv" % q)
    BA = pd.read_csv(f"{dir1}/hx_BA_q%0.1f.csv" % q)
    plt.plot(ERparam, ER["hx_avg"].values, "k" + q_style[i], label=r"$q=%0.1f$" % q)
    plt.plot(BAparam, BA["hx_avg"].values, "r" + q_style[i])

leg1 = plt.legend() # put in caption that black=ER, red=BA
ax[0].add_artist(leg1)
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")

er_line = mlines.Line2D([], [], color='k', ls='-',lw=3)
ba_line = mlines.Line2D([], [], color='r', ls='-',lw=3)
plt.legend([er_line, ba_line], ['ER', "BA"], loc='lower center', handlelength=1.25, fontsize=9)





# SMALL WORLD
plt.sca(ax[1])
q_list = [0.1, 0.5, 0.9]
q_style = ["o-","x-","s-"]
N = 200
k = 6

for i,q in enumerate(q_list):
    data = pd.read_csv(f"{dir2}/small_world_N%i_k%i_q%0.1f.csv" % (N,k,q))
    plt.plot(data["p"], data["hx_avg"], "C0" + q_style[i], label=r"$q=%0.1f$" % q)
        
plt.xlabel(r"Rewiring probability, $p$")
plt.xscale("log")
plt.legend(bbox_to_anchor=(.0, 0.55), loc=2,)

blt.letter_subplots(axes=ax, xoffset=0, yoffset=1.05)

plt.tight_layout()
plt.savefig("figure7-robustness-q.pdf")

# plt.show()

    
    
