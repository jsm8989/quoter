import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("../processing/hx_real-networks.csv")
gdata = pd.read_csv("../processing/network_statistics.csv")
dens = gdata["density"].values[[1,2,4,8,9,10,11,12,13,14,15,17]]
C = gdata["transitivity"].values[[1,2,4,8,9,10,11,12,13,14,15,17]]

folders = ['Arxiv_ca-GrQc','adolescent_health','email_network','terrorists',
           'dolphins','lesmis','kapfdata','movies','Sampson','GoldenAge',
           'NFL2009_network','Freemans_EIES']

# density plot
for i,folder in enumerate(folders):
    x = dens[i]
    y = data["hx_avg"].values[i]
    yerr = data["hx_sd"].values[i]
##    plt.errorbar(x, y, yerr=yerr, fmt='ko', elinewidth=3)
    plt.plot(x,y,'ko')
    
    if folder == 'Freemans_EIES':
        plt.text(x-0.1, y-0.01, folder, fontsize=8.5)
    elif folder == 'Arxiv_ce-GrQc':
        plt.text(x+0.02, y, "Arxiv", fontsize=8.5)
    elif folder == 'lesmis':
        plt.text(x+0.02, y-.005, folder, fontsize=8.5)
    else:
        plt.text(x+.02, y, folder, fontsize=8.5)

plt.xlabel("Density")
plt.ylabel(r"Mean cross-entropy")
plt.show()

# transitivity plot
for i,folder in enumerate(folders):
    x = C[i]
    y = data["hx_avg"].values[i]
    yerr = data["hx_sd"].values[i]
##    plt.errorbar(x, y, yerr=yerr, fmt='ko', elinewidth=3)
    plt.plot(x,y,'ko')
plt.xlabel("Transitivity")
plt.ylabel(r"Mean cross-entropy")
plt.show()



