import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("../processing/fix_degree_vary_nAB.csv")

plt.plot(data["nAB"],data["hx"],'o')
plt.xlabel(r"$n_{AB}$")
plt.ylabel("Mean cross-entropy")
plt.show()
