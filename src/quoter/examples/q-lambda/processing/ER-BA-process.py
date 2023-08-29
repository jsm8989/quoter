import numpy as np
import pandas as pd
import os

N = 100
q_list = [0, 0.1, .2, 0.3, .4, 0.5, .6, 0.7, .8, .9, .99, .999, 1]
lam_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
k_list = [5, 10, 15, 20, 25]
T = 1000
trials_list = list(range(100))


# average hx vs average degree
for k in k_list:
    data = np.zeros((len(q_list),len(lam_list)))
    for i,q in enumerate(q_list):
        for j,lam in enumerate(lam_list):
            print("k%i q%0.4f lambda%i" % (k,q,lam))
            hx_list = []
            for trial in trials_list:
                # file name format was changed in the second batch of simulations
                if k in [5,20] and q in [0,.2,.4,.6,.8,.9,1] and lam in [1,2,4,6,8]:
                    efile = "../data_ER/edge/N%i_k%i_q%0.1f_lam%i_T%i_sim%i.txt" % (N,k,q,lam,T,trial)
            
                else:
                    efile = "../data_ER/edge/N%i_k%i_q%0.4f_lam%i_T%i_sim%i.txt" % (N,k,q,lam,T,trial)
                

                if os.path.isfile(efile):  
                    edata = pd.read_csv(efile, sep = " ")
                    hx_list.extend(edata["hx"].values)
                        
                else:
                    print("file not found",k,q,lam,trial)
                                                
                        
            data[i,j] = np.mean(hx_list)

    df = pd.DataFrame(data=data)
    df.to_csv("Jan-20/hx_ER_k%i.csv" % k, header=False, index=False)



        

            
            


        
        
