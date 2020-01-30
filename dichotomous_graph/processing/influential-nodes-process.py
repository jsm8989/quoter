import numpy as np
import pandas as pd
import os

# There's something glitchy with this script. Works if you manually set
# N = [250] and rerun, but otherwise outputs a matrix of zeros.


# Uncomment this to process avg degree = 64
##k1_list = np.arange(4,36,4) # k1+k2=64
##k2_list = 64-np.arange(4,36,4)
##K = 64

k1_list = np.arange(2,18,2) # k1+k2=32
k2_list = 32-np.arange(2,18,2)
K = 32

k1k2_list = zip(k1_list,k2_list)

n_list = [500]
q = 0.5
T = 1000
trials_list = list(range(500))


for n in n_list:
    n1 = n2 = n
    data = np.zeros((23,len(k1_list)))
    for i,(k1,k2) in enumerate(k1k2_list):
        print(n,k1,k2)
        hx = []
        hx11 = []
        hx12 = []
        hx21 = []
        hx22 = []
        hx1X = []
        hx2X = []
        hxX1 = []
        hxX2 = []
        deg = 0
        dens = 0
        clus = 0
        count = 0
            
        for trial in trials_list:
                efile = "../data2/edge/N1%i_N2%i_k1%i_k2%i_q%0.1f_T%i_sim%i.txt" % (n1,n2,k1,k2,q,T,trial)
                gfile = "../data2/graph/N1%i_N2%i_k1%i_k2%i_q%0.1f_T%i_sim%i.txt" % (n1,n2,k1,k2,q,T,trial)

                if os.path.isfile(efile) and os.path.isfile(gfile):  
                        edata = pd.read_csv(efile, sep = " ")
                        gdata = pd.read_csv(gfile, sep = " ")
                        
                        hx.extend(edata["hx"].values)
                        hx11.extend(edata["hx"].loc[(edata["alter"] < n) & (edata["ego"] < n)].values)
                        hx12.extend(edata["hx"].loc[(edata["alter"] < n) & (edata["ego"] > n)].values)
                        hx21.extend(edata["hx"].loc[(edata["alter"] > n) & (edata["ego"] < n)].values)
                        hx22.extend(edata["hx"].loc[(edata["alter"] > n) & (edata["ego"] > n)].values)

                        hx1X.extend(edata["hx"].loc[(edata["alter"] < n)].values)
                        hx2X.extend(edata["hx"].loc[(edata["alter"] > n)].values)
                        hxX1.extend(edata["hx"].loc[(edata["ego"] < n)].values)
                        hxX2.extend(edata["hx"].loc[(edata["ego"] > n)].values)

                        deg += gdata["average_degree"].values[0]
                        dens += gdata["density"].values[0]
                        clus += gdata["transitivity"].values[0]
                        count += 1
                else:
                    print("no data", n, k1, k2, trial)

        data[0,i] = np.mean(hx)
        data[1,i] = np.var(hx)
        
        data[2,i] = np.mean(hx11)
        data[3,i] = np.var(hx11)
        
        data[4,i] = np.mean(hx12)
        data[5,i] = np.var(hx12)
        
        data[6,i] = np.mean(hx21)
        data[7,i] = np.var(hx21)
        
        data[8,i] = np.mean(hx22)
        data[9,i] = np.var(hx22)
        
        data[10,i] = np.mean(hx1X)
        data[11,i] = np.var(hx1X)
        
        data[12,i] = np.mean(hx2X)
        data[13,i] = np.var(hx2X)

        data[14,i] = np.mean(hxX1)
        data[15,i] = np.var(hxX1)
        
        data[16,i] = np.mean(hxX2)
        data[17,i] = np.var(hxX2)
        
        data[18,i] = dens/count
        data[19,i] = clus/count
        data[20,i] = deg/count
        data[21,i] = k1/k2
        data[22,i] = k1**2/4 + k2**2/4 - k1*k2/2

    cols = ["hx_avg", "hx_var",
            "hx11_avg", "hx11_var",
            "hx12_avg", "hx12_var",
            "hx21_avg", "hx21_var",
            "hx22_avg", "hx22_var",
            "hx1X_avg", "hx1X_var",
            "hx2X_avg", "hx2X_var",
            "hxX1_avg", "hxX1_var",
            "hxX2_avg", "hxX2_var",
            "density", "transitvity",
            "average_degree", "degree_ratio", "degree_variance"]
    df = pd.DataFrame(data=data.transpose(),columns=cols)

        
    df.to_csv("hx_dichotomous_n%i_k1k2%i_q%0.1f.csv" % (n,K,q), index=False)

