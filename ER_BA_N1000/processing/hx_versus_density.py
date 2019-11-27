import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

N = 1000
q_list = [0.5]
T = 1000
trials_list = list(range(200))

param_list = np.arange(2,51,2) # for ER
##param_list = list(range(1,21+1)) + list(range(23,26+1)) # for BA

ERparam = np.arange(2,51,2) # for ER
BAparam = list(range(1,21+1)) + list(range(23,26+1)) # for BA
BAparam = [2*m - 2*m**2/N for m in BAparam]


####### DENSITY VERSUS AVERAGE CROSS ENTROPY
##for q in q_list:
##    data = np.zeros((6,len(param_list)))
##    for i,x in enumerate(param_list):
##        hx_list = []
##        deg = 0
##        dens = 0
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
##        data[2,i] = dens/count
##        data[3,i] = clus/count
##        data[4,i] = assort/count
##        data[5,i] = deg/count
##        
##        print(x, "done")
##
##    df = pd.DataFrame({"hx_avg":data[0,:],"hx_std":data[1,:],
##                       "density":data[2,:],"transitivity":data[3,:],
##                       "assortativity":data[4,:],"average_degree":data[5,:]})
##    df = df.to_csv("hx_ER_q%0.1f.csv" % q,index=False)



### PLOT: DENSITY VERSUS AVERAGE CROSS ENTROPY
##fig, ax = plt.subplots(1,3,figsize=(10,3))
##plt.sca(ax[0])
##ER = pd.read_csv("hx_ER_q0.5.csv")
##BA = pd.read_csv("hx_BA_q0.5.csv")
##
##plt.plot(ERparam,ER["hx_avg"],'ko',label="ER")
##plt.plot(BAparam,BA["hx_avg"],'ro',label="BA")
##plt.xlabel(r"$\langle k \rangle$")
##plt.ylabel("Average cross-entropy")
##plt.legend()
##
##
##
# DENSITY VERSUS AVERAGE NODE ENTROPY
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
##
##
### PLOT: DENSITY VERSUS AVERAGE NODE ENTROPY
##ER = pd.read_csv("h_ER_q0.5.csv")
##BA = pd.read_csv("h_BA_q0.5.csv")
##
##plt.sca(ax[1])
##plt.plot(ERparam,ER["h_avg"],'ko',label="ER")
##plt.plot(BAparam,BA["h_avg"],'ro',label="BA")
##plt.xlabel(r"$\langle k \rangle$")
##plt.ylabel("Average node entropy")
##
##
##
### PLOT: AVERAGE NODE ENTROPY & AVERAGE CROSS-ENTROPY VS DENSITY FOR Q = 0.5
##ERH = pd.read_csv("h_ER_q0.5.csv")
##BAH = pd.read_csv("h_BA_q0.5.csv")
##ER = pd.read_csv("hx_ER_q0.5.csv")
##BA = pd.read_csv("hx_BA_q0.5.csv")
##
##plt.sca(ax[2])
##plt.plot(ERparam,ER["hx_avg"]-ERH["h_avg"],'ko',label=r"ER")
##plt.plot(BAparam,BA["hx_avg"]-BAH["h_avg"],'ro',label=r"BA")
##plt.xlabel(r"$\langle k \rangle$")
##plt.ylabel(r"$\langle h_\times - h \rangle$")
##
##plt.tight_layout()
##plt.show()


# PLOT: AVERAGE NODE ENTROPY VS AVERAGE CROSS-ENTROPY
##plt.plot(ERH["h_avg"],ER["hx_avg"],'ko',label="ER")
##plt.plot(BAH["h_avg"],BA["hx_avg"],'ro',label="BA")
##plt.xlabel("Average node entropy")
##plt.ylabel("Average cross-entropy")
##plt.legend()
##plt.show()


# PLOT: Stdev (or variance) of entropy vs density for N=100 vs N=1000
##fig,ax = plt.subplots(1,2,figsize=(8,3),sharey=True)
##ER = pd.read_csv("hx_ER_q0.5.csv")
##BA = pd.read_csv("hx_BA_q0.5.csv")
##
##plt.sca(ax[1])
##plt.plot(ERparam,ER["hx_std"],'ko',label="ER")
##plt.plot(BAparam,BA["hx_std"],'ro',label="BA")
##plt.xlabel(r"$\langle k \rangle$")
##plt.title(r"$N=1000$")
##
##ER = pd.read_csv("../../ER_BA_selfEntropy/processing/hx_ER_q0.5.csv")
##BA = pd.read_csv("../../ER_BA_selfEntropy/processing/hx_BA_q0.5.csv")
##
##N=100
##ERparam =  np.arange(5,51,5) # for ER
##BAparam = [ 3,  5,  8, 11, 15, 18, 23, 28, 34, 50] # for BA
##BAparam = [2*m - 2*m**2/N for m in BAparam]
##
##plt.sca(ax[0])
##plt.plot(ERparam[1::2],ER["hx_std"].values[1::2],'ko',label="ER")
##plt.plot(BAparam[1::2],BA["hx_std"].values[1::2],'ro',label="BA")
##plt.legend()
##plt.xlabel(r"$\langle k \rangle$")
##plt.ylabel("Cross-entropy standard deviation")
##plt.title(r"$N=100$")
##plt.show()

# Plot: same as above, but for N=1000 only & with more values of <k>
BAparam = list(range(1,21+1)) + list(range(22,25+1)) # for BA
BAparam = [2*m - 2*m**2/N for m in BAparam]
ER = pd.read_csv("hx_ER_q0.5.csv")
BA = pd.read_csv("hx_BA_q0.5.csv")
ERH = pd.read_csv("h_ER_q0.5.csv")
BAH = pd.read_csv("h_BA_q0.5.csv")

##plt.plot(ERparam,ER["hx_avg"]-ERH["h_avg"],'ko',label="ER")
##plt.plot(BAparam,BA["hx_avg"]-BAH["h_avg"],'ro',label="BA")
##plt.ylabel(r"$\langle h_\times - h\rangle$")

plt.plot(ERparam,ER["hx_std"],'ko',label="ER")
plt.plot(BAparam,BA["hx_std"],'ro',label="BA")
plt.ylabel("Cross-entropy standard deviation")

plt.xlabel(r"$\langle k \rangle$")
plt.legend()
plt.show()
