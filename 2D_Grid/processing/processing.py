import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

length = 20
width = 20
q = 0.9
T = 1000
trials_list = list(range(300))

### DISTANCE VS HX (in ring lattice)
##d_list = range(1,21)
##hx_avg = np.zeros(len(d_list))
##hx_var = np.zeros(len(d_list))
##p = 0
##hx_trial = [ [None] for _ in range(len(d_list)) ]
##for trial in trials_list:
##    efile = "../data_grid/edge/length%i_width%i_q%0.1f_T%i_sim%i.txt" % (length,width,q,T,trial)
##
##    try:
##        edata = pd.read_csv(efile, sep=" ")
##    except:
##        print("no data",p,trial)
##
##    else:
##        for i,d in enumerate(d_list):
##            hx_trial[i].extend(edata["hx"].loc[edata["distance"]==d].values)
##
##
##for i,d in enumerate(d_list):
##    print(len(hx_trial[i]))
##    hx_avg[i] = np.mean(hx_trial[i][1:])
##    hx_var[i] = np.var(hx_trial[i][1:])
##
##
##df = pd.DataFrame(data={"d":d_list,"hx_avg":hx_avg,"hx_var":hx_var})
##df = df.to_csv("2D_Grid_q%0.1f.csv" % q, index=False)


# PLOT distance vs hx
data = pd.read_csv("2D_Grid_q%0.1f.csv" % q)
plt.plot(data["d"],data["hx_avg"],'C0o-')
plt.errorbar(data["d"],data["hx_avg"],data["hx_var"])
plt.xlabel("Distance")
plt.ylabel("Average cross-entropy")
plt.show()



