import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data_ER = pd.read_csv("ER_BA/processing/hx_ER.csv")
data_BA = pd.read_csv("ER_BA/processing/hx_BA.csv")
data_ER_ab = pd.read_csv("ER_BA/processing/hx_abv-blw-k_ER.csv")
data_BA_ab = pd.read_csv("ER_BA/processing/hx_abv-blw-k_BA.csv")
data_real = pd.read_csv("real_networks/processing/hx_real-networks.csv")
gdata = pd.read_csv("real_networks/processing/network_statistics.csv")


fig = plt.figure(figsize=(10*1.2,4*1.2))

# ER-BA average degree, density, & ASPL vs hx
plt.subplot(2,4,1)
plt.plot(data_ER["average_degree"],data_ER["hx_avg"],'ko',label="ER")
plt.plot(data_BA["average_degree"],data_BA["hx_avg"],'ro',label="BA")
plt.legend(loc="lower right")
plt.xlabel("Average degree")
plt.ylabel("Mean cross-entropy")

plt.subplot(2,4,2)
plt.plot(data_ER["density"],data_ER["hx_avg"],'ko')
plt.plot(data_BA["density"],data_BA["hx_avg"],'ro')
plt.xlabel("Density")

plt.subplot(2,4,3)
plt.plot(data_ER["ASPL"],data_ER["hx_avg"],'ko')
plt.plot(data_BA["ASPL"],data_BA["hx_avg"],'ro')
plt.xlabel("Average shortest path length")


# Real world network plot
##dens = gdata["density"].values[[1,2,4,8,9,10,11,12,13,14,15,17]]
##C = gdata["transitivity"].values[[1,2,4,8,9,10,11,12,13,14,15,17]]
##folders = ['Arxiv_ca-GrQc','adolescent_health','email_network','terrorists',
##           'dolphins','lesmis','kapfdata','movies','Sampson','GoldenAge',
##           'NFL2009_network','Freemans_EIES']
##plt.subplot(2,4,4)
##for i,folder in enumerate(folders):
##    x = C[i]
##    y = data_real["hx_avg"].values[i]
##    yerr = data_real["hx_sd"].values[i]
##    plt.errorbar(x, y, yerr=yerr, fmt='bo', elinewidth=3)
####    plt.plot(x,y,'bo')
####    if folder == 'Freemans_EIES':
####        plt.text(x-0.1, y-0.01, folder, fontsize=8.5)
####    elif folder == 'Arxiv_ce-GrQc':
####        plt.text(x+0.02, y, "Arxiv", fontsize=8.5)
####    elif folder == 'lesmis':
####        plt.text(x+0.02, y-.005, folder, fontsize=8.5)
####    else:
####        plt.text(x+.02, y, folder, fontsize=8.5)
##plt.xlabel("Density")
##plt.ylabel("Mean cross-entropy")
##plt.title("Real networks")


# ER-BA above/below average degree plot
ER_params = np.arange(5,51,5) # for ER. Use for both plots' x-ticks 
BA_m = [3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA only
BA_params = [2*m-2*m**2/100 for m in BA_m]

plt.subplot(2,4,5)
plt.plot(ER_params,data_ER_ab["above_average_k"].values,'-ko',label=r"$k_i > \langle k \rangle$")
plt.plot(ER_params,data_ER_ab["below_average_k"].values,'-ro',label=r"$k_i < \langle k \rangle$")
plt.legend()
plt.xlabel(r"$\langle k \rangle$")
plt.xticks(ER_params)
plt.ylabel("Mean cross-entropy")
plt.title("Erdős–Rényi")

plt.subplot(2,4,6)
plt.plot(BA_params,data_BA_ab["above_average_k"].values,'-ko',label=r"$k_i > \langle k \rangle$")
plt.plot(BA_params,data_BA_ab["below_average_k"].values,'-ro',label=r"$k_i < \langle k \rangle$")
plt.legend()
plt.xlabel(r"$\langle k \rangle$")
plt.xticks(ER_params)
plt.title("Barabási–Albert")

plt.tight_layout()
##plt.show()   
plt.savefig("f1.pdf")

