import numpy as np
import pandas as pd
import os

# Parameters for simulation, used in loading in files
N = 1000
q = 0.5
T = 1000
trials_list = list(range(200))
##alpha_list = [(1.5,1.5),(1.5,2.5),(2.5,1.5),(2.5,2.5)] # data_%s/
alpha_list = [(2.0,1.5),(2.0,2.0),(2.0,2.5),(1.5,2.0),(2.5,2.0)] # data_%s-Dec2

# CHANGE THIS depending on which data you want to process
graph = "BA" # change this to ER/BA

# Parameters specific to ER & BA networks
if graph == "ER":
    param_list = ERparam = np.arange(2,51,2) # k-values
else: # graph == "BA"
    param_list = list(range(1,21+1)) + list(range(23,26+1)) # m-values for BA


# Process the data: edge data only
data = np.zeros((2,len(param_list)))
for alphas in alpha_list:
    alpha = alphas[0]
    hub_alpha = alphas[1]
    for i,x in enumerate(param_list):
        hx_list = []  # store cross-entropies
        
        for trial in trials_list:

            # file naming format depends on whether ER or BA
            if graph == "ER":
                param_sym = "k"
            else:
                param_sym = "m"
            
            efile = "../data_%s-Dec2/edge/N%i_%s%i_A%0.1f_HA%0.1f_q%0.1f_T%i_sim%i.txt" % (graph,N,param_sym,x,alpha,hub_alpha,q,T,trial)
            if os.path.isfile(efile):
                edata = pd.read_csv(efile, sep = " ")     
                hx_list.extend(edata["hx"].values)

            else:
                print("no data", alpha, x)
                

        print(i/len(param_list)) # progress check, percentage done
        
        data[0,i] = np.mean(hx_list)
        data[1,i] = np.std(hx_list)

    # save csv file with processed data
    df = pd.DataFrame({"%s" % param_sym:param_list, "hx_avg":data[0,:], "hx_std":data[1,:]})
    df.to_csv("hx_%s_A%0.1f_HA%0.1f.csv" % (graph,alpha,hub_alpha), index=False)
    

### Process tdata: including node & graph data
##data = np.zeros((7,len(param_list)))
##for alphas in alpha_list:
##    alpha = alphas[0]
##    hub_alpha = alphas[1]
##    for i,x in enumerate(param_list):
##        hx_list = []  # store cross-entropies
##        h_list = [] # store node entropies
##
##        # compute average graph statistics
##        deg = 0 
##        dens = 0
##        clus = 0
##        assort = 0
##        count = 0
##        
##        for trial in trials_list:
##
##            # file naming format depends on whether ER or BA
##            if graph == "ER":
##                param_sym = "k"
##            else:
##                param_sym = "m"
##            
##            efile = "../data_%s-Dec2/edge/N%i_%s%i_A%0.1f_HA%0.1f_q%0.1f_T%i_sim%i.txt" % (graph,N,param_sym,x,alpha,hub_alpha,q,T,trial)
##            nfile = "../data_%s-Dec2/node/N%i_%s%i_A%0.1f_HA%0.1f_q%0.1f_T%i_sim%i.txt" % (graph,N,param_sym,x,alpha,hub_alpha,q,T,trial)
##            gfile = "../data_%s-Dec2/graph/N%i_%s%i_A%0.1f_HA%0.1f_q%0.1f_T%i_sim%i.txt" % (graph,N,param_sym,x,alpha,hub_alpha,q,T,trial)
##
##            try:
##                edata = pd.read_csv(efile, sep = " ")
##                ndata = pd.read_csv(nfile, sep = " ")
##                gdata = pd.read_csv(gfile, sep = " ")
##                
##            except:
##                print("no data", alpha, x)
##                
##            else:
##                hx_list.extend(edata["hx"].values)
##                h_list.extend(ndata["h"].values)
##                
##                deg += gdata["average_degree"].values[0]
##                dens += gdata["density"].values[0]
##                clus += gdata["transitivity"].values[0]
##                count += 1
##
##        print(i/len(param_list)) # progress check, percentage done
##        
##        data[0,i] = np.mean(hx_list)
##        data[1,i] = np.std(hx_list)
##        data[2,i] = np.mean(h_list)
##        data[3,i] = np.std(h_list)
##        data[4,i] = dens/count
##        data[5,i] = clus/count
##        data[6,i] = deg/count
##
##    # save csv file with processed data
##    df = pd.DataFrame({"%s" % param_sym:param_list, "hx_avg":data[0,:], "hx_std":data[1,:],
##                        "h_avg":data[2,:], "h_std":data[3,:],
##                       "density":data[4,:],"transitivity":data[5,:],
##                       "average_degree":data[6,:]})
##    df.to_csv("hx_%s_A%0.1f_HA%0.1f.csv" % (graph,alpha,hub_alpha), index=False)



