import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

N = 200
k = 6
T = 1000
q_list = [0, .2, .4, .6, .8, .9, .99, .999, .9999]
lam_list = [1, 2, 4, 6, 8]
p_list = [0,1]
trials_list = list(range(150))

# DENSITY VERSUS AVERAGE CROSS ENTROPY
for p in p_list:
    data = np.zeros((len(q_list),len(lam_list)))
    for i,q in enumerate(q_list):
        for j,lam in enumerate(lam_list):
            print("starting: q%0.4f lambda%i" % (q,lam))
            hx_list = []
            for trial in trials_list:
                efile = "../data_SW/edge/N%i_p%0.1f_q%0.4f_lam%i_T%i_sim%i.txt" % (N,p,q,lam,T,trial)

                if os.path.isfile(efile):  
                        edata = pd.read_csv(efile, sep = " ")
                        hx_list.extend(edata["hx"].values)
                        
            data[i,j] = np.mean(hx_list)

    df = pd.DataFrame(data=data)
    df.to_csv("hx_SW_p%0.1f.csv" % p, header=False, index=False)


data1 = np.loadtxt("hx_SW_p%0.1f.csv" % 0, delimiter=",")
data2 = np.loadtxt("hx_SW_p%0.1f.csv" % 1, delimiter=",")
##q_list = [0, .2, .4, .6, .8, .9, .99, .999, .9999]
##lam_list = [1, 2, 4, 6, 8]
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
plt.title(r"$\langle h_\times \rangle_{p = 0} - \langle h_\times\rangle_{p = 1}$")
plt.show()


        
        
