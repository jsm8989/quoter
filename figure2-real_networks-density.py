import os
import numpy as np
import pandas as pd
import scipy, scipy.stats
import matplotlib.pyplot as plt
import bltools as blt # see baglab github
from adjustText import adjust_text
from scipy import stats, linalg
from scipy.optimize import fsolve
import math
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


def get_association(x,y):
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x,y)
    print(r_value, p_value)
    return r_value, p_value
    

def get_predictability(S,N): # explodes for small values of N or large values of S
    try:
        PiMax = fsolve(lambda Pi : S + Pi*math.log(Pi,2) + (1 - Pi)*math.log(1 - Pi,2) - (1 - Pi)*math.log(N-1,2), 0.5)
    except:
        PiMax = 1
    return float(PiMax)

small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]

dir1 = "Lewis_sims"
dir2 = "real_networks/processing/analyses-2019-10-29"

a=1
fig, ax = plt.subplots(1,3,figsize=(8*a,3*a),constrained_layout=True)

# Simple Contagion
plt.sca(ax[0])
real_simple = pd.read_csv(f"{dir1}/real_simple_peak_size_m.csv")
real_simple = real_simple[real_simple["network"].isin(small_networks)] 
plt.plot(real_simple["density"],real_simple["peak_size_prop"], "o")
plt.xlabel(r"Density")
plt.ylabel("Average peak size (proportion)")
plt.title("Simple Contagion")

print("Association between density and peak size (simple contagion):")
get_association(real_simple["density"],real_simple["peak_size_prop"])

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
plt.xlabel(r"Density")
plt.ylabel("Average peak size (proportion)")
plt.title("Complex Contagion")

print("Association between density and peak size (complex contagion):")
get_association(real_complex["density"],real_complex["peak_size_prop"])

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
pred = [get_predictability(s,1000) for s in df["average_hx"].values]

##plt.plot(df["density"].values,df["average_hx"].values,'o')
plt.plot(df["density"].values, pred, 'o')

# Annotate networks
T = []
for i,network in enumerate(small_networks):
    x = df["density"].values[i]
##    y = df["average_hx"].values[i]
    y = pred[i]

    lbl = network
    if lbl == 'Les Miserables':
        lbl = 'Les Mis'
    else:
        lbl = lbl.split(" ")[0]
    T.append((x,y,lbl))

texts = [plt.text(x, y, lbl, fontsize=8.5) for x,y,lbl in T]
adjust_text(texts)

plt.xlabel(r"Density")
plt.ylabel(r"Average predictability, $\Pi$")
plt.title("Quoter Model")

### inset. average hx vs average degree
##axcurr = plt.gca()
##dd = 0.02
##dx,dy = -0.15+dd, 0.26+dd
##a = 1.3
##wi,hi = a*0.4-dd,a*0.4*0.8-dd
##axins = inset_axes(axcurr, width="60%", height="60%",
##                   bbox_to_anchor=(.65+dx, .3+dy, wi,hi),
##                   bbox_transform=axcurr.transAxes, loc="upper right")
##plt.plot(df["density"], df["average_hx"], "C1o", ms=2)
##plt.xlabel(r"density")
##plt.ylabel(r"$\langle h_\times \rangle$")


# association between hx and density:
d = df["density"].values
hx = df["average_hx"].values

print("Association between density and hx (predictability):")
print("Association between density and peak size (complex contagion):")
get_association(d, pred)


blt.letter_subplots(axes=ax.flatten(), xoffset=-.1, yoffset=1.05)
##plt.tight_layout()
plt.savefig("figure2-real_networks-density.pdf")
plt.show()
