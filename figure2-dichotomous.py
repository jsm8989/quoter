import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bltools as blt

dir1 = "dichotomous_graph/processing"
data = pd.read_csv(f"{dir1}/hx_dichotomous.csv")
fig, ax = plt.subplots(1,2,figsize=(7,3),sharey=False)

plt.sca(ax[0])
plt.plot(data["degree_ratio"].values, data["hx_avg"].values)
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"$\langle h_\times \rangle$")

plt.sca(ax[1])
plt.plot(data["degree_ratio"].values, data["hx_std"].values)
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Variance $h_\times$")

blt.letter_subplots(axes=ax, xoffset=-0.3)
plt.tight_layout()
plt.savefig("figure2.pdf")
##plt.show()

