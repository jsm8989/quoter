import os
import numpy as np
import pandas as pd
import scipy, scipy.stats
import matplotlib.pyplot as plt
import bltools as blt # see baglab github

dir2 = "real_networks/processing/analyses-2019-10-29"

df = pd.read_csv(f"{dir2}/real_networks-links_only.csv")

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

plt.savefig("figure2tentative-real_networks-density.pdf")
##plt.show()
