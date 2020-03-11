import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import math
import itertools
from scipy import stats


q_list = [0.5]
T = 2000
lam = 3
z = 8
# trials_list = list(range(300))
trials_list = list(range(300))


for qi,q in enumerate(q_list):
	RR, RQ, QR, QQ = [], [], [], []
	RRt, RQt, QRt, QQt = [], [], [], []
	for trial in trials_list:
		file = "../data_2ndorder/z%i_q%0.3f_T%i_lam%i_sim%i.txt" % (z,q,T,lam,trial)
		data = pd.read_csv(file, sep = " ")
		dRR = data.loc[data["label"]=="RR"]
		dRQ = data.loc[data["label"]=="RQ"]
		dQR = data.loc[data["label"]=="QR"]
		dQQ = data.loc[data["label"]=="QQ"]

		RR.extend(dRR["lambda"].values)
		RQ.extend(dRQ["lambda"].values)
		QR.extend(dQR["lambda"].values)
		QQ.extend(dQQ["lambda"].values)

		RRt.extend(dRR["time"].values)
		RQt.extend(dRQ["time"].values)
		QRt.extend(dQR["time"].values)
		QQt.extend(dQQ["time"].values)

	labels = ["RR","RQ","QR","QQ"]
	colors = ['k','r','b','m']
	for i,(alist,blist) in enumerate(zip([RR,RQ,QR,QQ],[RRt,RQt,QRt,QQt])):
		bin_means, bin_edges, binnumber = stats.binned_statistic(blist, alist, 'mean', bins=50)
		bin_centers = [(bin_edges[i]+bin_edges[i+1])/2 for i in range(len(bin_edges)-1)]
		plt.plot(bin_centers, bin_means, color=colors[i], label=labels[i])
		# plt.plot(blist,alist,'o',ms=3,label=labels[i])

plt.xlabel(r"Position in ego's text, $t$")
plt.ylabel(r"$\Lambda_{xy,t}$")
plt.legend(title=r"$xy$")
plt.savefig("2ndorder.pdf")
plt.show()



