import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_ER = pd.read_csv("../processing/hx_ER.csv")
data_BA = pd.read_csv("../processing/hx_BA.csv")

fig = plt.figure(figsize=(10,3))

plt.subplot(1,3,1)
plt.plot(data_ER["average_degree"],data_ER["hx_avg"],'ko',label="ER")
plt.plot(data_BA["average_degree"],data_BA["hx_avg"],'ro',label="BA")
plt.legend()
plt.xlabel("Average degree")
plt.ylabel("Mean cross-entropy")

plt.subplot(1,3,2)
plt.plot(data_ER["density"],data_ER["hx_avg"],'ko')
plt.plot(data_BA["density"],data_BA["hx_avg"],'ro')
plt.xlabel("Density")

plt.subplot(1,3,3)
plt.plot(data_ER["ASPL"],data_ER["hx_avg"],'ko')
plt.plot(data_BA["ASPL"],data_BA["hx_avg"],'ro')
plt.xlabel("Average shortest path length")

plt.tight_layout()
plt.show()

