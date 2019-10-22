import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

def make_SBM(sizes,p,return_blocks=False):
    """ My implementation of the stochastic block model.

        sizes (nx1 list of ints) -- the size of each block
        p (nxn list of floats) -- probability of connections between blocks
    """
    G = nx.Graph()
    p = np.array(p)
    
    # partions nodes into blocks: if sizes = [2,3,4] then
    # blocks will be [[0,1],[2,3,4],[5,6,7,8]]
    blocks = [ list(range(sum(sizes[:i]),sum(sizes[:(i+1)]))) for i in range(len(sizes)) ]

    for i in range(len(blocks)):
        block1 = blocks[i]
        for j in range(i,len(blocks)):
            block2 = blocks[j]
            for node1 in block1:
                for node2 in block2:
                    if random.random() < p[i,j]:
                        G.add_edge(node1,node2)

    if return_blocks:
        return G, blocks
    else:
        return G

def make_SBM_simple(N,mu):
    """ As in optimal modularity paper

        N (integer) -- total number of nodes
        mu (float in [0,1]) --  between community connection probability
    """
    G = nx.Graph()

    b1 = list(range(0,int(N/2)))
    b2 = list(range(int(N/2),N))

    for n1 in b1:
        for n2 in b2:
            if random.random() < mu:
                G.add_edge(n1,n2)

    for n1 in b1:
        for n2 in b1:
            if random.random() < (1-mu) and n1 != n2: # avoid self-loops
                G.add_edge(n1,n2)

    for n1 in b2:
        for n2 in b2:
            if random.random() < (1-mu) and n1 != n2: # avoid self-loops
                G.add_edge(n1,n2)


    return G
    






