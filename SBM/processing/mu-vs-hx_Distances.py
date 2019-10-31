import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

N=2000
M=10000
q_list=[0.5,0.1,0.9]
T=1000
mu_list = np.arange(.05,.51,.05)
trials_list = list(range(300))


##for q in q_list:
##    hx_w_avg = []
##    hx_b_avg = []
##    for i,mu in enumerate(mu_list):
##        hx_w_dist = np.zeros(5)
##        hx_b_dist = np.zeros(5)
##        count_w_dist = np.zeros(5)
##        count_b_dist = np.zeros(5)
##        for trial in trials_list:
##            if trial % 50 == 0:
##                print(mu,trial)
##            efile = "../data/N%i_mu%0.2f_M%i_q%0.2f_T%i_sim%i.txt" % (N,mu,M,q,T,trial)
##
##            edata = pd.read_csv(efile, sep = " ")
##
##            block1 = list(range(0,int(N/2)))
##            block2 = list(range(int(N/2),N))
##
##            for d,dist in enumerate(range(1,6)):
##                w = edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["distance"] ==  dist)].values
##                hx_w_dist[d] += np.sum(w)
##                b = edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["distance"] ==  dist)].values
##                hx_b_dist[d] += np.sum(b)
##                count_w_dist[d] += len(w)
##                count_b_dist[d] += len(b)
##                
##        for d,dist in enumerate(range(1,6)):
##            if count_w_dist[d] > 0:
##                hx_w_dist[d] /= count_w_dist[d]
##            if count_b_dist[d] > 0:
##                hx_b_dist[d] /= count_b_dist[d]
##
##        hx_w_avg.append(hx_w_dist)
##        hx_b_avg.append(hx_b_dist)
##        
##    
##    cols_w = ["hx_w%i" % i for i in range(1,6)]
##    cols_b = ["hx_b%i" % i for i in range(1,6)]
##    df_mu = pd.DataFrame({"mu": mu_list})
##    df_w = pd.DataFrame(data=hx_w_avg,columns=cols_w)
##    df_b = pd.DataFrame(data=hx_b_avg,columns=cols_b)
##    df = pd.concat([df_mu,df_w,df_b],axis=1)
##    df = df.to_csv("sbm_Distances_q%0.2f.csv" % q, index=False)

def SNR(m1,m2,n):
    """ Signal to noise ratio, computed elementwise 
        m1 = sample 1st moment (sample mean) .. can be np.array or pandas
        m2 = sample 2nd moment .. can be np.array or pandas
        n = number of observations .. can be np.array or pandas
    """
    try: # if passed in as pandas
        m1 = m1.values
        m2 = m2.values
        n = n.values
    except:
        pass
    var = m2-np.power(m1,2)
    sample_s = np.sqrt(np.multiply(np.divide(n,n-1),var)) #sqrt( (n/(n-1)) * var)
    return np.divide(m1,sample_s)
    

##data1 = pd.read_csv("sbm_Distances_q0.10.csv")
##data2 = pd.read_csv("sbm_Distances_q0.50.csv")
##data3 = pd.read_csv("sbm_Distances_q0.90.csv")



# PLOT 1: subplots (q,d) mu on x-axis, hx on y-axis, lines labeled within/between
##fig = plt.figure(figsize=(10,6))
##
##q_list = [0.1,0.5,0.9]
##for i,q in enumerate(q_list):
##    data = pd.read_csv("sbm_Distances_q%0.2f.csv" % q)
##    for j,dist in enumerate(range(1,6)):
##        curr_plot = 1+i+3*j
##        hx_w = data["hx_w%i" % dist].values
##        hx_b = data["hx_b%i" % dist].values
##        plt.subplot(5,3,curr_plot)
##        plt.plot(mu_list,hx_w,label=r"$h_x(A|i)$")
##        plt.plot(mu_list,hx_b,label=r"$h_x(B|i)$")
##        plt.title("q = %0.1f, d = %i" % (q,dist))
##        if curr_plot == 1:
##            plt.legend(loc="best",prop={'size': 8})
##        if curr_plot in [14]:
##            plt.xlabel(r"$\mu$")
##        if curr_plot in [7]:
##            plt.ylabel("Cross-entropy")
##        if curr_plot not in [1,4,7,10,13]:
##            plt.yticks([])
##        if curr_plot not in [13,14,15]:
##            plt.xticks([])
##        
##        if curr_plot in [1,2,3]:
##            plt.ylim([3.28,3.38])
##        elif curr_plot in [4,5,6]:
##            plt.ylim([3.374,3.388])
##        elif curr_plot in [7,8,9]:
##            plt.ylim([3.374,3.397])
##        elif curr_plot in [10,11,12]:
##            plt.ylim([3.374,3.399])
##        else:
##            plt.ylim([3.37,3.41])
##
##plt.tight_layout()
##plt.savefig("hx-versus-q-d.pdf")
####plt.show()



### PLOT 2: subplots (q,mu) distance on x-axis, hx on y-axis, lines labeled within/between
##fig = plt.figure(figsize=(10,6))
##
##q_list = [0.1,0.5,0.9]
##mu_list = [0.1, 0.2, 0.3, 0.4, 0.5]
##cols_w = ["hx_w%i" % i for i in range(1,6)]
##cols_b = ["hx_b%i" % i for i in range(1,6)]
##for i,q in enumerate(q_list):
##    data = pd.read_csv("sbm_Distances_q%0.2f.csv" % q)
##    for j,mu in enumerate(mu_list):
##        curr_plot = 1+i+3*j
##        hx_w = data[cols_w].loc[data["mu"] == mu].values[0]
##        hx_b = data[cols_b].loc[data["mu"] == mu].values[0]
##        plt.subplot(5,3,curr_plot)
##        plt.plot(range(1,6),hx_w,label=r"$h_x(A|i)$")
##        plt.plot(range(1,6),hx_b,label=r"$h_x(B|i)$")
##        plt.title("q = %0.1f, mu = %0.2f" % (q,mu))
##        if curr_plot == 1:
##            plt.legend(loc="lower right",prop={'size': 8})
##        if curr_plot in [14]:
##            plt.xlabel("Distance")
##        if curr_plot in [7]:
##            plt.ylabel("Cross-entropy")
##        if curr_plot not in [1,4,7,10,13]:
##            plt.yticks([])
##        if curr_plot not in [13,14,15]:
##            plt.xticks([])
##        
##        if curr_plot in [1,2,3]:
##            plt.ylim([3.28,3.42])
##        elif curr_plot in [4,5,6]:
##            plt.ylim([3.28,3.42])
##        elif curr_plot in [7,8,9]:
##            plt.ylim([3.28,3.42])
##        elif curr_plot in [10,11,12]:
##            plt.ylim([3.28,3.42])
##        else:
##            plt.ylim([3.28,3.42])
##
##plt.tight_layout()
####plt.savefig("hx-versus-q-d.pdf")
##plt.show()



# PLOT 3: subplots q. mu=0.1 only, distance on x-axis, hx on y-axis, lines labeled within/between
##fig = plt.figure(figsize=(10,3))
##
##q_list = [0.1,0.5,0.9]
##mu_list = [0.1, 0.2, 0.3, 0.4, 0.5]
##cols_w = ["hx_w%i" % i for i in range(1,6)]
##cols_b = ["hx_b%i" % i for i in range(1,6)]
##for i,q in enumerate(q_list):
##    data = pd.read_csv("sbm_Distances_q%0.2f.csv" % q)
##    curr_plot = 1+i
##    hx_w = data[cols_w].loc[data["mu"] == 0.1].values[0]
##    hx_b = data[cols_b].loc[data["mu"] == 0.1].values[0]
##    plt.subplot(1,3,curr_plot)
##    print(q,hx_w)
##    plt.plot(range(1,6),hx_w,label=r"$h_x(A|i)$")
##    plt.plot(range(1,6),hx_b,label=r"$h_x(B|i)$")
##    plt.title("q = %0.1f, mu = %0.2f" % (q,0.1))
##    if curr_plot == 1:
##        plt.legend(loc="lower right",prop={'size': 8})
##    if curr_plot in [2]:
##        plt.xlabel("Distance")
##    if curr_plot in [1]:
##        plt.ylabel("Cross-entropy")
##    if curr_plot not in [1]:
##        plt.yticks([])
##    
##    plt.ylim([3.28,3.42])
##
##plt.tight_layout()
##plt.savefig("hx-versus-q-d.pdf")
####plt.show()


