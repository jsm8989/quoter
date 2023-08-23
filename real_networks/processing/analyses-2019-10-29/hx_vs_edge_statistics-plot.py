import numpy as np
import matplotlib.pyplot as plt
import random

# We probably will not use this!

stat_list = []
hx_list = []
###"network trial alter ego quoteProb hx distance triangles d_u d_v ECC\n"
with open("edge_stats-all_networks-links_only.txt", "r") as f:
    next(f)
    for line_iter in f:
        line = line_iter.rstrip().split()
        if float(line[-1]) <= 1:  # golden age has self-loops and some ECC > 1
            stat_list.append(float(line[-1]))  # ECC
            hx_list.append(
                float(line[-6])
            )  # indexing from end because 'network' names are 2 words... sigh
##        stat_list.append(float(line[-7])) # quote probability
##        hx_list.append(float(line[-6]))

sample = random.sample(range(len(hx_list)), 10000)  # take a sample
stat_list = np.array(stat_list)[sample]  # type:ignore
hx_list = np.array(hx_list)[sample]  # type:ignore
plt.plot(stat_list, hx_list, "ko")
plt.xlabel("ECC")
plt.ylabel("Cross-entropy")
plt.show()
