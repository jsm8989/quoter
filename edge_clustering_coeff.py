import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def edge_clustering_coeff(G,u,v,return_info=False):
    u_nbrs = nx.neighbors(G,u)
    v_nbrs = nx.neighbors(G,v)
    uv_nbrs = set(u_nbrs) & set(v_nbrs)
    triangles = len(uv_nbrs)

    deg_u = len(u_nbrs)
    deg_v = len(v_nbrs)
    
    if min(deg_u-1,deg_v-1) == 0: # undefined?
        ECC = 0
    else:
        ECC = triangles/min(deg_u-1,deg_v-1)
    
    if return_info:
        return triangles, deg_u, deg_v, ECC
    else:
        return ECC


if __name__ == "__main__":
    # ECC example from paper
    G = nx.Graph()
    G.add_edges_from([(1,2),(1,4),(1,5),(1,6),(2,3),(3,4),(3,5),(3,6),
                      (4,5),(4,6),(5,6)])
    print(edge_clustering_coeff(G,1,4))
    pos = nx.spring_layout(G)
    labels=nx.draw_networkx_labels(G,pos)
    nx.draw(G,pos)
    plt.show()

    # Test on real networks
##    for name in networks_dict:
##        print(name)
##        G = read_any(name)
##        ECCs = []
##        for i,e in enumerate(G.edges()):
##            ECCs.append(edge_clustering_coeff(G,e[0],e[1]))
##    ##    print(len([x for x in ECCs if x == 2])/len(G.edges()))
##        print(np.mean([x for x in ECCs if x != 2]))
##    ##plt.hist([x for x in ECCs if x !=2])
##    ##plt.show()
