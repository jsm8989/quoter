import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

N=40
q=0.5
T=1000

sbm_p_list = [0.2,0.4,0.6,0.8]
sbm_q_list = [0.2,0.4,0.6,0.8]
trials_list = list(range(200))

##hx_w = np.zeros((len(sbm_p_list),len(sbm_q_list))) # within block
##hx_b = np.zeros((len(sbm_p_list),len(sbm_q_list))) # between block
##for i,p in enumerate(sbm_p_list):
##    for j,mu in enumerate(sbm_q_list):
##        trial_avg_w = count_w = trial_avg_b = count_b = 0
##        for trial in trials_list:
##            if trial % 50 == 0:
##                print(p,mu,trial)
##            efile = "../../data_sbm-p-mu-N40/N%i_p%0.3f_mu%0.4f_q%0.2f_T%i_sim%i.txt" % (N,p,mu,q,T,trial)
##
##            edata = pd.read_csv(efile, sep = " ")
##            
##            block1 = list(range(0,20))
##            block2 = list(range(20,40))
##
##            egos = edata["ego"].values
##            alters = edata["alter"].values
##            hx_list = edata["hx"].values
##            dist_list = edata["distance"].values
##            
##            for ego,alter,hx,d in zip(egos,alters,hx_list,dist_list):
##                
##                if d == 1:
##                    #within block
##                    if (ego in block1 and alter in block1) or (ego in block2 and alter in block2):
##                        trial_avg_w += hx
##                        count_w += 1
##                        
##                    else: # between block
##                        trial_avg_b += hx
##                        count_b += 1
##
##        hx_w[i,j] = trial_avg_w/count_w
##        hx_b[i,j] = trial_avg_b/count_b
##
##np.savetxt("sbm_w.csv",hx_w,delimiter=",")
##np.savetxt("sbm_b.csv",hx_b,delimiter=",")

dataW = pd.read_csv("sbm_w.csv",header=None,sep = ",").values
dataB = pd.read_csv("sbm_b.csv",header=None,sep = ",").values

style = ['r-','k-','b-','g-']
for j in range(len(sbm_q_list)):
    plt.plot(sbm_p_list,dataW[:,j],style[j],label=r"$\mu=%0.1f$" % sbm_q_list[j])
    plt.plot(sbm_p_list,dataB[:,j],style[j]+'-')

plt.legend()
plt.xlabel(r"$p$")
plt.ylabel("Cross-entropy")
plt.show()

