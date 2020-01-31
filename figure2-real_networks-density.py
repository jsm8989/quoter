import os
import numpy as np
import pandas as pd
import scipy, scipy.stats
import matplotlib.pyplot as plt
import bltools as blt # see baglab github
from adjustText import adjust_text

small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]

dir1 = "Lewis_sims"
dir2 = "real_networks/processing/analyses-2019-10-29"

a=1
fig, ax = plt.subplots(1,3,figsize=(8*a,3*a))

# Simple Contagion
plt.sca(ax[0])
real_simple = pd.read_csv(f"{dir1}/real_simple_peak_size_m.csv")
real_simple = real_simple[real_simple["network"].isin(small_networks)] 
plt.plot(real_simple["density"],real_simple["peak_size_prop"], "o")
plt.ylabel("Average peak size (proportion)")
plt.title("Simple Contagion")

# Annotate
T = []
for i in range(len(real_simple)):
    x = real_simple["density"].values[i]
    y = real_simple["peak_size_prop"].values[i]

    lbl = real_simple["network"].values[i]
    if lbl == 'Les Miserables':
        lbl = 'Les Mis'
    else:
        lbl = lbl.split(" ")[0]
    T.append((x,y,lbl))

texts = [plt.text(x, y, lbl, fontsize=8.5) for x,y,lbl in T]
adjust_text(texts)


# Complex Contagion
plt.sca(ax[1])
real_complex = pd.read_csv(f"{dir1}/real_complex_peak_size_m.csv")
real_complex = real_complex[real_complex["network"].isin(small_networks)]
plt.plot(real_complex["density"],real_complex["peak_size_prop"], "o")
plt.xlabel(r"Density,  $M/\binom{N}{2}$")
plt.ylabel("Average peak size (proportion)")
plt.title("Complex Contagion")

# Annotate
T = []
for i in range(len(real_complex)):
    x = real_complex["density"].values[i]
    y = real_complex["peak_size_prop"].values[i]

    lbl = real_complex["network"].values[i]
    if lbl == 'Les Miserables':
        lbl = 'Les Mis'
    else:
        lbl = lbl.split(" ")[0]
    T.append((x,y,lbl))

texts = [plt.text(x, y, lbl, fontsize=8.5) for x,y,lbl in T]
adjust_text(texts)


# QUOTER MODEL
plt.sca(ax[2])
df = pd.read_csv(f"{dir2}/real_networks-links_only.csv")

plt.plot(df["density"].values,df["average_hx"].values,'o')

# Annotate networks
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

plt.ylabel(r"$\langle h_\times \rangle$")
plt.title("Quoter Model")

# association between hx and density:
d = df["density"].values
hx = df["average_hx"].values

print("Association between density and hx:")
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(d, hx)
print(r_value, p_value)

plt.tight_layout()
plt.savefig("figure2-real_networks-density.pdf")
plt.show()
