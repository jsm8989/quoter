import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data_SBM = pd.read_csv("../processing/sbm_N60.csv")

# Plot hx_w and hx_b vs mu on same plot
plt.plot(data_SBM["mu"],data_SBM["hx_w"],'o-',label="within")
plt.plot(data_SBM["mu"],data_SBM["hx_b"],'o-',label="between")
plt.xlabel(r"$\mu$")
plt.ylabel("Mean cross-entropy")
plt.legend()
plt.show()


# Plot ratio of hx_w/hx_b vs mu
plt.plot(data_SBM["mu"],np.divide(data_SBM["hx_w"],data_SBM["hx_b"]),'o-')
plt.xlabel(r"$\mu$")
plt.ylabel(r"$\langle h(within) \rangle / \langle h(between) \rangle$")  
plt.show()
