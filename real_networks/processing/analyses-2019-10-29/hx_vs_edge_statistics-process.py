import numpy as np
import pandas as pd
import os

q = 0.5
T = 1000
trials_list = list(range(300))
small_networks = ["CKM physicians", "Dolphins", "Email Spain", "Freeman's EIES",
              "Golden Age", "Kapferer tailor", "Les Miserables",
              "Hollywood music", "Sampson's monastery", "Terrorist"]

# Cross-entropy versus "edge" statistics (quoteProb, ECC, distance)
datadir = "../../data_separate_link-nonlink/data"

##with open("edge_stats-all_networks-links_only.txt","a+") as g:
##    g.write("network trial alter ego quoteProb hx distance triangles d_u d_v ECC\n")
    
for i,name in enumerate(small_networks):
    print(name)
    
    os.chdir("../") # <--this is a mess. Change this!!
    G = read_any(name)
    os.chdir("analyses-2019-10-29")
    
    for trial in trials_list:
        outdir = os.path.join(datadir, name)
        outfile = "%s_q%0.1f_T%i_sim%i.txt" % (name,q,T,trial)
        edata = pd.read_csv(os.path.join(outdir,outfile), sep = " ")
        with open(os.path.join(outdir,outfile),"r") as f:
            next(f)
            with open("edge_stats-all_networks-links_only.txt","a+") as g:
                for line in f:
                    line = line.rstrip().split()
                    if line[-1] == "2.0000": # ECC undefined
                        line[-1] = "1.0000" 
                    if line[4] == "1": # distance == 1 --> links only
                        g.write("%s %i " % (name,trial) + " ".join(line) + "\n")
