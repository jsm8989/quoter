import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import math
import itertools
from scipy import stats


q = 0
# T = 1000
T = 20000
lam = 3
zlist = [2,8]
trials_list = list(range(500))

fig, ax = plt.subplots(1,2,figsize=(8,4))
for iz,z in enumerate(zlist):
	plt.sca(ax[iz])
	R = []
	index = []
	for trial in trials_list:
		if trial % 50 == 0:
			print(trial, "done")

		file = "../data_random/z%i_q%0.3f_T%i_lam%i_sim%i.txt" % (z,q,T,lam,trial)
		data = pd.read_csv(file, sep = " ")
		vals = data["lambda"].values
		R.extend(vals)
		index.extend(list(range(len(vals))))

	bin_means, bin_edges, binnumber = stats.binned_statistic(index, R, 'mean', bins=50)
	bin_centers = [(bin_edges[i]+bin_edges[i+1])/2 for i in range(len(bin_edges)-1)]
	plt.plot(bin_centers, bin_means, label="empirical")

	d = 1/z
	rng = list(range(1,int(np.max(bin_centers)),2))
	em = np.euler_gamma # euler-mascheroni constant
	theory1 = [math.log(t)/math.log(1/d) + 1 for t in rng]
	# theory2 = [math.log(t*(1-d))/math.log(1/d) + em/math.log(1/d) - 1/2 + 1 for t in rng]
	theory2 = [math.log(t)/math.log(1/d) + em/math.log(1/d) - 1/2 + 1 for t in rng]
	plt.plot(rng,theory1,label="theory 1")
	plt.plot(rng,theory2,'k:',label="theory 2")
	plt.xlabel("Position in ego's text, $t$")
	plt.title(r"$z=%i$" % z)

plt.sca(ax[0])
plt.legend()
plt.ylabel(r"$\Lambda_{t}$")
# plt.savefig("LambdaRandom1000.pdf")
plt.show()



