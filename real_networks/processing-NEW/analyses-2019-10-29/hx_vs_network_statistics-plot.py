import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Real networks: cross-entropy versus density & other network statistics
df = pd.read_csv("real_networks-links_only.csv")

### UNUSED: calculate standard error
##m2_minus_m1_sq = df["average_hxsquared"].values - np.power(df["average_hx"].values,2) 
##n_over_n_minus_1 = np.divide(df["count"].values,df["count"].values - 1)
##sample_var = np.multiply(n_over_n_minus_1,m2_minus_m1_sq)
##stderror = np.divide(sample_var, df["count"].values)

plt.plot(df["density"].values,df["average_hx"].values,'o')

# Optional: annotating which network is which
small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]

for i,network in enumerate(small_networks):
    x = df["density"].values[i]
    y = df["average_hx"].values[i]

    if network == "Freeman's EIES":
        plt.text(x-0.15, y-0.01, network, fontsize=8.5)
    else:
        plt.text(x+.02, y, network, fontsize=8.5)

plt.xlabel(r"Density,  $M/\binom{N}{2}$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.show()


### UNUSED: hx vs {density, transitivity} and density vs transitvity
##df = pd.read_csv("real_networks-links_only.csv")
##fig = plt.figure(figsize=(10,3))
##plt.subplot(1,3,1)
##plt.plot(df["density"],df["average_hx"],'ko')
##plt.xlabel(r"Density,  $M/\binom{N}{2}$")
##plt.ylabel("Cross-entropy")
##plt.subplot(1,3,2)
##plt.plot(df["transitivity"],df["average_hx"],'ko')
##plt.xlabel(r"Transitivity")
##plt.subplot(1,3,3)
##plt.plot(df["density"],df["transitivity"],'ko')
##plt.xlabel(r"Density,  $M/\binom{N}{2}$")
##plt.ylabel("Transitivity")
##plt.tight_layout()
##plt.show()
