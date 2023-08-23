import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def edge_clustering_coeff(
    G: nx.Graph, u: int, v: int, return_info: bool = False, draw: bool = False
):
    """
    Compute ECC between two nodes u and v, defined as the number of triangles containing both u and v divided by min(degrees(u,v))-1

    Args:
        G: NetworkX graph to be analysed. Must be directed
        u: node index of first node
        v: node index of second node
        return_info: if True return information about the algorithm
        draw: choose whether to visualise the graph

    Returns:
        triangles deg_u deg_v ECC (if return_info)
        ECC
    """
    u_nbrs = nx.neighbors(G, u)
    v_nbrs = nx.neighbors(G, v)
    uv_nbrs = set(u_nbrs) & set(v_nbrs)
    triangles = len(uv_nbrs)  # could be replaced by nx.triangles(G, [u,v]) or similar

    deg_u = nx.degree(G)[u]  # len(u_nbrs)
    deg_v = nx.degree(G)[v]  # len(v_nbrs)

    if min(deg_u - 1, deg_v - 1) == 0:  # undefined?
        ECC: float = 0
    else:
        ECC = triangles / min(deg_u - 1, deg_v - 1)

    if draw:
        pos = nx.spring_layout(G)
        labels = nx.draw_networkx_labels(G, pos)
        nx.draw(G, pos)
        plt.show()

    if return_info:
        return triangles, deg_u, deg_v, ECC
    else:
        return ECC


if __name__ == "__main__":
    # ECC example from paper
    G = nx.Graph()
    G.add_edges_from(
        [
            (1, 2),
            (1, 4),
            (1, 5),
            (1, 6),
            (2, 3),
            (3, 4),
            (3, 5),
            (3, 6),
            (4, 5),
            (4, 6),
            (5, 6),
        ]
    )
    print(edge_clustering_coeff(G, 1, 4, draw=True))

    # Test on real networks - TODO
    # for name in networks_dict:
    #     print(name)
    #     G = read_any(name)
    #     ECCs = []
    #     for i, e in enumerate(G.edges()):
    #         ECCs.append(edge_clustering_coeff(G, e[0], e[1]))
    #     print(len([x for x in ECCs if x == 2]) / len(G.edges()))
    #     print(np.mean([x for x in ECCs if x != 2]))
    # plt.hist([x for x in ECCs if x != 2])
    # plt.show()
