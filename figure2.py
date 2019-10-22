import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_ER = pd.read_csv("ER_BA/processing/hx_ER.csv")
data_BA = pd.read_csv("ER_BA/processing/hx_BA.csv")
data_ER_ab = pd.read_csv("ER_BA/processing/hx_abv-blw-C_ER.csv")
data_BA_ab = pd.read_csv("ER_BA/processing/hx_abv-blw-C_BA.csv")
data_link_1 = pd.read_csv("link_tracking/processing/fix_degree_vary_nAB.csv")
data_link_2 = pd.read_csv("link_tracking/processing/fix_density_vary_transitivity.csv")
data_real = pd.read_csv("real_networks/processing/hx_real-networks.csv")
gdata = pd.read_csv("real_networks/processing/network_statistics.csv")


fig = plt.figure(figsize=(8,6))

# ER-BA transitivity vs hx
plt.subplot(3,2,1)
plt.plot(data_ER["transitivity"],data_ER["hx"],'ko',label="ER")
plt.plot(data_BA["transitivity"],data_BA["hx"],'ro',label="BA")
plt.legend()
plt.xlabel("Transitivity")
plt.ylabel("Mean cross-entropy")

# Real world network plot
dens = gdata["density"].values[[1,2,4,8,9,10,11,12,13,14,15,17]]
C = gdata["transitivity"].values[[1,2,4,8,9,10,11,12,13,14,15,17]]
folders = ['Arxiv_ca-GrQc','adolescent_health','email_network','terrorists',
           'dolphins','lesmis','kapfdata','movies','Sampson','GoldenAge',
           'NFL2009_network','Freemans_EIES']
plt.subplot(3,2,2)
for i,folder in enumerate(folders):
    x = C[i]
    y = data_real["hx_avg"].values[i]
    yerr = data_real["hx_sd"].values[i]
##    plt.errorbar(x, y, yerr=yerr, fmt='bo', elinewidth=3)
    plt.plot(x,y,'bo')
plt.xlabel("Transitivity")
plt.ylabel("Mean cross-entropy")
plt.title("Real networks")

# ER-BA above/below average clustering
ER_params = np.arange(5,51,5) # for ER. Use for both plots' x-ticks 
BA_m = [3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA only
BA_params = [2*m-2*m**2/100 for m in BA_m]

plt.subplot(3,2,3)
plt.plot(ER_params,data_ER_ab["above_average_C"].values,'-ko',label=r"$C_i > \langle C \rangle$")
plt.plot(ER_params,data_ER_ab["below_average_C"].values,'-ro',label=r"$C_i < \langle C \rangle$")
plt.legend()
plt.xlabel(r"$\langle k \rangle$")
plt.xticks(ER_params)
plt.ylabel("Mean cross-entropy")
plt.title("Erdős–Rényi")

plt.subplot(3,2,4)
plt.plot(BA_params,data_BA_ab["above_average_C"].values,'-ko',label=r"$C_i > \langle C \rangle$")
plt.plot(BA_params,data_BA_ab["below_average_C"].values,'-ro',label=r"$C_i < \langle C \rangle$")
plt.legend()
plt.xlabel(r"$\langle k \rangle$")
plt.xticks(ER_params)
plt.title("Barabási–Albert")

# Link graph 1
plt.subplot(3,2,5)
plt.plot(data_link_1["nAB"],data_link_1["hx"],'o')
plt.xlabel(r"$n_{AB}$")
plt.ylabel("Mean cross-entropy")
plt.title(r"Link graph: fix degee, vary $n_{AB}$")

# Link graph 2
plt.subplot(3,2,6)
plt.plot(data_link_2["transitivity"],data_link_2["hx"],'o')
plt.xlabel("Transitivity")
plt.ylabel("Mean cross-entropy")
plt.title("Link graph: fix density, vary transitivity")


plt.tight_layout()
plt.show()
