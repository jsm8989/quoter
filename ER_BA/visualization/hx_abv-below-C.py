import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ER_params = np.arange(5,51,5) # for ER. Use for both plots' x-ticks 
BA_m = [3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA only
BA_params = [2*m-2*m**2/100 for m in BA_m]

data_ER = pd.read_csv("../processing/hx_abv-blw-C_ER.csv")
data_BA = pd.read_csv("../processing/hx_abv-blw-C_BA.csv")

fig = plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(ER_params,data_ER["above_average_C"].values,'-ko',label=r"$C_i > \langle C \rangle$")
plt.plot(ER_params,data_ER["below_average_C"].values,'-ro',label=r"$C_i < \langle C \rangle$")
plt.legend()
plt.xlabel(r"$\langle k \rangle$")
plt.xticks(ER_params)
plt.ylabel("Mean cross-entropy")

plt.subplot(1,2,2)
plt.plot(BA_params,data_BA["above_average_C"].values,'-ko',label=r"$C_i > \langle C \rangle$")
plt.plot(BA_params,data_BA["below_average_C"].values,'-ro',label=r"$C_i < \langle C \rangle$")
plt.legend()
plt.xlabel(r"$\langle k \rangle$")
plt.xticks(ER_params)

plt.tight_layout()
plt.show()   
