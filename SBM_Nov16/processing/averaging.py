import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N = 1000
m = N//2 
q=0.9
T=1000
p = 0.4
mu_seq = [0.0444, 0.0570857, 0.0705176, 0.0847636, 0.0999,
              0.116013, 0.1332, 0.151572, 0.171257, 0.1924, 0.215169,
              0.23976, 0.2664, 0.295357, 0.326945, 0.361543, 0.3996]
##trials_list = list(range(1000))


##trials_seq = np.array([10,20,50,100,200,500,1000])/2
##for n_trials in trials_seq:
##    n_trials = int(n_trials)
##    W_avg = np.zeros(len(mu_seq))
##    B_avg = np.zeros(len(mu_seq))
##    W_var = np.zeros(len(mu_seq))
##    B_var = np.zeros(len(mu_seq))
##    for i,mu in enumerate(mu_seq):
##        hx_w = []
##        hx_b = []
##        print(i)
##        for trial in range(n_trials):
##            
##            efile = "../data-Nov16/edge/N%i_p%0.2f_mu%0.4f_q%0.2f_T%i_sim%i.txt" % (N,p,mu,q,T,trial)
##            try:
##                edata = pd.read_csv(efile, sep = " ")
##            except:
##                print("No data", p,mu,trial)
##
##            else:
##                
##                hx_w.extend(edata["hx"].loc[edata["ego"]==1].values)
##                hx_b.extend(edata["hx"].loc[edata["ego"]==m].values)
##
##        W_avg[i] = np.mean(hx_w)
##        B_avg[i] = np.mean(hx_b)
##        W_var[i] = np.var(hx_w)
##        B_var[i] = np.var(hx_b)
##        
##    df = pd.DataFrame({"mu":mu_seq,"hx_w_avg":W_avg,"hx_b_avg":B_avg,
##                       "hx_w_var":W_var,"hx_b_var":B_var})
##    df = df.to_csv("sbm_q%0.2f_trials%i.csv" % (q,n_trials), index=False)




## PLOT 1
##trials_seq = np.array([10,20,50,100,200,500,1000])/2
##trials_seq = trials_seq[2:]
##trials_seq2 = [10,20,50,100,200,500,1000]
##trials_seq2 = trials_seq2[2:]
##style=['C%i-' %i for i in range(len(trials_seq))]
##print(style)
##for i,n_trials in enumerate(trials_seq):
##    data = pd.read_csv("sbm_q%0.2f_trials%i.csv" % (q,n_trials))
####    plt.plot(data["mu"],data["hx_w_avg"],style[i],label="within %i" % trials_seq2[i])
##    plt.plot(data["mu"],data["hx_b_avg"],style[i]+'-',label="between %i" % trials_seq2[i])
##plt.xlabel("$\mu$")
##plt.ylabel("Average cross-entropy")
##plt.legend()
##plt.show()


# PLOT 2: subplots
trials_seq = np.array([10,20,50,100,200,500,1000])/2
trials_seq = trials_seq[3:]
trials_seq2 = [10,20,50,100,200,500,1000]
trials_seq2 = trials_seq2[3:]
style=['C%i-' %i for i in range(len(trials_seq))]
fig,ax = plt.subplots(1,4,figsize=(11,4),sharey=True)
for i,n_trials in enumerate(trials_seq):
    plt.sca(ax[i])
    data = pd.read_csv("sbm_q%0.2f_trials%i.csv" % (q,n_trials))
    plt.plot(data["mu"],data["hx_w_avg"],style[i],label="within")
    plt.plot(data["mu"],data["hx_b_avg"],style[i]+'-',label="between")
    plt.xlabel("$\mu$")
    plt.legend()
    plt.title("%i trials" % trials_seq2[i])
    if i==0:
        plt.ylabel("Average cross-entropy")
plt.show()





