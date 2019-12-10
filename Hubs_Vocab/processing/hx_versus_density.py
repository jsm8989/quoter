import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt

N = 1000
T = 1000
q=0.5
trials_list = list(range(200))

param_list = np.arange(2,51,2) # for ER
##param_list = list(range(1,21+1)) + list(range(23,26+1)) # for BA
alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5),(1.5,2.0),(2.5,2.0)]

ERparam = np.arange(2,51,2) # for ER
BAparam = list(range(1,21+1)) + list(range(23,26+1)) # for BA
BAparam = [2*m - 2*m**2/N for m in BAparam]


### DENSITY VERSUS AVERAGE CROSS ENTROPY
##for alphas in alpha_list:
##    alpha = alphas[0]
##    hub_alpha = alphas[1]
##    data = np.zeros((5,len(param_list)))
##    for i,x in enumerate(param_list):
##        hx_list = []
##        deg = 0
##        dens = 0
##        clus = 0
##        count = 0
##        for trial in trials_list:
##            efile = "../data_ER-Dec2/edge/N%i_k%i_A%0.1f_HA%0.1f_q%0.1f_T%i_sim%i.txt" % (N,x,alpha,hub_alpha,q,T,trial)
##            gfile = "../data_ER-Dec2/graph/N%i_k%i_A%0.1f_HA%0.1f_q%0.1f_T%i_sim%i.txt" % (N,x,alpha,hub_alpha,q,T,trial)
##            if os.path.isfile(efile):
##                edata = pd.read_csv(efile, sep = " ")
##                gdata = pd.read_csv(gfile, sep = " ")
##                hx_list.extend(edata["hx"].values)
##
##                deg += gdata["average_degree"].values[0]
##                dens += gdata["density"].values[0]
##                clus += gdata["transitivity"].values[0]
##                count += 1
##        
##        data[0,i] = np.mean(hx_list)
##        data[1,i] = np.std(hx_list)
##        data[2,i] = dens/count
##        data[3,i] = clus/count
##        data[4,i] = deg/count
##        
##        print(alphas,x, "done")
##
##    df = pd.DataFrame({"hx_avg":data[0,:],"hx_std":data[1,:],
##                       "density":data[2,:],"transitivity":data[3,:],
##                       "average_degree":data[4,:]})
##    df = df.to_csv("hx_ER_A%0.1f_HA%0.1F_q%0.1f.csv" % (alpha,hub_alpha,q),index=False)
##


# DENSITY VERSUS AVERAGE NODE ENTROPY
##data = np.zeros((2,len(param_list)))
##for alphas in alpha_list:
##    alpha = alphas[0]
##    hub_alpha = alphas[1]
##    for i,x in enumerate(param_list):
##        h_list = []
##        for trial in trials_list:
##            nfile = "../data_ER-Dec2/node/N%i_k%i_A%0.1f_HA%0.1f_q%0.1f_T%i_sim%i.txt" % (N,x,alpha,hub_alpha,q,T,trial)
##            if os.path.isfile(nfile):
##                try:
##                    ndata = pd.read_csv(nfile, sep = " ")
##                    h_list.extend(ndata["h"].values)
##                except:
##                    print("error: empty file")
##        
##        data[0,i] = np.mean(h_list)
##        data[1,i] = np.std(h_list)
##        
##        print(alphas,x, "done")
##
##    df = pd.DataFrame({"h_avg":data[0,:],"h_std":data[1,:]})
##    df = df.to_csv("h_ER_A%0.1f_HA%0.1F_q%0.1f.csv" % (alpha,hub_alpha,q),index=False)




# Plot
##ERparam =  np.arange(2,51,2) # for ER
##BAparam = list(range(1,21+1)) + list(range(22,25+1)) # for BA
##BAparam = [2*m - 2*m**2/N for m in BAparam]
##style = ['-','x','o','--']
##alpha_list = [(1.5,1.5),(1.5,2.5),(2.5,1.5),(2.5,2.5)]
##
##fig, ax = plt.subplots(1,2,figsize=(8,3),sharey=False)
##for i,alphas in enumerate(alpha_list):
##    alpha = alphas[0]
##    hub_alpha = alphas[1]
##    ER = pd.read_csv("hx_ER_A%0.1f_HA%0.1F_q%0.1f.csv" % (alpha,hub_alpha,q))
##    BA = pd.read_csv("hx_BA_A%0.1f_HA%0.1F_q%0.1f.csv" % (alpha,hub_alpha,q))
##    ERH = pd.read_csv("h_ER_A%0.1f_HA%0.1F_q%0.1f.csv" % (alpha,hub_alpha,q))
##    BAH = pd.read_csv("h_BA_A%0.1f_HA%0.1F_q%0.1f.csv" % (alpha,hub_alpha,q))
##
##    plt.sca(ax[0])
##    plt.plot(ERparam,ER["hx_avg"]-ERH["h_avg"],'k'+style[i],label=r"$\alpha=%0.1f, \alpha_{hub}=%0.1f$" %(alpha,hub_alpha))
##    plt.plot(BAparam,BA["hx_avg"]-BAH["h_avg"],'r'+style[i])
##    plt.xlabel(r"$\langle k \rangle$")
##    plt.ylabel(r"$\langle h_\times - h\rangle$")
##    plt.title("Black = ER, Red = BA")
##    plt.legend() 
##
##    plt.sca(ax[1])
##    plt.plot(ERparam,np.power(ER["hx_std"],2),'k'+style[i])
##    plt.plot(BAparam,np.power(BA["hx_std"],2),'r'+style[i])
##    plt.xlabel(r"$\langle k \rangle$")
##    plt.ylabel("Cross-entropy variance")
##
##plt.tight_layout()
##plt.show()



# Plot
ERparam =  np.arange(2,51,2) # for ER
BAparam = list(range(1,21+1)) + list(range(22,25+1)) # for BA
BAparam = [2*m - 2*m**2/N for m in BAparam]
style = ['-','x','o']
##alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5)]
alpha_list = [(1.5,2.0),(2.0,2.0),(2.5,2.0)]

fig, ax = plt.subplots(1,2,figsize=(8,3),sharey=False)
for i,alphas in enumerate(alpha_list):
    alpha = alphas[0]
    hub_alpha = alphas[1]
    ER = pd.read_csv("hx_ER_A%0.1f_HA%0.1F_q%0.1f.csv" % (alpha,hub_alpha,q))
    BA = pd.read_csv("hx_BA_A%0.1f_HA%0.1F_q%0.1f.csv" % (alpha,hub_alpha,q))

    plt.sca(ax[0])
    plt.plot(ERparam,ER["hx_avg"].values,'k'+style[i],label=r"$\alpha=%0.1f, \alpha_{hub}=%0.1f$" %(alpha,hub_alpha))
    plt.plot(BAparam,BA["hx_avg"].values,'r'+style[i])
    plt.xlabel(r"$\langle k \rangle$")
    plt.ylabel(r"$\langle h_\times \rangle$")
    plt.title("Black = ER, Red = BA")
    plt.legend() 

    plt.sca(ax[1])
    plt.plot(ERparam,np.power(ER["hx_std"].values,2),'k'+style[i])
    plt.plot(BAparam,np.power(BA["hx_std"].values,2),'r'+style[i])
    plt.xlabel(r"$\langle k \rangle$")
    plt.ylabel("Cross-entropy variance")

plt.tight_layout()
plt.show()

