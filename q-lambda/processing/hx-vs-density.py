import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

N = 100
q_list = [0, .2, .4, .6, .8, .9, .99, .999, .9999]
lam_list = [1, 2, 4, 6, 8]
k_list = [5, 20]
T = 1000
trials_list = list(range(100))

# DENSITY VERSUS AVERAGE CROSS ENTROPY
##for k in k_list:
##    data = np.zeros((len(q_list),len(lam_list)))
##    for i,q in enumerate(q_list):
##        for j,lam in enumerate(lam_list):
##            print("starting: q%0.4f lambda%i" % (q,lam))
##            hx_list = []
##            for trial in trials_list:
##                if q in [.99,.999,.9999]:
##                    efile = "../data_ER/edge/N%i_k%i_q%0.4f_lam%i_T%i_sim%i.txt" % (N,k,q,lam,T,trial)
##                else:
##                    efile = "../data_ER/edge/N%i_k%i_q%0.1f_lam%i_T%i_sim%i.txt" % (N,k,q,lam,T,trial)
##
##                if os.path.isfile(efile):  
##                        edata = pd.read_csv(efile, sep = " ")
##                        hx_list.extend(edata["hx"].values)
##                        
##            data[i,j] = np.mean(hx_list)
##
##    df = pd.DataFrame(data=data)
##    df.to_csv("hx_ER_k%i.csv" % k, header=False, index=False)


data1 = np.loadtxt("hx_ER_k%i.csv" % 5, delimiter=",")
data2 = np.loadtxt("hx_ER_k%i.csv" % 20, delimiter=",")
q_list = [0, .2, .4, .6, .8, .9, .99, .999, .9999]
lam_list = [1, 2, 4, 6, 8]

a=0
b=9
print(np.subtract(data2[a:b,:],data1[a:b,:]))
q_list = q_list[a:b]
plt.imshow(np.subtract(data2[a:b,:],data1[a:b,:]), origin="lower")
plt.colorbar()
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
plt.title(r"$\langle h_\times \rangle_{k = 20} - \langle h_\times\rangle_{k = 5}$")
plt.show()


        
        
