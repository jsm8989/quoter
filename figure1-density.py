import os
import numpy as np
import pandas as pd
import scipy, scipy.stats
import matplotlib.pyplot as plt
import bltools as blt # see baglab github

dir1 = "ER_BA_N1000/processing"
dir2 = "real_networks/processing/analyses-2019-10-29"
ER = pd.read_csv(f"{dir1}/hx_ER.csv")
BA = pd.read_csv(f"{dir1}/hx_BA.csv")
N = 1000
BAdeg = np.array([2*m - 2*m**2/N for m in BA["m"].values]) # theoretical degree for BA
##BAparam = list(range(1,21+1)) + list(range(22,25+1)) # for BA -- hack'ey way of better spacing the x-axis
##BAdeg = [2*m - 2*m**2/N for m in BAparam]

fig, ax = plt.subplots(1,3,figsize=(8,3),sharey=False)

# average cross-entropy vs average degree
plt.sca(ax[0])
Ier_ = ER["k"].values <= 40
#plt.plot(ER["k"].values[I_], ER["hx_avg"].values - ER["h_avg"].values,'ko', label="ER") 
plt.plot(ER["k"].values[Ier_], ER["hx_avg"].values[Ier_],'ko', label="ER") 
Iba_ = BAdeg <= 40
#plt.plot(BAdeg[I_], BA["hx_avg"].values - BA["h_avg"].values, 'ro', label="BA")
plt.plot(BAdeg[Iba_], BA["hx_avg"].values[Iba_], 'ro', label="BA")
plt.xlabel(r"Average degree, $\langle k \rangle$")
#plt.ylabel(r"KL-divergence, $\langle h_\times - h \rangle$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.legend()

# variance of cross-entropy vs average degree
plt.sca(ax[1])
plt.plot(ER["k"].values[Ier_], np.power(ER["hx_std"].values[Ier_], 2), 'ko', label="ER")
plt.plot(BAdeg[Iba_], np.power(BA["hx_std"].values[Iba_], 2), 'ro', label="BA")
plt.xlabel(r"Average degree, $\langle k \rangle$")
plt.ylabel(r"Variance $h_\times$")

# Real networks: cross-entropy versus density & other network statistics
df = pd.read_csv(f"{dir2}/real_networks-links_only.csv")

plt.sca(ax[2])
plt.plot(df["density"].values,df["average_hx"].values,'o')

# Optional: annotating which network is which
small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]
try:
    from adjustText import adjust_text
    T = []
    for i,network in enumerate(small_networks):
        x = df["density"].values[i]
        y = df["average_hx"].values[i]
    
        lbl = network
        if lbl == 'Les Miserables':
            lbl = 'Les Mis'
        else:
            lbl = lbl.split(" ")[0]
        T.append((x,y,lbl))
    
    texts = [plt.text(x, y, lbl, fontsize=8.5) for x,y,lbl in T]
    adjust_text(texts)
except ImportError:
    for i,network in enumerate(small_networks):
        x = df["density"].values[i]
        y = df["average_hx"].values[i]
        
        if network == "Freeman's EIES":
            plt.text(x, y-0.01*1.5, network.replace(" ", "\n"), fontsize=8.5, ha='center')
        else:
            plt.text(x+.02, y, network, fontsize=8.5)

plt.xlabel(r"Density,  $M/\binom{N}{2}$")
plt.ylabel(r"$\langle h_\times \rangle$")


# association between hx and density:
d = df["density"].values
hx = df["average_hx"].values

print("Association between density and hx:")
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(d, hx)
print(r_value, p_value)


blt.letter_subplots(axes=ax, xoffset=[-0.325,-0.375,-0.3])
plt.tight_layout(w_pad=0.5)
##plt.savefig("figure1.pdf")
plt.show()




