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

def get_wcounts_list(user,mu):
    N = 2000
    M = 10000
    q = 0.9
    T = 1000
    trial = 0
    
    file = "N%i_mu%0.2f_M%i_q%0.1f_T%i_sim%i.txt" % (N,mu,M,q,T,trial)
    data = pd.read_csv(file, sep=" ")

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

##        # plot actual word distribution
##        word_counts = Counter(w_past)
##        wcounts_list.append(word_counts)

    return wcounts_list[::10] # only do some

if __name__ == "__main__":
    mu_list = [0.05,0.5]
    users_list = [0,1]    
    data = []
    for mu in mu_list:
        for user in users_list:
            data.append(get_wcounts_list(user,mu))

    lenData = min([len(wcounts_l) for wcounts_l in data])

    plt.ion()
    for i in range(lenData):
##        if i==1:
##            input("press enter to continue...")
            
        # plot rank vs frequency (seen so far)
        plt.plot(range(1,len(data[0][i])+1), np.array(data[0][i])/sum(data[0][i]),label="mu=0.05,user=A")
        plt.plot(range(1,len(data[1][i])+1), np.array(data[1][i])/sum(data[1][i]),label="mu=0.05,user=B")
        plt.plot(range(1,len(data[2][i])+1), np.array(data[2][i])/sum(data[2][i]),label="mu=0.50,user=A")
        plt.plot(range(1,len(data[3][i])+1), np.array(data[3][i])/sum(data[3][i]),label="mu=0.50,user=B")

        plt.xlabel("word rank")
        plt.ylabel("word frequency")
        plt.legend()

        plt.title("time=%0.4f" % ((i+1)/lenData)) # normalized time
        plt.xlim(1,1000)
        plt.ylim(10**(-4),1)
        plt.xscale("log")
        plt.yscale("log")
        plt.draw()
        plt.pause(0.001)
        if i != lenData-1: # stop
            plt.clf()
