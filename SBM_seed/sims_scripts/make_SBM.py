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


def make_SBM_simple1(N,mu):
    """ As in optimal modularity paper
        N (integer) -- total number of nodes
        mu (float in [0,1]) --  between community connection probability

        Problem with this implementation:
        -there are m^2 between edges but only m*(m-1) within edges, hence
        as mu increases so does the density
    """
    G = nx.Graph()
    m = int(N/2)

    for n1 in range(0,m):
        for n2 in range(m,N):
            if random.random() < mu:
                G.add_edge(n1,n2)

    for n1 in range(0,m-1):
        for n2 in range(n1+1,m):
            if random.random() < (1-mu) and n1 != n2: # avoid self-loops
                G.add_edge(n1,n2)

    for n1 in range(m,N-1):
        for n2 in range(n1+1,N):
            if random.random() < (1-mu) and n1 != n2: # avoid self-loops
                G.add_edge(n1,n2)


    return G


def make_SBM_simple2(N,mu):
    """ As in optimal modularity paper

        N (integer) -- total number of nodes
        mu (float in [0,1]) --  between community connection probability

        Note about this implementation:
        -This factors in a correction probability so that the density
        is (in expectation) constant
    """
    G = nx.Graph()
    m = int(N/2)

    for n1 in range(0,m):
        for n2 in range(m,N):
            # correction factor of (m-1)/m because there are m^2 between edges
            # but only m*(m-1) within edges
            if random.random() < mu*(m-1)/m: 
                G.add_edge(n1,n2)
    
    for n1 in range(0,m-1):
        for n2 in range(n1+1,m):
            if random.random() < 1-mu:
                G.add_edge(n1,n2)

    for n1 in range(m,N-1):
        for n2 in range(n1+1,N):
            if random.random() < 1-mu:
                G.add_edge(n1,n2)

    return G

def make_SBM_simple3(N,mu):
    """ As in optimal modularity paper

        N (integer) -- total number of nodes
        mu (float in [0,1]) --  between community connection probability

        Note about this implementation:
        -This factors in a correction probability so that the density
        is EXACTLY constant (barring the fact that int(mu*(m-1)/m*len(eb))
        may be rounded up/down to cause minor fluctuations)
        -The edges are selected randomly, but the number of edges selected
        is no longer random.
    """
    G = nx.Graph()
    m = int(N/2)


    eb = []
    for n1 in range(0,m):
        for n2 in range(m,N):
            eb.append((n1,n2))

    ew = []
    for n1 in range(0,m-1):
        for n2 in range(n1+1,m):
            ew.append((n1,n2))

    for n1 in range(m,N-1):
        for n2 in range(n1+1,N):
            ew.append((n1,n2))

    e_tot = m*(m-1) # we fix e_tot = m*(m-1)
    ebi = np.random.choice(range(len(eb)),size=int(mu*e_tot),replace=False)
    ewi = np.random.choice(range(len(ew)),size=e_tot-int(mu*e_tot),replace=False)
    G.add_edges_from(np.array(eb)[ebi])
    G.add_edges_from(np.array(ew)[ewi])
    
    return G

def make_SBM_simple4(N,mu,M):
    """ As in optimal modularity paper

        N (integer) -- total number of nodes
        mu (float in [0,1]) --  between community connection probability

        Note about this implementation:
        -This factors in a correction probability so that the density
        is EXACTLY constant (barring the fact that int(mu*(m-1)/m*len(eb))
        may be rounded up/down to cause minor fluctuations)
        -The edges are selected randomly, but the number of edges selected
        is no longer random.
    """
    m = int(N/2)
    assert M <= m*(m-1), print("number of edges must be at most m*(m-1)")

    eb = []
    for n1 in range(0,m):
        for n2 in range(m,N):
            eb.append((n1,n2))

    ew = []
    for n1 in range(0,m-1):
        for n2 in range(n1+1,m):
            ew.append((n1,n2))

    for n1 in range(m,N-1):
        for n2 in range(n1+1,N):
            ew.append((n1,n2))

    ebi = np.random.choice(range(len(eb)),size=int(mu*M),replace=False)
    ewi = np.random.choice(range(len(ew)),size=M-int(mu*M),replace=False)

    G = nx.Graph()
    G.add_nodes_from(range(N))
    G.add_edges_from(np.array(eb)[ebi])
    G.add_edges_from(np.array(ew)[ewi])

    # deal with isolated vertices
    iso = list(nx.isolates(G))
    for i in iso:
        deg2plus = [j for j in G.nodes() if G.degree(j) >= 2]
        rmv = random.choice(deg2plus)
        rmv_nbr = random.choice(nx.neighbors(G,rmv))
        G.remove_edge(rmv,rmv_nbr)
        G.add_edge(i,rmv_nbr)
    
    return G

if __name__ == "__main__":
    mu_list = np.arange(0,0.51,0.1)
    dens = np.zeros(len(mu_list))
    trials = 50
    N = 200
    for i,mu in enumerate(mu_list):
        for _ in range(trials):
##            G = make_SBM_simple1(N,mu)
##            G = make_SBM_simple2(N,mu)
            G = make_SBM_simple4(N,mu,1000)
##            print(nx.number_of_edges(G),nx.number_of_nodes(G))
            dens[i] += nx.density(G)
        dens[i] /= trials
    print("\n".join(["mu=%0.2f dens=%0.8f" % (mu,d) for mu,d in zip(mu_list,dens)]))
##    G = make_SBM_simple4(100,0.03,750)
##    print(nx.number_of_edges(G))
##    nx.draw(G)
##    plt.show()






