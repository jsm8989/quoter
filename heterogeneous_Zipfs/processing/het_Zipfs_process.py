import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

N = 200
q = 0.5
T = 1000
k = 8
alpha = 2
trials_list = list(range(300))
delta_list = np.arange(0,1.05,.05)

for graph in ["ER","BA"]:
	if graph == "ER":
   		param_sym = "k"
   		col = "k"

	else:
		param_sym = "m"
		m = k//2
		col = "r"

	hx = []
	for delta_alpha in delta_list:
   		hx_this_delta = []
   		print(delta_alpha)

   		for trial in trials_list:
   			file = "../data_%s/N%i_k%i_q%0.1f_T%i_a%0.1f_delta%0.2f_sim%i.txt" % (graph,N,k,q,T,alpha,delta_alpha,trial)
   			data = pd.read_csv(file, sep = " ")
   			hx_this_delta.extend(data["hx"].values)
   		hx.append(np.mean(hx_this_delta))

	plt.plot(delta_list, hx, col+"o", label = "%s" % graph)

plt.xlabel(r"$\delta$")
plt.ylabel(r"$\langle h_\times \rangle$")
plt.legend()
plt.show()