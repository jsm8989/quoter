import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ER = pd.read_csv("hx_ER.csv")
BA = pd.read_csv("hx_BA.csv")
N = 1000
BAdeg = [2*m - 2*m**2/N for m in BA["m"].values] # theoretical degree for BA
##BAparam = list(range(1,21+1)) + list(range(22,25+1)) # for BA -- hack'ey way of better spacing the x-axis
##BAdeg = [2*m - 2*m**2/N for m in BAparam]

fig, ax = plt.subplots(1,2,figsize=(10,4),sharey=False)

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

plt.tight_layout()
plt.savefig("ER-BA_hx_vs_avgdeg.pdf")
plt.show()
