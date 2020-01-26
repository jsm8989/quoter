import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

dir1 = "dichotomous_graph/processing"
data = pd.read_csv(f"{dir1}/hx_dichotomous.csv")
fig, ax = plt.subplots(1,2,figsize=(8,4),sharey=False)

plt.sca(ax[0])
plt.plot(data["degree_ratio"].values, data["hx_avg"].values)
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")

plt.sca(ax[1])
plt.plot(data["degree_ratio"].values, data["hx_std"].values)
plt.xlabel(r"$k_1/k_2$")
plt.ylabel(r"Variance of $h_\times$")

plt.tight_layout()
plt.savefig("figure2.pdf")
##plt.show()

