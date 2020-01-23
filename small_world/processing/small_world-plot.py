import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# hx vs transitivity 
data = pd.read_csv("small_world.csv")
plt.plot(data["C"],data["hx_avg"],'o-')
plt.xlabel("Transitivity")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")
plt.show()

# Zipf & Uniform vocabulary distributions
data_Z = pd.read_csv("small_world.csv")
data_U = pd.read_csv("small_world_uniform.csv")
fig, ax = plt.subplots(1,3,figsize=(10,4),sharey=False)

plt.sca(ax[0])
plt.plot(data_Z["C"],data_Z["hx_avg"],'C0o-',label="Zipf")
plt.plot(data_U["C"],data_U["hx_avg"],'C1o-',label="Uniform")
plt.legend()
plt.title("On same plot")
plt.xlabel("Transitivity")
plt.ylabel(r"Average cross-entropy, $\langle h_\times \rangle$")

plt.sca(ax[1])
plt.plot(data_Z["C"],data_Z["hx_avg"],'C0o-')
plt.title("Zipf")

plt.sca(ax[2])
plt.plot(data_U["C"],data_U["hx_avg"],'C1o-')
plt.title("Uniform")

plt.tight_layout()
plt.show()
