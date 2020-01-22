import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import scipy.stats

N = 100
q_list = [0, 0.1, .2, 0.3, .4, 0.5, .6, 0.7, .8, .9, .99, .999, 1]
lam_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
k_list = [5, 10, 15, 20, 25]
T = 1000
trials_list = list(range(100))




# DENSITY VERSUS AVERAGE CROSS ENTROPY
##for k in k_list:
##    data = np.zeros((len(q_list),len(lam_list)))
##    for i,q in enumerate(q_list):
##        for j,lam in enumerate(lam_list):
##            print("k%i q%0.4f lambda%i" % (k,q,lam))
##            hx_list = []
##            for trial in trials_list:
##                if k in [5,20] and q in [0,.2,.4,.6,.8,.9,1] and lam in [1,2,4,6,8]:
##                    efile = "../data_ER/edge/N%i_k%i_q%0.1f_lam%i_T%i_sim%i.txt" % (N,k,q,lam,T,trial)
##            
##                else:
##                    efile = "../data_ER/edge/N%i_k%i_q%0.4f_lam%i_T%i_sim%i.txt" % (N,k,q,lam,T,trial)
##                
##
##                if os.path.isfile(efile):  
##                    edata = pd.read_csv(efile, sep = " ")
##                    hx_list.extend(edata["hx"].values)
##                        
##                else:
##                    print("file not found",k,q,lam,trial)
##                                                
##                        
##            data[i,j] = np.mean(hx_list)
##
##    df = pd.DataFrame(data=data)
##    df.to_csv("Jan-21/hx_ER_k%i.csv" % k, header=False, index=False)


data1 = np.loadtxt("Jan-20/hx_ER_k%i.csv" % 5, delimiter=",")
data2 = np.loadtxt("Jan-20/hx_ER_k%i.csv" % 20, delimiter=",")

plt.imshow(np.subtract(data2,data1), origin="lower")
plt.colorbar()
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
plt.title(r"$\langle h_\times \rangle_{k = 20} - \langle h_\times\rangle_{k = 5}$")
plt.show()


def spearmans_rank_correlation(xs, ys):
    
    # Calculate the rank of x's
    xranks = pd.Series(xs).rank()
    
    # Caclulate the ranking of the y's
    yranks = pd.Series(ys).rank()
    
    # Calculate Pearson's correlation coefficient on the ranked versions of the data
    return scipy.stats.pearsonr(xranks, yranks)



# store Spearman's correlation coefficient in data
data = np.zeros((len(q_list),len(lam_list)))

for i,_ in enumerate(q_list):
    for j,_ in enumerate(lam_list):
        A = [] # append <hx> for each k
        for k in k_list:
            data_q_lam = np.loadtxt("Jan-20/hx_ER_k%i.csv" % k, delimiter=",")
            A.append(data_q_lam[i,j])
        data[i,j] = scipy.stats.spearmanr(k_list, A)[0]
print(data)
        
plt.imshow(data, origin="lower")
plt.colorbar()
plt.xticks(range(len(lam_list)), lam_list)
plt.yticks(range(len(q_list)),q_list)
plt.xlabel(r"Quote length, $\lambda$")
plt.ylabel(r"Quote probability, $q$")
plt.title(r"Spearman's correlation of $\langle h_\times \rangle$ for $\langle k \rangle = 5,10,15,20,25$")
plt.show()
        

            
            


        
        
