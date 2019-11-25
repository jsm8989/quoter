import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter

def get_past_words_and_times(W1,T1,t2):
    prevW1 = []
    prevT1 = []
    for w1, t1 in zip(W1,T1):
        if t1 <= t2:
            prevW1.append(w1)
            prevT1.append(t1)
        else:
            break # no need to keep comparing times since the lists are ordered
    return prevW1,prevT1

if __name__ == "__main__":
    N = 2000
    M = 10000
    q = 0.9
    T = 1000
    mu_list = [0.05,0.5]
    trial = 0

    mu = mu_list[1] # high modularity first
    file = "N%i_mu%0.2f_M%i_q%0.1f_T%i_sim%i.txt" % (N,mu,M,q,T,trial)
    data = pd.read_csv(file, sep=" ")

    #user 0 first
    user = 1
    data = data.loc[data["user"]==user]
    times = data["time"].values
    words = data["word"].values
    
    all_times = np.unique(times)
    wcounts_list = []
    
    for t in all_times:
        w_past, _ = get_past_words_and_times(words,times,t)
        
        # plot rank vs frequency (seen so far)
        word_counts = [count for (word,count) in Counter(w_past).most_common()]
        wcounts_list.append(word_counts)

        # plot actual word distribution
##        word_counts = Counter(w_past)
##        wcounts_list.append(word_counts)
        

    plt.ion()
    wcounts_list = wcounts_list[::10] # only do some
    for i,word_counts in enumerate(wcounts_list):
        # plot rank vs frequency (seen so far)
        plt.plot(range(1,len(word_counts)+1), np.array(word_counts)/sum(word_counts))
        plt.xlabel("word rank")
        plt.ylabel("word frequency")

        # plot actual word distribution
##        w=word_counts.keys()
##        c=list(word_counts.values())
##        plt.plot(w, np.array(c)/sum(c), 'o')
##        plt.xlabel("word")
##        plt.ylabel("word frequency")

        plt.title("time=%0.4f mu=%0.2f user=%i" % (i/len(word_counts),mu,user) ) # normalized time
        plt.xlim(1,1000)
        plt.ylim(10**(-4),1)
        plt.xscale("log")
        plt.yscale("log")
        
        plt.draw()
        plt.pause(0.001)
        if i != len(wcounts_list)-1: # stop
            plt.clf()
