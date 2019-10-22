import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_ER = pd.read_csv("../processing/hx_ER-Distance.csv")
data_BA = pd.read_csv("../processing/hx_BA-Distance.csv")

fig = plt.figure(figsize=(10,4))

plt.subplot(2,3,1)
plt.plot(data_ER["average_degree"],data_ER["hx1"],'o-',label=r"$d=1$")
plt.plot(data_ER["average_degree"],data_ER["hx2"],'o-',label=r"$d=2$")
plt.plot(data_ER["average_degree"],data_ER["hx3"],'o-',label=r"$d=3$")
plt.legend()
plt.xlabel("Average degree")
plt.ylabel("Mean cross-entropy")
plt.title("Erdős–Rényi")

plt.subplot(2,3,2)
plt.plot(data_ER["density"],data_ER["hx1"],'o-',label=r"$d=1$")
plt.plot(data_ER["density"],data_ER["hx2"],'o-',label=r"$d=2$")
plt.plot(data_ER["density"],data_ER["hx3"],'o-',label=r"$d=3$")
plt.xlabel("Density")

plt.subplot(2,3,3)
plt.plot(data_ER["ASPL"],data_ER["hx1"],'o-',label=r"$d=1$")
plt.plot(data_ER["ASPL"],data_ER["hx2"],'o-',label=r"$d=2$")
plt.plot(data_ER["ASPL"],data_ER["hx3"],'o-',label=r"$d=3$")
plt.xlabel("Average shortest path length")


plt.subplot(2,3,4)
plt.plot(data_BA["average_degree"],data_BA["hx1"],'o-',label=r"$d=1$")
plt.plot(data_BA["average_degree"],data_BA["hx2"],'o-',label=r"$d=2$")
plt.plot(data_BA["average_degree"],data_BA["hx3"],'o-',label=r"$d=3$")
plt.legend()
plt.xlabel("Average degree")
plt.ylabel("Mean cross-entropy")
plt.title("Barabási–Albert")

plt.subplot(2,3,5)
plt.plot(data_BA["density"],data_BA["hx1"],'o-',label=r"$d=1$")
plt.plot(data_BA["density"],data_BA["hx2"],'o-',label=r"$d=2$")
plt.plot(data_BA["density"],data_BA["hx3"],'o-',label=r"$d=3$")
plt.xlabel("Density")

plt.subplot(2,3,6)
plt.plot(data_BA["ASPL"],data_BA["hx1"],'o-',label=r"$d=1$")
plt.plot(data_BA["ASPL"],data_BA["hx2"],'o-',label=r"$d=2$")
plt.plot(data_BA["ASPL"],data_BA["hx3"],'o-',label=r"$d=3$")
plt.xlabel("Average shortest path length")


plt.tight_layout()
plt.savefig("hx_versus_density-Distance.pdf")
plt.show()

