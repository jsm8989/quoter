import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import itertools

def make_SBM_general(sizes,p,return_blocks=False):
    """ My implementation of the stochastic block model.

        Args:
            sizes (nx1 list of ints) -- the size of each block
            p (nxn list of floats) -- probability of connections between blocks
            return_blocks (boolean) -- if True, returns partition of nodes into blocks
        Returns:
            a network (nx.Graph) which is a realization of the stochastic block model
    """
    G = nx.Graph()
    p = np.array(p)
    
    # partions nodes into blocks: if sizes = [2,3,4] then
    # blocks will be [[0,1],[2,3,4],[5,6,7,8]]
    blocks = [ list(range(sum(sizes[:i]),sum(sizes[:(i+1)]))) for i in range(len(sizes)) ]

    N = sum(sizes)
    
    A = np.zeros((N,N))
    for i in range(len(blocks)):
        block1 = blocks[i]
        for j in range(i,len(blocks)):
            block2 = blocks[j]

            if block1 == block2: # same blocks
                for k in range(len(block1)-1):
                    node1 = block1[k]
                    for l in range(k+1,len(block1)):
                        node2 = block1[l]
                        if random.random() < p[i,j]:
                            A[node1,node2] = A[node2,node1] =  1
                            G.add_edge(node1,node2)
                            
            else: # different blocks
                for node1 in block1: 
                    for node2 in block2:
                        if random.random() < p[i,j]:
                            A[node1,node2] = A[node2,node1] = 1
                            G.add_edge(node1,node2)

    if return_blocks:
        return G, blocks
    else:
        return G,A # change this after done debugging


def make_SBM_simple(N,mu,M):
    """ As in optimal modularity paper [1]. There are two blocks of equal size (N/2).
        The parameters M and mu determine the density and modularity of the network,
        respectively.
        
        Args:
            N (integer) -- number of nodes
            M (integer) -- number of edges
            mu (float in [0,1]) --  fraction of M edges to be placed between communities
        Returns:
            a network (nx.Graph) which is a realization of the stochastic block model as described in:

            [1] Nematzadeh, A., Ferrara, E., Flammini, A., & Ahn, Y. Y. (2014). Optimal
            network modularity for information diffusion. Physical review letters,
            113(8), 088701.
    """
    m = int(N/2)
    assert M <= m*(m-1), print("number of edges must be at most m*(m-1)")

    A = range(0,m)
    B = range(m,N)
    
    # edges between
    eb = list(itertools.product(A,B))
    
    # edges within
    ew = list(itertools.combinations(A,2)) + list(itertools.combinations(B,2))

    # add the edges    
    G = nx.Graph()
    G.add_nodes_from(range(N))
    G.add_edges_from(random.sample(eb, int(mu*M) ))
    G.add_edges_from(random.sample(ew, M-int(mu*M) ))

##    # Note: G may be disconnected.
##    # Here is a way to deal with a few isolated vertices, without changing
##    # the number of edges -- though the modularity will change slightly.
##    iso = list(nx.isolates(G))
##    for i in iso:
##        deg2plus = [j for j in G.nodes() if G.degree(j) >= 2]
##        rmv = random.choice(deg2plus)
##        rmv_nbr = random.choice(nx.neighbors(G,rmv))
##        G.remove_edge(rmv,rmv_nbr)
##        G.add_edge(i,rmv_nbr)
    
    return G


def make_SBM3(N,p,mu):
    """
        Another version of SBM. This is a special case of the general SBM,
        in which there are two blocks of equal size and only two unique
        connection probabilities: p (within block) and mu (between block).
    """
    m = int(N/2)
    A = range(0,m)
    B = range(m,N)
    
    # edges between
    eb = itertools.product(A,B)
    eb = [e for e in eb if random.random() < mu]

    # edges within
    ew = list(itertools.combinations(A,2)) + list(itertools.combinations(B,2))
    ew = [e for e in ew if random.random() < p]

    G = nx.Graph()
    G.add_nodes_from(range(N))
    G.add_edges_from(eb + ew)

    return G

def make_SBM3_oldDens(N,p,mu):
    """
        Another version of SBM. This is a special case of the general SBM,
        in which there are two blocks of equal size and only two unique
        connection probabilities: p (within block) and mu (between block).
    """
    m = int(N/2)
    A = range(0,m)
    B = range(m,N)
    
    # edges between
    eb = itertools.product(A,B)
    eb = [e for e in eb if random.random() < mu]

    # edges within
    p = 2*p-p**2
    ew = list(itertools.combinations(A,2)) + list(itertools.combinations(B,2))
    ew = [e for e in ew if random.random() < p]

    G = nx.Graph()
    G.add_nodes_from(range(N))
    G.add_edges_from(eb + ew)

    return G

if __name__ == "__main__":
    pass
##    N=100
##    M=750
##    for i,mu in enumerate([.03,.12,.3]):
##        G = make_SBM_simple(N,mu,M)
##        pos=nx.spring_layout(G,k=.25,iterations=40)
##        
##        plt.subplot(1,3,i+1)
##        nodes=nx.draw_networkx_nodes(G,pos,node_size=10,node_color="C1")
##        edges=nx.draw_networkx_edges(G,pos,width=0.5)
##        limits=plt.axis('off')
##        plt.title(r"$\mu = %0.2f$" % mu)
##        
##    plt.tight_layout()
##    plt.show()
    
##    mu_list = np.arange(0,0.51,0.1)
##    dens = np.zeros(len(mu_list))
##    trials = 5
##    N = 2000
##    for i,mu in enumerate(mu_list):
##        for _ in range(trials):
##            G = make_SBM_simple(N,mu,10000)
####            print(nx.number_of_edges(G),nx.number_of_nodes(G))
##            dens[i] += nx.number_connected_components(G)
##        dens[i] /= trials
##    print("\n".join(["mu=%0.2f dens=%0.8f" % (mu,d) for mu,d in zip(mu_list,dens)]))
##    G = make_SBM_simple4(100,0.03,750)
##    print(nx.number_of_edges(G))
##    nx.draw(G)
##    plt.show()

    fig,axes=plt.subplots(2,5,figsize=(10,4))
    for c in range(5):
##        plt.sca(axes[0,c])
##        G = make_SBM3(40,0.75,.1)
##        A = nx.adjacency_matrix(G)
##        A = A.todense()
##        plt.spy(A)
        
        plt.sca(axes[0,c])
        G,A = make_SBM_general([20,20],[[0.75,0.1],[0.1,0.75]])
        sp = nx.adjacency_matrix(G)
        sp = sp.todense()
        plt.spy(sp)

        plt.sca(axes[1,c])
        plt.spy(A)

    plt.tight_layout()
    plt.show()

    



