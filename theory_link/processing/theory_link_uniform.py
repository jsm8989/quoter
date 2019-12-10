import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import math
import itertools



q_list = np.linspace(0,1,20)
T = 1000
lam_list = [3,6,9]
z_list = [2,4,8]
trials_list = list(range(100))

##for z in z_list:
##    for lam in lam_list:
##        print(z,lam)
##        hx_all_q = np.zeros(len(q_list))
##        for i,q in enumerate(q_list):
##            hx_this_q = []
##            for trial in trials_list:
##                z_alter=z_ego=z
##                efile = "../data_uniform/z%i_q%0.3f_T%i_lam%i_sim%i.txt" % (z,q,T,lam,trial)
##                edata = pd.read_csv(efile, sep = " ")
##                hx_this_q.extend(edata["hx"].values)
##            hx_all_q[i] = np.mean(hx_this_q)
##
##        
##        df = pd.DataFrame({"q":q_list,"hx_avg":hx_all_q})
##        df = df.to_csv("z%i_lam%i.csv" % (z,lam), index=False)

z_style = ['o','s','x']
lam_color = ['C0','C1','C2']

for i,z in enumerate(z_list):
    for j,lam in enumerate(lam_list):
        data = pd.read_csv("z%i_lam%i.csv" % (z,lam))
        plt.plot(data["q"].values,data["hx_avg"].values,z_style[i], c=lam_color[j], fillstyle="none", label=r"$z=%i,\lambda=%i$" % (z,lam))    

        T = 1000*lam
        theory_L = [T/math.log(z,2) *  ( (1-q)*(math.log(T*z,2) - 1) +
                 q/2*(math.log(T*z**(lam+2),2)+(z**lam/T + 1)*math.log(T/z**lam + 1,2) - 2)) for q in q_list]
        theory_hx = [T*math.log(T,2)/L for L in theory_L]
        plt.plot(q_list, theory_hx, c=lam_color[j])
leg = plt.legend(title=r"$T=1000\lambda$", loc="lower left", bbox_to_anchor=(0,0.08), ncol=3, prop={'size': 8})
leg._legend_box.align = "left"
plt.xlabel(r"Quote probability, $q$")
plt.ylabel(r"Cross-entropy, $h_\times$ [bits]")
plt.show()



