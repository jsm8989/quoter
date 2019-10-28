import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

N=600
q=0.05
T=1000
mu_list = np.arange(.05,.51,.05)
trials_list = list(range(0,2100))

##hx_w = np.zeros(len(mu_list)) # within block
##hx_b = np.zeros(len(mu_list)) # between block
##hx_all = np.zeros(len(mu_list))
##hx_w2 = np.zeros(len(mu_list)) # within block
##hx_b2 = np.zeros(len(mu_list)) # between block
##hx_all2 = np.zeros(len(mu_list))
##n_w = np.zeros(len(mu_list))
##n_b = np.zeros(len(mu_list))
##n_all = np.zeros(len(mu_list))
##for i,mu in enumerate(mu_list):
##        trial_avg_w = count_w = trial_avg_b = count_b = trial_avg_all = count_all = 0
##        trial_avg_w2 = trial_avg_b2 = trial_avg_all2 =0
##
##        for trial in trials_list:
##            efile = "../data_vary_q-1800/N%i_mu%0.2f_q%0.2f_T%i_sim%i.txt" % (N,mu,q,T,trial)
##
##            try:
##                edata = pd.read_csv(efile, sep = " ")
##                
##                block1 = list(range(0,int(N/2)))
##                block2 = list(range(int(N/2),N))
##
##                egos = edata["ego"].values
##                alters = edata["alter"].values
##                hx_list = edata["hx"].values
##                
##                for ego,alter,hx in zip(egos,alters,hx_list):
##                    if ego == 0:
##                        pass
##                    
##                    #within block
##                    elif ego in block1:
##                        trial_avg_w += hx
##                        trial_avg_w2 += hx**2
##                        count_w += 1
##                        
##                    else: # between block
##                        trial_avg_b += hx
##                        trial_avg_b2 += hx**2
##                        count_b += 1
##                        
##
##                    trial_avg_all += hx
##                    trial_avg_all2 += hx**2
##                    count_all += 1
##
##            except: # no data
##                pass
##
##        print(i)
##
##        hx_w[i] = trial_avg_w/count_w
##        hx_b[i] = trial_avg_b/count_b
##        hx_all[i] = trial_avg_all/count_all
##        hx_w2[i] = trial_avg_w2/count_w
##        hx_b2[i] = trial_avg_b2/count_b
##        hx_all2[i] = trial_avg_all2/count_all
##        n_w[i] = count_w
##        n_b[i] = count_b
##        n_all[i] = count_all
##        print(hx_w)
##
##
##    
##
##df = pd.DataFrame({"mu":mu_list,"hx_w":hx_w,"hx_b":hx_b,"hx_all":hx_all,
##                   "hx_w2":hx_w2,"hx_b2":hx_b2,"hx_all2":hx_all2,
##                   "n_w":n_w,"n_b":n_b,"n_all":n_all})
##df = df.to_csv("sbm_seed_N600_q0.05_tri2100.csv",index=False)

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
    
##data1 = pd.read_csv("sbm_seed_N600_q0.05_tri2100.csv")
##data1_w_SNR = SNR(data1["hx_w"],data1["hx_w2"],data1["n_w"])
##data1_b_SNR = SNR(data1["hx_b"],data1["hx_b2"],data1["n_b"])
##plt.plot(data1["mu"],data1_w_SNR,label=r"$h_x(A|i)$")
##plt.plot(data1["mu"],data1_b_SNR,label=r"$h_x(B|i)$")
##plt.xlabel(r"$\mu$")
##plt.ylabel("SNR")
##plt.legend()
##plt.show()

data1 = pd.read_csv("../sbm_seed_N600_q0.05_tri300.csv")
data2 = pd.read_csv("../sbm_seed_N600_q0.05_tri600.csv")
data3 = pd.read_csv("../sbm_seed_N600_q0.05_tri1200.csv")

fig = plt.figure(figsize=(10,3))

plt.subplot(1,3,1)
data1_w_SNR = data1["hx_w"].values
plt.plot(data1["mu"],data1["hx_w"],label=r"$h_x(A|i)$")
plt.plot(data1["mu"],data1["hx_b"],label=r"$h_x(B|i)$")
plt.xlabel(r"$\mu$")
plt.ylabel("Mean cross-entropy")
plt.ylim([3.3758,3.3786])
plt.legend()
plt.title(r"300 trials")

plt.subplot(1,3,2)
plt.plot(data2["mu"],data2["hx_w"],label=r"$h_x(A|i)$")
plt.plot(data2["mu"],data2["hx_b"],label=r"$h_x(B|i)$")
plt.xlabel(r"$\mu$")
plt.ylabel("Mean cross-entropy")
plt.ylim([3.3758,3.3786])
plt.legend()
plt.title(r"600 trials")

plt.subplot(1,3,3)
plt.plot(data3["mu"],data3["hx_w"],label=r"$h_x(A|i)$")
plt.plot(data3["mu"],data3["hx_b"],label=r"$h_x(B|i)$")
plt.xlabel(r"$\mu$")
plt.ylabel("Mean cross-entropy")
plt.ylim([3.3758,3.3786])
plt.legend()
plt.title(r"1200 trials")


plt.tight_layout()
plt.show()



