import networkx as nx
import numpy as np
import pandas as pd
import re
import sys
from networkx.algorithms import bipartite

def get_giant_component(G):
    # extract only the giant component
    cc = sorted(nx.connected_components(G), key=len, reverse=True)
    G.remove_nodes_from(set(G.nodes()) - set(cc[0]))
    return G

def read_adolescent():
    file = "../NETWORKS/adolescent_health/out.moreno_health_health"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]   # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)
    
    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_arxiv_CondMat():
    file = "../NETWORKS/Arxiv_ca-CondMat/Newman-Cond_mat_95-99-binary.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return get_giant_component(G)


def read_arxiv_GrQc():
    file = "../NETWORKS/Arxiv_ca-GrQc/CA-GrQc.txt"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(4)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return get_giant_component(G)


def read_ckm(network_num=3):
    assert network_num in [1,2,3], "network_num (int) must be 1, 2, or 3"
    file = "../NETWORKS/CKM_physicians/ckm.txt"
    with open(file,"r") as f:
        skip = [next(f) for _ in range(9)]
        A123 = f.read().strip().split()
        N = 246
        A1 = A123[:N**2]
        A2 = A123[N**2:2*(N**2)]
        A3 = A123[2*(N**2):3*(N**2)]
        A1 = np.reshape(A1, (N,N)).astype(int)
        A2 = np.reshape(A2, (N,N)).astype(int)
        A3 = np.reshape(A3, (N,N)).astype(int)
        if network_num == 1:
            G = nx.from_numpy_matrix(A1)
        elif network_num == 2:
            G = nx.from_numpy_matrix(A2)
        else: #network_num == 3
            G = nx.from_numpy_matrix(A3)

    return get_giant_component(G)

    
def read_dolphins():
    file = "../NETWORKS/dolphins/out.dolphins"
    elist = []
    with open(file, "r") as f:
        next(f, "")   # skip a line
        for line in f:
            e = set(int(x) for x in line.rstrip().split("\t"))
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_email():
    # Spain email network
    file = "../NETWORKS/email_network/email.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_enron():
    """ 10588 nodes
        65901 edges (directed) and   54527 (undirected)
        We use the undirected graph.
    """
    
    file = "../NETWORKS/enron/enron-edgelist.txt"

    G = nx.read_edgelist(file, delimiter=" ", create_using=nx.Graph(),
                         data=False, encoding='utf-8')
    G = nx.convert_node_labels_to_integers(G, first_label=0)
    
    return get_giant_component(G)


def read_Eu_Core():
    file = "../NETWORKS/email-Eu-core/email-Eu-core.txt"
    G = nx.read_edgelist(file,nodetype=int)

    return get_giant_component(G)


def read_Freemans(network_num=1):
    assert network_num in [1,2], "network_num (int) must be 1 or 2"
    file = "../NETWORKS/Freemans_EIES/Freemans_EIES-time%i_n48.txt" % network_num
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = set(int(x) for x in line.rstrip().split(" ")[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_golden():
    file = "../NETWORKS/GoldenAge/HollywoodGoldenAge_matrix_s0.txt"
    A=np.loadtxt(file)
    G = nx.from_numpy_matrix(A)
    G.remove_edges_from(G.selfloop_edges())
    return G


def read_hypertext():
    """ This network is a DYNAMIC network (edges are timestamped).
        We are treating it as static (a link is present if a
        link existed at any time).
    """
    file = "../NETWORKS/sociopatterns-hypertext/out.sociopatterns-hypertext"
    elist = []
    with open(file,"r") as f:
        skip = [next(f) for _ in range(2)]
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_kapf():
    file = "../NETWORKS/kapfdata/kapfts1.dat"
    adjmat = np.loadtxt(file)
    G = nx.from_numpy_matrix(adjmat)
    return G


def read_lesmis():
    # The downloaded file is not in proper GML format for Networkx
    # Run this once to reformat.
##    file = "../lesmis/lesmis.gml"
##    with open(file, "r") as f:
##        new_file_string = f.read().replace("\s+\[", "[")
##
##    with open("../lesmis/lesmis_reformatted.gml","w") as f:
##        f.write(new_file_string)

    file = "../NETWORKS/lesmis/lesmis_reformatted.gml"
    G = nx.read_gml(file)
    G = nx.convert_node_labels_to_integers(G, first_label=0)
    return G


def read_Marvel():
    file = "../NETWORKS/Marvel/Marvel.txt"
    elist = []
    with open(file,"r") as f:
        skip = [next(f) for _ in range(19430)]
        for line in f:
            linelist = line.rstrip().split()
            lineedges = [ (linelist[0], e2) for e2 in linelist[1:] ]
            elist.extend(lineedges)
    G = nx.Graph()
    G.add_edges_from(elist)
    G = nx.convert_node_labels_to_integers(G, first_label=0)

    return get_giant_component(G)


def read_movies():
    # Was unable to figure out how to use nx.read_pajek for this file,
    # ended up looking at the data and doing it manually. Edgelist starts
    # at line 107 and ends at line 298.
    file = "../NETWORKS/movies/Movies.paj"
##    G = nx.read_pajek(file)
    elist = []
    with open(file,"r") as f:
        linecount = 1
        while linecount <= 298:
            line = f.readline()
            if linecount >= 107:
                line = re.sub(r'\s+', ' ', line).strip()
                e = set(int(x) for x in line.split(" ")[:2])
                elist.append(e)
                
            linecount += 1
            
    B = nx.Graph()
    B.add_edges_from(elist)
    B.add_node(78) # node 78 doesn't appear in any edges

    # Project onto composers. Two composers are linked if they worked with the
    # same producer.
    G = bipartite.projected_graph(B, list(range(63,103)))
    
    return get_giant_component(G)


def read_netscience():
    # The downloaded file is not in proper GML format for Networkx
    # Run this once to reformat.
##    file = "../NETWORKS/netscience/netscience.gml"
##    with open(file, "r") as f:
##        new_file_string = f.read().replace("\s+\[", "[")
##
##    with open("../netscience/netscience_reformatted.gml","w") as f:
##        f.write(new_file_string)

    file = "../NETWORKS/netscience/netscience_reformatted.gml"
    G = nx.read_gml(file)
    G = nx.convert_node_labels_to_integers(G, first_label=0)

    return get_giant_component(G)


def read_NFL():
    file = "../NETWORKS/NFL2009_network/NFL2009_EdgeList.txt"
    elist = []
    with open(file, "r") as f:
        next(f, "")   # skip a line
        for line in f:
            e = set(int(x) for x in line.rstrip().split("\t")[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    
    return G


def read_org():
    file = "../NETWORKS/organizational/Cross_Parker-Manufacturing_info.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_pgp():
    file = "../NETWORKS/pgp_trust/pgp_2004.net"
    elist = []
    with open(file,"r") as f:
        linecount = 1
        while linecount <= 35023:
            line = f.readline()
            if linecount >= 10684:
                e = tuple(int(x) for x in line.rstrip().split(" ")[:2])
                elist.append(e)
                
            linecount += 1
            
    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_Sampson():
    # Was unable to figure out how to use nx.read_pajek for this file,
    # ended up looking at the data and doing it manually. Edgelist starts
    # at line 107 and ends at line 298.
    file = "../NETWORKS/Sampson/Sampson.paj"
##    G = nx.read_pajek(file)
    elist = []
    with open(file,"r") as f:
        linecount = 1
        while linecount <= 350:
            line = f.readline()
            if linecount >= 29:
                line = re.sub(r'\s+', ' ', line).strip()
                relation = int(line.split(" ")[2]) # only keep positive links
                e = set(int(x) for x in line.split(" ")[:2] if relation > -1)
                
                if len(e) == 2:
                    elist.append(e)
                
            linecount += 1
            
    G = nx.Graph() 
    G.add_edges_from(elist)
    return G


def read_terrorist():
    file = "../NETWORKS/terrorists/terrorist.pairs"
    G = nx.read_edgelist(file,nodetype=int)
    return G


def read_UC_Irvine():
    file = "../NETWORKS/UC_Irvine2004/OClinks_w.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return get_giant_component(G)


networks_dict = {"Adolescent health": read_adolescent,
                "Arxiv CondMat": read_arxiv_CondMat,
##                "Arxiv GrQc": read_arxiv_GrQc,
                "CKM physicians": read_ckm,
                "Dolphins": read_dolphins,
                "Email Spain": read_email,
                "Email Enron": read_enron,
##                "Email Eu Core": read_Eu_Core,
                "Freeman's EIES": read_Freemans,
                "Golden Age": read_golden,
##                "Hypertext": read_hypertext,
                "Kapferer tailor": read_kapf,
                "Les Miserables": read_lesmis,
##                "Marvel": read_Marvel, 
                "Hollywood music": read_movies,
##                "Network science": read_netscience,
##                "NFL": read_NFL,
##                "Intra-organizational": read_org,
##                "Web of Trust": read_pgp,
                "Sampson's monastery": read_Sampson,
                "Terrorist": read_terrorist}
##                "UC Irvine": read_UC_Irvine}


def read_any(name):        
    assert name in networks_dict, "Name must be one of the following networks:\n" + "\n".join(networks_dict.keys())
    return networks_dict[name]()

    
if __name__ == "__main__":
    titles = []
    num_nodes = []
    num_edges = []
    density = []
    avg_k = []
    max_k = []
    min_k = []
##    ASPL = []
##    diam = []
    assortativity = []
    transitivity = []
    avg_clustering = []
    
    for name in networks_dict:
        print(name)
        G = read_any(name)
        n = nx.number_of_nodes(G)
        e = nx.number_of_edges(G)
        titles.append(name)
        num_nodes.append(n)
        num_edges.append(e)
        density.append(round(e/(n*(n-1)/2),4))
        avg_k.append(round(2*nx.number_of_edges(G)/nx.number_of_nodes(G),1))
        max_k.append(max(list(nx.degree(G,G.nodes()).values())))
        min_k.append(min(list(nx.degree(G,G.nodes()).values())))
##        ASPL.append(nx.average_shortest_path_length(G))
##        diam.append(nx.diameter(G))
        assortativity.append(round(nx.degree_assortativity_coefficient(G),2))
        transitivity.append(round(nx.transitivity(G),2))
        avg_clustering.append(round(nx.average_clustering(G),2))

    data = [[titles[i],num_nodes[i],num_edges[i],density[i],avg_k[i],max_k[i],
             min_k[i],assortativity[i],
             transitivity[i],avg_clustering[i]] for i in range(len(num_nodes))]

    df = pd.DataFrame(data, columns=["network","num_nodes","num_edges","density","avg_k","max_k","min_k",
                                     "assortativity","transitivity","average_clustering"]) 
    df.set_index("network")
    df = df.sort_values("density")
    with open("network_statistics.csv","w") as f:
        f.write(df.to_csv(index=False))

    #PRINT MY TEX TABLE!
    with open("network_statistics.csv","r") as f:
        dfstring = f.read()
        dfstring = dfstring.replace(",", " & ")
        dfstring = dfstring.replace("\n", r"\\" + "\n")
        print(dfstring)


##    # Construct edgelist with quoteProbs
##    for name in networks_dict:
##        G0  = read_any(name)
##        G = G0.to_directed()
##        for e in G.edges(): #e[0] = alter e[1] = ego
##            G[e[0]][e[1]]["quoteProb"] = 1/len(G.predecessors(e[1]))
##
##        with open("edgelists_to_fileshare/" + name + ".txt", "w") as f:
##            f.write("alter ego quoteProb\n")
##            for e in G.edges():
##                f.write("%i %i %0.8f\n" % (e[0],e[1],G[e[0]][e[1]]["quoteProb"]))
##        
##        print(name)
            
        



