import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from quoter.real_networks.read_networks import (
    read_any,
    networks_dict,
    small_networks,
)
from quoter.quoter_model import edge_clustering_coeff

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

    # Testing on real networks
    for name in networks_dict:
        print(f"\n{name}")
        G = read_any(name)
        ECCs = []
        for i, e in enumerate(G.edges()):
            ECCs.append(edge_clustering_coeff(G, e[0], e[1]))
        print(
            f"Number of ECC=2 divided by number of edges in graph: {len([x for x in ECCs if x == 2]) / len(G.edges())}"
        )
        print(
            f"Mean of ECC over entire graph, ignoring anomalies: {np.mean([x for x in ECCs if x != 2])}"
        )
    plt.hist([x for x in ECCs if x != 2])
    plt.title("Summary of Edge Clustering Coefficient analysis")
    plt.xlabel("ECC_value")
    plt.ylabel("Counts for all edge pairings in network ensemble")
    plt.show()
