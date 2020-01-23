import numpy as np
import pandas as pd
import os

N = 100
q = 0.9
T = 1000
alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5)]

# this combination generates modularity = [-.20,-.15,-.10,...,.20,.25,.30]
p_list = [0.0655977,0.0824176,0.102041,0.125232,0.153061,
          0.187075,0.229592,0.284257,0.357143,0.459184,0.612245]

mu = 0.15

trials_list = list(range(1000))

W = np.zeros(len(p_list)) # avg hx on edges entirely within either block (i.e. AA or BB)
B = np.zeros(len(p_list)) # avg hx on edges which cross blocks (i.e. AB or BA)
AA = np.zeros(len(p_list)) # avg hx on edges of form i-->j where i in A, j in A
AB = np.zeros(len(p_list)) # avg hx on edges of form i-->j where i in A, j in B
BA = np.zeros(len(p_list)) # ETC...
BB = np.zeros(len(p_list)) # ETC...

for alpha in alpha_list:
    alpha_A = alpha[0]
    alpha_B = alpha[1]
    for j,p in enumerate(p_list):
        print(alpha,j)
        hx_AA, hx_AB, hx_BA, hx_BB = [], [], [], []
        for trial in trials_list:
            efile = "../data-Jan20/edge/N%i_p%0.2f_mu%0.2f_aA%0.1f_aB_%0.1f_q%0.1f_T%i_sim%i.txt" % (N,p,mu,alpha_A,alpha_B,q,T,trial)
            try:
                edata = pd.read_csv(efile, sep = " ")
            except:
                print("No data",alpha,p,trial)

            else:
                
                block1 = list(range(0,int(N/2)))
                block2 = list(range(int(N/2),N))

                data_AA = edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block1))].values
                data_BB = edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block2))].values
                data_AB = edata["hx"].loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block2))].values
                data_BA = edata["hx"].loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block1))].values
                hx_AA.extend(data_AA)
                hx_BB.extend(data_BB)
                hx_AB.extend(data_AB)
                hx_BA.extend(data_BA)

        W[j] = np.mean(hx_AA+hx_BB)
        B[j] = np.mean(hx_AB+hx_BA)
        AA[j] = np.mean(hx_AA)
        BB[j] = np.mean(hx_BB)
        AB[j] = np.mean(hx_AB)
        BA[j] = np.mean(hx_BA)
        

    df = pd.DataFrame(data={"p":p_list,"hx_w":W,"hx_b":B,
                            "AA":AA,"BB":BB,"AB":AB,"BA":BA})
    df.to_csv("sbm_2param_aA%0.1f_aB%0.1f.csv" % (alpha_A,alpha_B), index=False)



