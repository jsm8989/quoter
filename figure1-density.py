import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

os.chdir("ER_BA_N1000/processing/")
ER = pd.read_csv("hx_ER.csv")
BA = pd.read_csv("hx_BA.csv")
N = 1000
BAdeg = [2*m - 2*m**2/N for m in BA["m"].values] # theoretical degree for BA
##BAparam = list(range(1,21+1)) + list(range(22,25+1)) # for BA -- hack'ey way of better spacing the x-axis
##BAdeg = [2*m - 2*m**2/N for m in BAparam]

fig, ax = plt.subplots(1,3,figsize=(8,3),sharey=False)

# average cross-entropy vs average degree
plt.sca(ax[0])
plt.plot(ER["k"].values, ER["hx_avg"].values - ER["h_avg"].values,'ko', label="ER") 
plt.plot(BAdeg, BA["hx_avg"].values - BA["h_avg"].values, 'ro', label="BA")
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel(r"KL-divergence, $\langle h_\times - h \rangle$")
plt.legend()

# variance of cross-entropy vs average degree
plt.sca(ax[1])
plt.plot(ER["k"].values, np.power(ER["hx_std"].values, 2), 'ko', label="ER")
plt.plot(BAdeg, np.power(BA["hx_std"].values, 2), 'ro', label="BA")
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel(r"Variance of $h_\times$")

# Real networks: cross-entropy versus density & other network statistics
os.chdir("../../real_networks/processing/analyses-2019-10-29")
df = pd.read_csv("real_networks-links_only.csv")

plt.sca(ax[2])
plt.plot(df["density"].values,df["average_hx"].values,'o')

# Optional: annotating which network is which
small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]

for i,network in enumerate(small_networks):
    x = df["density"].values[i]
    y = df["average_hx"].values[i]

    if network == "Freeman's EIES":
        plt.text(x-0.22, y-0.01, network, fontsize=8.5)
    else:
        plt.text(x+.02, y, network, fontsize=8.5)

plt.xlabel(r"Density,  $M/\binom{N}{2}$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")



plt.tight_layout()
plt.savefig("../../../figure1.pdf")
plt.show()




