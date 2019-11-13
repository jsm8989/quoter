import numpy as np
import networkx as nx
from scipy import sparse
from scipy.linalg import eig
from itertools import product

# Code is not my own
#Source: https://github.com/zhiyzuo/python-modularity-maximization/blob/master/modularity_maximization/utils.py

def get_modularity(G, community_dict):
    '''
    Calculate the modularity. Edge weights are ignored.
    Undirected:
    .. math:: Q = \frac{1}{2m}\sum_{i,j} \(A_ij - \frac{k_i k_j}{2m}\) * \detal_(c_i, c_j)
    Directed:
    .. math:: Q = \frac{1}{m}\sum_{i,j} \(A_ij - \frac{k_i^{in} k_j^{out}}{m}\) * \detal_{c_i, c_j}
    Parameters
    ----------
    network : nx.Graph or nx.DiGraph
        The network of interest
    community_dict : dict
        A dictionary to store the membership of each node
        Key is node and value is community index
    Returns
    -------
    float
        The modularity of `network` given `community_dict`
    '''

    Q = 0
    A = nx.to_scipy_sparse_matrix(G).astype(float)

    if type(G) == nx.Graph:
        # for undirected graphs, in and out treated as the same thing
        out_degree = in_degree = dict(nx.degree(G))
        M = 2.*(G.number_of_edges())
        print("Calculating modularity for undirected graph")
    elif type(G) == nx.DiGraph:
        in_degree = dict(G.in_degree())
        out_degree = dict(G.out_degree())
        M = 1.*G.number_of_edges()
        print("Calculating modularity for directed graph")
    else:
        print('Invalid graph type')
        raise TypeError

    nodes = list(G)
    Q = np.sum([A[i,j] - in_degree[nodes[i]]*\
                         out_degree[nodes[j]]/M\
                 for i, j in product(range(len(nodes)),\
                                     range(len(nodes))) \
                if community_dict[nodes[i]] == community_dict[nodes[j]]])
    return Q / M
