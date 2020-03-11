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

# for z in z_list:
#    for lam in lam_list:
#        print(z,lam)
#        hx_all_q = np.zeros(len(q_list))
#        for i,q in enumerate(q_list):
#            hx_this_q = []
#            for trial in trials_list:
#                efile = "../data_QMpaper-NEW/data_QMpaper-NEW/z%i_q%0.3f_T%i_lam%i_sim%i.txt" % (z,q,T,lam,trial)
#                edata = pd.read_csv(efile, sep = " ")
#                hx_this_q.extend(edata["hx"].values)
#            hx_all_q[i] = np.mean(hx_this_q)

       
#        df = pd.DataFrame({"q":q_list,"hx_avg":hx_all_q})
#        df = df.to_csv("QMpaper-NEW/z%i_lam%i.csv" % (z,lam), index=False)

z_style = ['x','s','o']
lam_color = ['C0','C1','C2']

for i,z in enumerate(z_list):
    for j,lam in enumerate(lam_list):
        data = pd.read_csv("QMpaper-NEW/z%i_lam%i.csv" % (z,lam))
        plt.plot(data["q"].values,data["hx_avg"].values,z_style[i], c=lam_color[j], fillstyle="none", label=r"$z=%i,\lambda=%i$" % (z,lam))    

        T = 1000*lam
        theory_L = [T/math.log(z) *  ( (1-q)*(math.log(T*z) - 1) +
                 q/2*(math.log(T*z**(lam+2))+(z**lam/T + 1)*math.log(T/z**lam + 1) - 2)) for q in q_list]
        theory_hx = [T*math.log(T,2)/L for L in theory_L]

        # only change Lambda_R
        theory_L2 = [T/math.log(z) *  ( (1-q)*(math.log(T*z) - 1 + np.euler_gamma - math.log(z)/2) +
                 q/2*(math.log(T*z**(lam+2))+(z**lam/T + 1)*math.log(T/z**lam + 1) - 2)) for q in q_list]
        theory_hx2 = [T*math.log(T,2)/L for L in theory_L2]

        # change Lambda_R and Lambda_Q
        # theory_L2 = [T/math.log(z) *  ( (1-q)*(math.log(T*z) - 1) +
        #          q/2*(math.log(T*z**(lam+2))+(z**lam/T + 1)*math.log(T/z**lam + 1) - 2)) + T*(np.euler_gamma/math.log(z) - 1/2) for q in q_list]
        # theory_hx2 = [T*math.log(T,2)/L for L in theory_L2]
    
        plt.plot(q_list, theory_hx, c=lam_color[j])
        plt.plot(q_list, theory_hx2, '--'+lam_color[j])

##        #d = 0.18
##        d = 1/z
##        q = q_list[1]
##        s = 0
##        for t in range(T):
##            if t % 40 == 0:
##                print("done", t/T)
##                
##            s1 = 0
####            for l in range(T-t): # expectation of P(Lambda_t = ell|R)
##            for l in range(200): # expectation of P(Lambda_t = ell|R)
##                s1 += l*(1-(1-d**l*(1-d))**t)
##
##            s2 = 0
####            for l in range(T-t): # expectation of P(Lambda_t = ell|Q)
##            for l in range(200): # expectation of P(Lambda_t = ell|Q)
##                s2 += (l+lam)*l*(1-(1-d**l*(1-d))**t)
####                for j in range(50): # message length
####                    s2 += (l+j)*l*(1-(1-d**l*(1-d))**t) * lam**j * math.exp(-lam)/math.factorial(j)
##
##            s += (1-q)*s1 + q*s2
##
##        with open("output.txt","w") as f:
##            f.write(str(T*math.log(T,2)/s) + " " + str(theory_hx[1]))

        
leg = plt.legend(loc="lower left", bbox_to_anchor=(0,0.08), ncol=3, prop={'size': 8})
# leg = plt.legend(title=r"$T=1000\lambda$", loc="lower left", bbox_to_anchor=(0,0.08), ncol=3, prop={'size': 8})
leg._legend_box.align = "left"
plt.xlabel(r"Quote probability, $q$")
plt.ylabel(r"Cross-entropy, $h_\times$ [bits]")
# plt.savefig()
plt.show()



