import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_ER = pd.read_csv("../processing/hx_ER.csv")
data_BA = pd.read_csv("../processing/hx_BA.csv")

plt.plot(data_ER["transitivity"],data_ER["hx"],'ko',label="ER")
plt.plot(data_BA["transitivity"],data_BA["hx"],'ro',label="BA")
plt.legend()
plt.xlabel("Transitivity")
plt.ylabel("Mean cross-entropy")
plt.show()

