import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

mu_list = [0.15,0.20,0.25,0.30]
N = 100
m = N//2

style = ['C0-','C1-','C2-','C3-']

# PLOT 1: hx vs p
for i,mu in enumerate(mu_list):
    data =  pd.read_csv("sbm_mu%0.2f_N%i.csv" % (mu,N))
    plt.plot(data["p"].values, data["hx_w"].values, style[i], label="%0.2f" % mu)
    plt.plot(data["p"].values, data["hx_b"].values, style[i]+'-')
plt.legend(title=r"$\mu$")
plt.xlabel(r"$p$")
plt.ylabel(r"$\langle h_\times \rangle$")
plt.show()

# PLOT 2: Delta hx vs p
for i,mu in enumerate(mu_list):
    data =  pd.read_csv("sbm_mu%0.2f_N%i.csv" % (mu,N))
    plt.plot(data["p"].values, data["hx_b"].values-data["hx_w"].values, style[i], label="%0.2f" % mu)
plt.legend(title=r"$\mu$")
plt.xlabel(r"$p$")
plt.ylabel(r"$\Delta h_\times$")
plt.show()

# PLOT 3: Delta hx vs modularity
for i,mu in enumerate(mu_list):
    data =  pd.read_csv("sbm_mu%0.2f_N%i.csv" % (mu,N))
    p_list = data["p"].values
    mu_list = np.array([mu]*len(p_list))
    modularity = (1/2)*np.divide(p_list-p_list*m+mu_list*m, p_list-p_list*m-mu_list*m)
    plt.plot(modularity, data["hx_b"].values-data["hx_w"].values, style[i], label="%0.2f" % mu)
plt.legend(title=r"$\mu$")
plt.xlabel(r"Modularity, $Q$")
plt.ylabel(r"$\Delta h_\times$")
plt.show()
