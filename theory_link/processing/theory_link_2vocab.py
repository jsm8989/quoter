import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
import math
import itertools




q_list = np.linspace(0,1,20)
T = 1000
lam = 3
alpha_list = [(1.5,2.0),(2.0,2.0),(2.5,2.0),(2.0,1.5),(2.0,2.5)]
trials_list = list(range(100))

##for (alpha_alter,alpha_ego) in alpha_list:
##    print(alpha_alter,alpha_ego)
##    hx_all_q = np.zeros(len(q_list))
##    for i,q in enumerate(q_list):
##        hx_this_q = []
##        for trial in trials_list:
##            efile = "../data_2vocab/Aa%0.1f_Ae%0.1f_q%0.3f_T%i_lam%i_sim%i.txt" % (alpha_alter,alpha_ego,q,T,lam,trial)
##            edata = pd.read_csv(efile, sep = " ")
##            hx_this_q.extend(edata["hx"].values)
##        hx_all_q[i] = np.mean(hx_this_q)
##
##    df = pd.DataFrame({"q":q_list,"hx_avg":hx_all_q})
##    df = df.to_csv("Aa%0.1f_Ae%0.1f.csv" % (alpha_ego,alpha_alter), index=False)



alpha_alter_style = ['o','s']*3
alpha_ego_color= ['C0','C1']*3
alpha_list = [(1.5,2.0),(2.0,2.0),(2.5,2.0),(2.0,1.5),(2.0,2.0),(2.0,2.5)]
d_list = [0.635779, 0.704073, 0.7472, 0.635779, 0.704073, 0.7472]

alpha_list = np.array(alpha_list)[[0,3,1,4,2,5]] # reorder for legend
d_list = np.array(d_list)[[0,3,1,4,2,5]]
for i,(alpha_alter,alpha_ego) in enumerate(alpha_list):
    data = pd.read_csv("Aa%0.1f_Ae%0.1f.csv" % (alpha_ego,alpha_alter))
    plt.plot(data["q"].values,data["hx_avg"].values, alpha_alter_style[i], c=alpha_ego_color[i], fillstyle="none", label=r"$\alpha_a=%0.2f, \alpha_e=%0.2f$" % (alpha_alter,alpha_ego))    

    T = 1000*lam
    z = 1/d_list[i]
    theory_L = [T/math.log(z,2) *  ( (1-q)*(math.log(T*z,2) - 1) +
             q/2*(math.log(T*z**(lam+2),2)+(z**lam/T + 1)*math.log(T/z**lam + 1,2) - 2)) for q in q_list]
    theory_hx = [T*math.log(T,2)/L for L in theory_L]
    plt.plot(q_list, theory_hx, c=alpha_ego_color[i])
leg = plt.legend(title=r"$T=1000\lambda$", ncol=3, prop={'size': 8})
leg._legend_box.align = "left"
plt.xlabel(r"Quote probability, $q$")
plt.ylabel(r"Cross-entropy, $h_\times$ [bits]")
plt.show()



