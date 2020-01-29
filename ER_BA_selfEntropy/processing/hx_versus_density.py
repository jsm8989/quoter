import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

N = 100
q_list = [0.1,0.5,0.9]
T = 1000
trials_list = list(range(200))

##param_list = np.arange(5,51,5) # for ER
####param_list = [ 3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA
##
### DENSITY VERSUS AVERAGE CROSS ENTROPY
##for q in q_list:
##    data = np.zeros((7,len(param_list)))
##    for i,x in enumerate(param_list):
##        hx_list = []
##        deg = 0
##        dens = 0
##        ASPL = 0
##        clus = 0
##        assort = 0
##        count = 0
##        for trial in trials_list:
##            efile = "../data_ER/edge/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
##            gfile = "../data_ER/graph/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
##            if os.path.isfile(efile):  
##                edata = pd.read_csv(efile, sep = " ")
##                gdata = pd.read_csv(gfile, sep = " ")
##                hx_list.extend(edata["hx"].values)
##
##                deg += gdata["average_degree"].values[0]
##                dens += gdata["density"].values[0]
##                ASPL += gdata["average_shortest_path_length"].values[0]
##                clus += gdata["transitivity"].values[0]
##                assort += gdata["assortativity"].values[0]
##                count += 1
##                
##        ##    "nodes edges density average_degree min_indegree max_indegree " +
##        ##   "min_outdegree max_outdegree transitivity average_clustering " +
##        ##  "average_shortest_path_length assortativity "
##        
##        data[0,i] = np.mean(hx_list)
##        data[1,i] = np.std(hx_list)
##        data[2,i] = ASPL/count
##        data[3,i] = dens/count
##        data[4,i] = clus/count
##        data[5,i] = assort/count
##        data[6,i] = deg/count
##        
##        print(x, "done")
##
##    df = pd.DataFrame({"hx_avg":data[0,:],"hx_std":data[1,:],"ASPL":data[2,:],
##                       "density":data[3,:],"transitivity":data[4,:],
##                       "assortativity":data[5,:],"average_degree":data[6,:]})
##    df = df.to_csv("hx_ER_q%0.1f.csv" % q,index=False)



### PLOT: DENSITY VERSUS AVERAGE CROSS ENTROPY
##ERparam = np.arange(5,51,5) # for ER
##BAparam = [ 3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA
##
##ER1 = pd.read_csv("hx_ER_q0.1.csv")
##ER2 = pd.read_csv("hx_ER_q0.5.csv")
##ER3 = pd.read_csv("hx_ER_q0.9.csv")
##BA1 = pd.read_csv("hx_BA_q0.1.csv")
##BA2 = pd.read_csv("hx_BA_q0.5.csv")
##BA3 = pd.read_csv("hx_BA_q0.9.csv")
##
##fig, axes = plt.subplots(1, 3, figsize=(10,3), sharey=True)
##axes = axes.flatten()
##plt.sca(axes[0])
##plt.plot(ERparam,ER1["hx_avg"],'ko',label="ER")
##plt.plot(BAparam,BA1["hx_avg"],'ro',label="BA")
##plt.xlabel(r"$\langle k \rangle$")
##plt.ylabel("Average cross-entropy")
##plt.title(r"$q = 0.1$")
##plt.legend()
##
##plt.sca(axes[1])
##plt.plot(ERparam,ER2["hx_avg"],'ko')
##plt.plot(BAparam,BA2["hx_avg"],'ro')
##plt.xlabel(r"$\langle k \rangle$")
##plt.title(r"$q = 0.5$")
##
##plt.sca(axes[2])
##plt.plot(ERparam,ER3["hx_avg"],'ko')
##plt.plot(BAparam,BA3["hx_avg"],'ro')
##plt.xlabel(r"$\langle k \rangle$")
##plt.title(r"$q = 0.9$")
##
##plt.tight_layout()
##plt.show()



### DENSITY VERSUS AVERAGE NODE ENTROPY
##data = np.zeros((2,len(param_list)))
##for q in q_list:
##    for i,x in enumerate(param_list):
##        h_list = []
##        for trial in trials_list:
##            efile = "../data_ER/edge/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
##            nfile = "../data_ER/node/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
##            gfile = "../data_ER/graph/N%i_k%i_q%0.1f_T%i_sim%i.txt" % (N,x,q,T,trial)
##            if os.path.isfile(efile):  
##    ##            edata = pd.read_csv(efile, sep = " ")
##                ndata = pd.read_csv(nfile, sep = " ")
##    ##            gdata = pd.read_csv(gfile, sep = " ")
##                
##                h_list.extend(ndata["h"].values)
##        
##        data[0,i] = np.mean(h_list)
##        data[1,i] = np.std(h_list)
##        
##        print(x, "done")
##
##    df = pd.DataFrame({"h_avg":data[0,:],"h_std":data[1,:]})
##    df = df.to_csv("h_ER_q%0.1f.csv" % q,index=False)


# PLOT: DENSITY VERSUS AVERAGE NODE ENTROPY
##ERparam = np.arange(5,51,5) # for ER
##BAparam = [ 3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA
##
##ER1 = pd.read_csv("h_ER_q0.1.csv")
##ER2 = pd.read_csv("h_ER_q0.5.csv")
##ER3 = pd.read_csv("h_ER_q0.9.csv")
##BA1 = pd.read_csv("h_BA_q0.1.csv")
##BA2 = pd.read_csv("h_BA_q0.5.csv")
##BA3 = pd.read_csv("h_BA_q0.9.csv")
##
##fig, axes = plt.subplots(1, 3, figsize=(10,3), sharey=True)
##axes = axes.flatten()
##plt.sca(axes[0])
##plt.plot(ERparam,ER1["h_avg"],'ko',label="ER")
##plt.plot(BAparam,BA1["h_avg"],'ro',label="BA")
##plt.xlabel(r"$\langle k \rangle$")
##plt.ylabel("Average NODE entropy")
##plt.title(r"$q = 0.1$")
##plt.legend()
##
##plt.sca(axes[1])
##plt.plot(ERparam,ER2["h_avg"],'ko')
##plt.plot(BAparam,BA2["h_avg"],'ro')
##plt.xlabel(r"$\langle k \rangle$")
##plt.title(r"$q = 0.5$")
##
##plt.sca(axes[2])
##plt.plot(ERparam,ER3["h_avg"],'ko')
##plt.plot(BAparam,BA3["h_avg"],'ro')
##plt.xlabel(r"$\langle k \rangle$")
##plt.title(r"$q = 0.9$")
##
##plt.tight_layout()
##plt.show()



# PLOT: AVERAGE NODE ENTROPY & AVERAGE CROSS-ENTROPY VS DENSITY FOR Q = 0.5
ERparam = np.arange(5,51,5) # for ER
BAparam = [ 3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA
BAparam = [2*m - 2*m**2/N for m in BAparam]
ER1H = pd.read_csv("h_ER_q0.1.csv")
ER2H = pd.read_csv("h_ER_q0.5.csv")
ER3H = pd.read_csv("h_ER_q0.9.csv")
BA1H = pd.read_csv("h_BA_q0.1.csv")
BA2H = pd.read_csv("h_BA_q0.5.csv")
BA3H = pd.read_csv("h_BA_q0.9.csv")
ER1 = pd.read_csv("hx_ER_q0.1.csv")
ER2 = pd.read_csv("hx_ER_q0.5.csv")
ER3 = pd.read_csv("hx_ER_q0.9.csv")
BA1 = pd.read_csv("hx_BA_q0.1.csv")
BA2 = pd.read_csv("hx_BA_q0.5.csv")
BA3 = pd.read_csv("hx_BA_q0.9.csv")

fig, axes = plt.subplots(1, 3, figsize=(10,3), sharey=True)
axes = axes.flatten()
plt.sca(axes[0])
plt.plot(ERparam,ER1["hx_avg"].values,'ko',label="ER")
plt.plot(BAparam,BA1["hx_avg"].values,'ro',label="BA")
plt.xlabel(r"$\langle k \rangle$")
plt.ylabel(r"$\langle h_\times \rangle$")
plt.title(r"$q = 0.1$")
plt.legend()

plt.sca(axes[1])
plt.plot(ERparam,ER2["hx_avg"].values,'ko')
plt.plot(BAparam,BA2["hx_avg"].values,'ro')
plt.xlabel(r"$\langle k \rangle$")
plt.title(r"$q = 0.5$")

plt.sca(axes[2])
plt.plot(ERparam,ER3["hx_avg"].values,'ko')
plt.plot(BAparam,BA3["hx_avg"].values,'ro')
plt.xlabel(r"$\langle k \rangle$")
plt.title(r"$q = 0.9$")

plt.tight_layout()
plt.show()


# PLOT: AVERAGE NODE ENTROPY VS AVERAGE CROSS-ENTROPY
##fig, axes = plt.subplots(1, 3, figsize=(10,3), sharey=True)
##axes = axes.flatten()
##plt.sca(axes[0])
##plt.plot(ER1H["h_avg"],ER1["hx_avg"],'ko',label="ER")
##plt.plot(BA1H["h_avg"],BA1["hx_avg"],'ro',label="BA")
##plt.xlabel("Average node entropy")
##plt.ylabel("Average cross-entropy")
##plt.title(r"$q = 0.1$")
##plt.legend()
##
##plt.sca(axes[1])
##plt.plot(ER2H["h_avg"],ER2["hx_avg"],'ko')
##plt.plot(BA2H["h_avg"],BA2["hx_avg"],'ro')
##plt.xlabel("Average node entropy")
##plt.ylabel("Average cross-entropy")
##plt.title(r"$q = 0.5$")
##
##plt.sca(axes[2])
##plt.plot(ER3H["h_avg"],ER3["hx_avg"],'ko')
##plt.plot(BA3H["h_avg"],BA3["hx_avg"],'ro')
##plt.xlabel("Average node entropy")
##plt.ylabel("Average cross-entropy")
##plt.title(r"$q = 0.9$")
##
##plt.tight_layout()
##plt.show()


