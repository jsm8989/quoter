import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import itertools
import sys


def get_modularity(G, community_dict):
    """
    Calculate the modularity. Edge weights are ignored. From https://github.com/zhiyzuo/python-modularity-maximization/blob/master/modularity_maximization/utils.py

    :param G: NetworkX graph to be analysed
    :param community_dict: A dict to store the membership of each node. Key is node and value is community index
    :returns: (float) The modularity of `G` given `community_dict`
    """

    Q = 0
    A = nx.to_scipy_sparse_array(G).astype(float)

    if type(G) == nx.Graph:
        # for undirected graphs, in and out treated as the same thing
        out_degree = in_degree = dict(nx.degree(G))
        M = 2.0 * (G.number_of_edges())
        print("Calculating modularity for undirected graph")
    elif type(G) == nx.DiGraph:
        in_degree = dict(G.in_degree())
        out_degree = dict(G.out_degree())
        M = 1.0 * G.number_of_edges()
        print("Calculating modularity for directed graph")
    else:
        print("Invalid graph type")
        raise TypeError

    nodes = list(G)
    Q = np.sum(
        [
            A[i, j] - in_degree[nodes[i]] * out_degree[nodes[j]] / M
            for i, j in itertools.product(range(len(nodes)), range(len(nodes)))
            if community_dict[nodes[i]] == community_dict[nodes[j]]
        ]
    )
    return Q / M


def make_SBM_general(sizes, p, return_blocks=False):
    """My implementation of the stochastic block model.

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
    blocks = [
        list(range(sum(sizes[:i]), sum(sizes[: (i + 1)]))) for i in range(len(sizes))
    ]

    N = sum(sizes)

    A = np.zeros((N, N))
    for i in range(len(blocks)):
        block1 = blocks[i]
        for j in range(i, len(blocks)):
            block2 = blocks[j]

            if block1 == block2:  # same blocks
                for k in range(len(block1) - 1):
                    node1 = block1[k]
                    for l in range(k + 1, len(block1)):
                        node2 = block1[l]
                        if random.random() < p[i, j]:
                            A[node1, node2] = A[node2, node1] = 1
                            G.add_edge(node1, node2)

            else:  # different blocks
                for node1 in block1:
                    for node2 in block2:
                        if random.random() < p[i, j]:
                            A[node1, node2] = A[node2, node1] = 1
                            G.add_edge(node1, node2)

    print(nx.number_of_nodes(G))
    if return_blocks:
        return G, blocks
    else:
        return G, A  # change this after done debugging


def make_SBM_simple(N, mu, M):
    """As in optimal modularity paper [1]. There are two blocks of equal size (N/2).
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
    m = int(N / 2)
    assert M <= m * (m - 1), print("number of edges must be at most m*(m-1)")

    A = range(0, m)
    B = range(m, N)

    # edges between
    eb = list(itertools.product(A, B))

    # edges within
    ew = list(itertools.combinations(A, 2)) + list(itertools.combinations(B, 2))

    # add the edges
    G = nx.Graph()
    G.add_nodes_from(range(N))
    G.add_edges_from(random.sample(eb, int(mu * M)))
    G.add_edges_from(random.sample(ew, M - int(mu * M)))

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


def make_SBM3(N, p, mu):
    """
    Another version of SBM. This is a special case of the general SBM,
    in which there are two blocks of equal size and only two unique
    connection probabilities: p (within block) and mu (between block).
    """
    m = int(N / 2)
    A = range(0, m)
    B = range(m, N)

    # edges between
    eb = itertools.product(A, B)
    eb = [e for e in eb if random.random() < mu]

    # edges within
    ew = itertools.chain(itertools.combinations(A, 2), itertools.combinations(B, 2))
    ew = [e for e in ew if random.random() < p]

    G = nx.Graph()
    G.add_nodes_from(range(N))
    G.add_edges_from(eb + ew)

    return G


def make_growing_SBM(N, p, mu_seq, trial):
    m = int(N / 2)
    A = range(0, m)
    B = range(m, N)
    mu = mu_seq[0]

    # edges between
    eb = itertools.product(A, B)
    eb = random.sample(list(eb), int(mu * m**2))

    # edges within
    ew = itertools.chain(itertools.combinations(A, 2), itertools.combinations(B, 2))
    ew = random.sample(list(ew), int(p * m * (m - 1)))

    G = nx.Graph()
    G.add_nodes_from(range(N))
    G.add_edges_from([(0, 1), (0, m)])  # these edges will be in every graph
    G.add_edges_from(eb + ew)
    nx.write_edgelist(
        G,
        "output/edgelist/N%i_p%0.2f_mu%0.4f_trial%i.txt" % (N, p, mu_seq[0], trial),
        delimiter=" ",
        data=False,
    )

    for i in range(1, len(mu_seq)):
        edges_to_add = int((mu_seq[i] - mu_seq[i - 1]) * m**2)
        eb = itertools.product(A, B)
        eb_remaining = list(nx.non_edges(G))
        eb_remaining = (set(eb_remaining) | set([x[::-1] for x in eb_remaining])) & set(
            eb
        )
        e = random.sample(sorted(eb_remaining), edges_to_add)
        G.add_edges_from(e)
        nx.write_edgelist(
            G,
            "output/edgelist/N%i_p%0.2f_mu%0.4f_trial%i.txt" % (N, p, mu_seq[i], trial),
            delimiter=" ",
            data=False,
        )

    return G


if __name__ == "__main__":
    ##
    N = 100
    M = 750
    for i, mu in enumerate([0.03, 0.12, 0.3]):
        G = make_SBM_simple(N, mu, M)
        pos = nx.spring_layout(G, k=0.25, iterations=40)

        plt.subplot(1, 3, i + 1)
        nodes = nx.draw_networkx_nodes(G, pos, node_size=10, node_color="C1")
        edges = nx.draw_networkx_edges(G, pos, width=0.5)
        limits = plt.axis("off")
        plt.title(r"$\mu = %0.2f$" % mu)

    plt.tight_layout()
    plt.show()

    ##
    N = 100
    m = N // 2
    p = 0.6
    mu = 0.15
    G = make_SBM3(N, p, mu)
    A = range(0, m)
    B = range(m, N)
    comm_dict = {x: 0 for x in A}
    comm_dict.update({x: 1 for x in B})
    Q = get_modularity(G, comm_dict)
    print(f"modularity of SBM3 model: {Q}")
    L = p * m * (m - 1) + mu * m**2
    k = m * (p * (m - 1) + mu * m)
    # print(2 * (p * m * (m - 1) / (2 * L) - (k / (2 * L)) ** 2))

    ##
    N = 1000
    m = N // 2
    A = range(0, m)
    B = range(m, N)
    p = 0.4

    # Mathematica code to generate this sequence:
    # Reverse[Table[\[Mu] /. NSolve[q[0.4, \[Mu], 1000] == K, \[Mu]], {K,
    # 0.00, 0.40, 0.025}]]
    mu_seq = [
        0.0444,
        0.0570857,
        0.0705176,
        0.0847636,
        0.0999,
        0.116013,
        0.1332,
        0.151572,
        0.171257,
        0.1924,
        0.215169,
        0.23976,
        0.2664,
        0.295357,
        0.326945,
        0.361543,
        0.3996,
    ]
    for trial in range(2):  # arbitrary number of simulations
        G = make_growing_SBM(N, p, mu_seq, trial)

        for i in range(len(mu_seq)):
            print("i: ", i)
            # edges between
            eb = itertools.product(A, B)
            # edges within
            ew = itertools.chain(
                itertools.combinations(A, 2), itertools.combinations(B, 2)
            )

            G = nx.read_edgelist(
                "output/edgelist/N%i_p%0.2f_mu%0.4f_trial%i.txt"
                % (N, p, mu_seq[i], trial),
                nodetype=int,
            )

            eb_pres = set(eb) | set([x[::-1] for x in eb])
            eb_pres = eb_pres & (
                set(G.edges()) | set([x[::-1] for x in list(G.edges())])
            )
            print("between density: ", len(eb_pres) / m**2)
            print("within A density: ", nx.density(G.subgraph(A)))
            print("within B density: ", nx.density(G.subgraph(B)))
            comm_dict = {x: 0 for x in A}
            comm_dict.update({x: 1 for x in B})
            Q = get_modularity(G, comm_dict)
            print("modularity:", Q, "\n")
