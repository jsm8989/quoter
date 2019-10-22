import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("../processing/fix_density_vary_transitivity.csv")

plt.plot(data["transitivity"],data["hx"],'o')
plt.xlabel("Transitivity")
plt.ylabel("Mean cross-entropy")
plt.show()
