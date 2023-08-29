import networkx as nx
import numpy as np
import pandas as pd
import re
from networkx.algorithms import bipartite
import community
import matplotlib.pyplot as plt
from itertools import product


def get_giant_component(G):
    """
    Returns the giant component of a graph. Giant components are nodes that are connected to each other in the graph.

    @param G - NetworkX graph to be analysed. It must be directed.

    @return G with only the giant component removed. This is a copy of G
    """
    cc = sorted(nx.connected_components(G), key=len, reverse=True)
    G.remove_nodes_from(set(G.nodes()) - set(cc[0]))
    return G


def get_modularity(G, community_dict):
    """
    Calculate the modularity. Edge weights are ignored. From https://github.com/zhiyzuo/python-modularity-maximization/blob/master/modularity_maximization/utils.py

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
    """

    Q = 0
    A = nx.to_scipy_sparse_matrix(G).astype(float)

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
            for i, j in product(range(len(nodes)), range(len(nodes)))
            if community_dict[nodes[i]] == community_dict[nodes[j]]
        ]
    )
    return Q / M


networks_folder = "/home/jimjam/Documents/Adelaide/quoter/real_networks/NETWORKS"


def read_adolescent():
    """
    Read adolescent_health file and return networkx graph. This file is used to determine the health of the network and should contain a list of tuples ( node_id node_name ) where node_id is the node id of the node that is connected to the node with the same node_name.


    Returns:
        NetworkX graph
    """
    file = networks_folder + "/adolescent_health/out.moreno_health_health"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_arxiv_CondMat():
    """
    Read Arxiv Cond Mat file and return Giant component.


    Returns:
        Graph with components as node ids
    """
    file = networks_folder + "/Arxiv_ca-CondMat/Newman-Cond_mat_95-99-binary.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return get_giant_component(G)


def read_arxiv_GrQc():
    """
    Read GrQc file and return giant component. It is assumed that the file is in arxiv format


    Returns:
        networkx graph with components as node ids
    """
    file = networks_folder + "/Arxiv_ca-GrQc/CA-GrQc.txt"
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
    """
    Read CKM physicians from file. This file is used to generate network connectivity matrices and other data structures that can be used for testing.

    :param network_num: ( int ) number of network 1 2 or 3
    :returns: ( NetworkX ) network connectivity matrices and other data
    """
    assert network_num in [1, 2, 3], "network_num (int) must be 1, 2, or 3"
    file = networks_folder + "/CKM_physicians/ckm.txt"
    with open(file, "r") as f:
        skip = [next(f) for _ in range(9)]
        A123 = f.read().strip().split()
        N = 246
        A1 = A123[: N**2]
        A2 = A123[N**2 : 2 * (N**2)]
        A3 = A123[2 * (N**2) : 3 * (N**2)]
        A1 = np.reshape(A1, (N, N)).astype(int)
        A2 = np.reshape(A2, (N, N)).astype(int)
        A3 = np.reshape(A3, (N, N)).astype(int)
        if network_num == 1:
            G = nx.from_numpy_array(A1)
        elif network_num == 2:
            G = nx.from_numpy_array(A2)
        else:  # network_num == 3
            G = nx.from_numpy_array(A3)

    return get_giant_component(G)


def read_dolphins():
    file = networks_folder + "/dolphins/out.dolphins"
    elist = []
    with open(file, "r") as f:
        next(f, "")  # skip a line
        for line in f:
            e = set(int(x) for x in line.rstrip().split("\t"))
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_email():
    # Spain email network
    file = networks_folder + "/email_network/email.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_enron():
    """10588 nodes
    65901 edges (directed) and   54527 (undirected)
    We use the undirected graph.
    """

    file = networks_folder + "/enron/enron-edgelist.txt"

    G = nx.read_edgelist(
        file, delimiter=" ", create_using=nx.Graph(), data=False, encoding="utf-8"
    )
    G = nx.convert_node_labels_to_integers(G, first_label=0)

    return get_giant_component(G)


def read_Eu_Core():
    file = networks_folder + "/email-Eu-core/email-Eu-core.txt"
    G = nx.read_edgelist(file, nodetype=int)

    return get_giant_component(G)


def read_Freemans(network_num=1):
    assert network_num in [1, 2], "network_num (int) must be 1 or 2"
    file = networks_folder + "/Freemans_EIES/Freemans_EIES-time%i_n48.txt" % network_num
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = set(int(x) for x in line.rstrip().split(" ")[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_golden():
    file = networks_folder + "/GoldenAge/HollywoodGoldenAge_matrix_s0.txt"
    A = np.loadtxt(file)
    G = nx.from_numpy_array(A)
    G.remove_edges_from(nx.selfloop_edges(G))
    return G


def read_hypertext():
    """This network is a DYNAMIC network (edges are timestamped).
    We are treating it as static (a link is present if a
    link existed at any time).
    """
    file = networks_folder + "/sociopatterns-hypertext/out.sociopatterns-hypertext"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_kapf():
    file = networks_folder + "/kapfdata/kapfts1.dat"
    adjmat = np.loadtxt(file)
    G = nx.from_numpy_array(adjmat)
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

    file = networks_folder + "/lesmis/lesmis_reformatted.gml"
    G = nx.read_gml(file)
    G = nx.convert_node_labels_to_integers(G, first_label=0)
    return G


def read_Marvel():
    file = networks_folder + "/Marvel/Marvel.txt"
    elist = []
    with open(file, "r") as f:
        # skip = [next(f) for _ in range(19430)]
        for line in f:
            linelist = line.rstrip().split()
            lineedges = [(linelist[0], e2) for e2 in linelist[1:]]
            elist.extend(lineedges)
    G = nx.Graph()
    G.add_edges_from(elist)
    G = nx.convert_node_labels_to_integers(G, first_label=0)

    return get_giant_component(G)


def read_movies():
    # Was unable to figure out how to use nx.read_pajek for this file,
    # ended up looking at the data and doing it manually. Edgelist starts
    # at line 107 and ends at line 298.
    file = networks_folder + "/movies/Movies.paj"
    ##    G = nx.read_pajek(file)
    elist = []
    with open(file, "r") as f:
        linecount = 1
        while linecount <= 298:
            line = f.readline()
            if linecount >= 107:
                line = re.sub(r"\s+", " ", line).strip()
                e = set(int(x) for x in line.split(" ")[:2])
                elist.append(e)

            linecount += 1

    B = nx.Graph()
    B.add_edges_from(elist)
    B.add_node(78)  # node 78 doesn't appear in any edges

    # Project onto composers. Two composers are linked if they worked with the
    # same producer.
    G = bipartite.projected_graph(B, list(range(63, 103)))

    return get_giant_component(G)


def read_netscience():
    # The downloaded file is not in proper GML format for Networkx
    # Run this once to reformat.
    ##    file = networks_folder + "/netscience/netscience.gml"
    ##    with open(file, "r") as f:
    ##        new_file_string = f.read().replace("\s+\[", "[")
    ##
    ##    with open("../netscience/netscience_reformatted.gml","w") as f:
    ##        f.write(new_file_string)

    file = networks_folder + "/netscience/netscience_reformatted.gml"
    G = nx.read_gml(file)
    G = nx.convert_node_labels_to_integers(G, first_label=0)

    return get_giant_component(G)


def read_NFL():
    file = networks_folder + "/NFL2009_network/NFL2009_EdgeList.txt"
    elist = []
    with open(file, "r") as f:
        next(f, "")  # skip a line
        for line in f:
            e = set(int(x) for x in line.rstrip().split("\t")[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return G


def read_org():
    file = networks_folder + "/organizational/Cross_Parker-Manufacturing_info.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    return G


def read_pgp():
    file = networks_folder + "/pgp_trust/pgp_2004.net"
    elist = []
    with open(file, "r") as f:
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


### There is a better version of Sampson's monastery network
##def read_Sampson_Pajek():
##    # Was unable to figure out how to use nx.read_pajek for this file,
##    # ended up looking at the data and doing it manually. Edgelist starts
##    # at line 107 and ends at line 298.
##    file = networks_folder + "/Sampson/Sampson.paj"
####    G = nx.read_pajek(file)
##    elist = []
##    with open(file,"r") as f:
##        linecount = 1
##        while linecount <= 350:
##            line = f.readline()
##            if linecount >= 29:
##                line = re.sub(r'\s+', ' ', line).strip()
##                relation = int(line.split(" ")[2]) # only keep positive links
##                e = set(int(x) for x in line.split(" ")[:2] if relation > -1)
##
##                if len(e) == 2:
##                    elist.append(e)
##
##            linecount += 1
##
##    G = nx.Graph()
##    G.add_edges_from(elist)
##    return G


def read_terrorist():
    file = networks_folder + "/terrorists/terrorist.pairs"
    G = nx.read_edgelist(file, nodetype=int)
    return G


def read_UC_Irvine():
    file = networks_folder + "/UC_Irvine2004/OClinks_w.txt"
    elist = []
    with open(file, "r") as f:
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return get_giant_component(G)


###------------ NEWER NETWORKS ------------###


def read_Arxiv_HepTh():
    ##    # The downloaded file is not in proper GML format for Networkx
    ##    # Run this once to reformat.
    ##    file = "Arxiv_ca-HepTh/hep-th.gml"
    ##    with open(file, "r") as f:
    ##        new_file_string = f.read().replace("\s+\[", "[")
    ##
    ##    with open("Arxiv_ca-HepTh/hep-th_reformatted.gml","w") as f:
    ##        f.write(new_file_string)

    file = networks_folder + "/Arxiv_ca-HepTh/hep-th_reformatted.gml"
    G = nx.read_gml(file)
    G = nx.convert_node_labels_to_integers(G, first_label=0)

    return get_giant_component(G)


def read_blogs():
    file = networks_folder + "/moreno_blogs/out.moreno_blogs_blogs"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)
    G.remove_edges_from(nx.selfloop_edges(G))

    return get_giant_component(G)


def read_club_membership():
    file = (
        networks_folder
        + "/brunson_club-membership/out.brunson_club-membership_club-membership"
    )
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            line = line.rstrip().split()[:2]
            e = (int(line[0]), int(line[1]) + 25)
            elist.append(e)

    B = nx.Graph()
    B.add_edges_from(elist)

    # Project onto people. Two people are linked if they belong to the
    # same club/board.
    G = bipartite.projected_graph(B, list(range(1, 26)))

    ##    # Project onto clubs.
    ##    G = bipartite.projected_graph(B, list(range(26,41)))

    return G


def read_facebook():
    file = networks_folder + "/ego-facebook/out.ego-facebook"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return G


def read_gplus():
    file = networks_folder + "/ego-gplus/out.ego-gplus"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return get_giant_component(G)


def read_highland():
    # signed network -- only take positive edges
    file = networks_folder + "/ucidata-gama/out.ucidata-gama"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            line = list(map(int, line.rstrip().split()))
            if line[2] == 1:
                e = (line[0], line[1])
                elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return get_giant_component(G)


def read_highschool():
    file = networks_folder + "/moreno_highschool/out.moreno_highschool_highschool"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return G


def read_jazz():
    file = networks_folder + "/arenas-jazz/out.arenas-jazz"
    elist = []
    with open(file, "r") as f:
        skip = next(f)  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return G


def read_karate():
    file = networks_folder + "/ucidata-zachary/out.ucidata-zachary"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return G


def read_prison():
    file = networks_folder + "/prison/prison.dat.txt"
    with open(file, "r") as f:
        skip = [next(f) for _ in range(4)]
        A = f.read().strip().split()
        N = 67
        A = np.reshape(A, (N, N)).astype(int)
        G = nx.from_numpy_array(A, create_using=nx.Graph())

    return G


def read_residence_oz():
    file = networks_folder + "/moreno_oz/out.moreno_oz_oz"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return G


def read_Sampson():
    # signed network -- only take positive links
    file = networks_folder + "/moreno_sampson/out.moreno_sampson_sampson"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            line = list(map(int, line.rstrip().split()))
            if line[2] == 1:
                e = (line[0], line[1])
                elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return G


def read_seventh():
    file = networks_folder + "/moreno_seventh/out.moreno_seventh_seventh"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return G


def read_taro():
    file = networks_folder + "/moreno_taro/out.moreno_taro_taro"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return G


def read_twitter():
    file = networks_folder + "/ego-twitter/out.ego-twitter"
    elist = []
    with open(file, "r") as f:
        skip = [next(f) for _ in range(2)]  # skip a line
        for line in f:
            e = tuple(int(x) for x in line.rstrip().split()[:2])
            elist.append(e)

    G = nx.Graph()
    G.add_edges_from(elist)

    return get_giant_component(G)


networks_dict = {
    "Adolescent health": read_adolescent,
    "Arxiv CondMat": read_arxiv_CondMat,
    "Arxiv GrQc": read_arxiv_GrQc,  # unused
    "CKM physicians": read_ckm,
    "Dolphins": read_dolphins,
    "Email Spain": read_email,
    "Email Enron": read_enron,
    "Email Eu Core": read_Eu_Core,  # unused
    "Freeman's EIES": read_Freemans,
    "Golden Age": read_golden,
    "Hypertext": read_hypertext,  # unused
    "Kapferer tailor": read_kapf,
    "Les Miserables": read_lesmis,
    "Marvel": read_Marvel,  # unused
    "Hollywood music": read_movies,
    "Network science": read_netscience,  # unused
    "NFL": read_NFL,  # unused
    "Intra-organizational": read_org,  # unused
    "Web of Trust": read_pgp,  # unused
    ##                "Sampson's monastery": read_Sampson_Pajek, # unused
    "Terrorist": read_terrorist,
    "UC Irvine": read_UC_Irvine,  # <-- old networks end here
    "Arxiv HepTh": read_Arxiv_HepTh,  # <-- newer networks start here
    "Blogs": read_blogs,
    "Club membership": read_club_membership,
    "Facebook": read_facebook,
    "Gplus": read_gplus,
    "Highland tribes": read_highland,
    "Highschool": read_highschool,
    "Prison": read_prison,
    "Jazz musicians": read_jazz,
    "Karate club": read_karate,
    "Residence hall": read_residence_oz,
    "Sampson's monastery": read_Sampson,
    "Seventh grade": read_seventh,
    "Taro exchange": read_taro,
    "Twitter": read_twitter,
}

small_networks = [
    "CKM physicians",
    "Dolphins",
    "Email Spain",
    "Freeman's EIES",
    "Golden Age",
    "Kapferer tailor",
    "Les Miserables",
    "Hollywood music",
    "Sampson's monastery",
    "Terrorist",
]


# Note: Twitter,  Facebook, Gplus are ego-networks
# >>> very low density & clustering. very disassortative
# Bad:
# -Twitter (way too big, ego-net, not often cited)
# -Gplus (way too big, ego-net)
# -Club membership (projection, too small/dense, not often cited)
# -Blogs (too big, not "social")
# -Arxiv HepTh (too big, already have Arxiv CondMat)
# Meh:
# -Facebook (moderate size, but ego-net)
# -Highland, Sampson (signed), Prison (not often cited)
# Okay: seventh grade (high density), Taro exchange (small)
# Good: Highschool, jazz musicians, karate club, residence hall


def read_any(name):
    assert (
        name in networks_dict
    ), "Name must be one of the following networks:\n" + "\n".join(networks_dict.keys())
    return networks_dict[name]()


def display_network_stats():
    print(
        "Network".ljust(22),
        "N".ljust(5),
        "E".ljust(5),
        "dens".ljust(7),
        "C".ljust(7),
        "r".ljust(7),
        "cc",
    )

    for name in sorted(networks_dict):
        G = read_any(name)
        G.remove_edges_from(nx.selfloop_edges(G))
        cc = sorted(nx.connected_components(G), key=len, reverse=True)
        print(
            name.ljust(22),
            str(nx.number_of_nodes(G)).ljust(5),
            str(nx.number_of_edges(G)).ljust(5),
            ("%0.4f" % nx.density(G)).ljust(7),
            ("%0.4f" % nx.transitivity(G)).ljust(7),
            ("%0.4f" % nx.degree_assortativity_coefficient(G)).ljust(7),
            len(cc),
        )


def save_network_stats_table(outfile, sort_by="density"):
    titles = []
    num_nodes = []
    num_edges = []
    density = []
    avg_k = []
    max_k = []
    min_k = []
    ASPL = []
    ##    diam = []
    assortativity = []
    transitivity = []
    avg_clustering = []
    modularity = []

    for name in small_networks:
        print(name)
        G = read_any(name)
        n = nx.number_of_nodes(G)
        e = nx.number_of_edges(G)
        titles.append(name)
        num_nodes.append(n)
        num_edges.append(e)
        density.append(round(e / (n * (n - 1) / 2), 3))
        avg_k.append(round(2 * nx.number_of_edges(G) / nx.number_of_nodes(G), 1))
        ##        max_k.append(max(list(nx.degree(G,G.nodes()).values())))
        ##        min_k.append(min(list(nx.degree(G,G.nodes()).values())))
        ASPL.append(round(nx.average_shortest_path_length(G), 2))
        ##        diam.append(nx.diameter(G))
        assortativity.append(round(nx.degree_assortativity_coefficient(G), 2))
        transitivity.append(round(nx.transitivity(G), 2))
        ##        avg_clustering.append(round(nx.average_clustering(G),2))
        partition = community.best_partition(G)
        Q = get_modularity(G, partition)
        modularity.append(round(Q, 2))

    data = [
        [
            titles[i],
            num_nodes[i],
            num_edges[i],
            avg_k[i],
            density[i],
            transitivity[i],
            ASPL[i],
            modularity[i],
            assortativity[i],
        ]
        for i in range(len(num_nodes))
    ]

    df = pd.DataFrame(
        data,
        columns=[
            "network",
            "num_nodes",
            "num_edges",
            "avg_k",
            "density",
            "transitivity",
            "ASPL",
            "Q",
            "assortativity",
        ],
    )
    df.set_index("network")
    df = df.sort_values(sort_by)
    with open(outfile, "w") as f:
        f.write(df.to_csv(index=False))

    # PRINT MY TEX TABLE!
    with open(outfile, "r") as f:
        dfstring = f.read()
        dfstring = dfstring.replace(",", " & ")
        dfstring = dfstring.replace("\n", r"\\" + "\n")
        print(dfstring)


if __name__ == "__main__":
    ##    x = []
    ##    y = []
    ##    for network in small_networks:
    ##        G = read_any(network)
    ##        partition = community.best_partition(G)
    ##        Q = get_modularity(G,partition)
    ##        x.append(nx.transitivity(G))
    ##        y.append(Q)
    ##    plt.plot(x,y,'o')
    ##    plt.xlabel("Transitivity")
    ##    plt.ylabel("Modularity")
    ##    plt.show()

    G = read_any("Network science")
    print(G.number_of_nodes())
    pos = nx.spring_layout(G, k=0.09, iterations=25)
    partition = community.best_partition(G)

    # extract top communities and color them
    from collections import Counter

    counts = [x[0] for x in Counter(list(partition.values())).most_common(5)]
    cmap = ["red", "green", "black", "magenta", "cyan"]
    cols = []
    for node in G.nodes():
        if partition[node] in counts:
            cols.append(cmap[counts.index(partition[node])])
        else:
            cols.append("white")

    nodes = nx.draw_networkx_nodes(G, pos=pos, node_size=25, node_color=cols)
    edges = nx.draw_networkx_edges(G, pos=pos, edge_width=5, edge_color="#DEB992")
    ax = plt.axes()
    x = "#051622"
    ax.spines["bottom"].set_color(x)
    ax.spines["top"].set_color(x)
    ax.spines["left"].set_color(x)
    ax.spines["right"].set_color(x)
    ax.set_facecolor(x)
    plt.show()

    # save_network_stats_table("network_statistics_NEW.csv","num_nodes")


##    # Construct edgelists with quoteProbs
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
