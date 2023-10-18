import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
from ProcessEntropy.CrossEntropyPythonOnly import (
    timeseries_cross_entropy,
)  # remote package; might have install dependency issues. If so use the following:
# from CrossEntropy import timeseries_cross_entropy
from typing import Iterable, Union, Tuple


def words_to_tweets(words: Iterable, times: Iterable):
    """
    Convert (words,times) array to a smaller array of (tweets,times)

    :param words: A list of words. Each word is a list of word tokens.
    :param times: A list of times. Each time it is called the words will be compared to each other to see if they are the same.
    :returns: A list of tuples where each tuple is a tweet
    """
    unique_times = list(sorted(set(times)))
    tweets = []
    # Add a tweet to the list of unique times
    for unq_t in unique_times:
        tweet = [w for w, t in zip(words, times) if t == unq_t]
        tweets.append(tweet)

    return [(t, w) for t, w in zip(unique_times, tweets)]


def write_all_data(G: nx.Graph, outdir: str, outfile: str, verbose: bool=False):
    """Compute and write data from quoter model simulations. This feels like it should be split up more.


    Args:
        G (nx.Graph): _description_
        outdir (str): _description_
        outfile (str): _description_
    """

    # graph skeleton for calculating clustering, transitivity, ASPL, etc.
    H = G.to_undirected()

    # compute edge data
    edges = random.sample(list(G.edges()), min(500, nx.number_of_edges(G)))
    nonedges = random.sample(
        list(nx.non_edges(G)), min(500, len(list(nx.non_edges(G))))
    )

    edge_sample = edges + nonedges
    alter_list, ego_list, qp_list, hx_list, dist_list = [], [], [], [], []
    tri_list, alter_degs, ego_degs = [], [], []

    if verbose:
        print("initialised for writing")

    for e in edge_sample:
        if verbose:
            print(f"Calculating cross-entropy for edge: {e}")
        
        # compute cross entropies. e[0] = alter, e[1] = ego
        time_tweets_target = words_to_tweets(
            G.nodes[e[1]]["words"], G.nodes[e[1]]["times"]
        )
        time_tweets_source = words_to_tweets(
            G.nodes[e[0]]["words"], G.nodes[e[0]]["times"]
        )
        hx = timeseries_cross_entropy(
            time_tweets_target, time_tweets_source, please_sanitize=False
        )
        hx_list.append(hx) # TODO: can swap pairs of edges based on this value when exploring network structural effects
        alter_list.append(e[0])
        ego_list.append(e[1])

        # also record quote probability
        try:
            qp_list.append(1 / len(list(G.predecessors(e[1])))) # TODO: double check why defined this way
        except:
            if verbose:
                print("no predecessors for this node, assigning qp=0")
            qp_list.append(0)

        # also record edge embeddeness & edge clustering coefficient
        triangles, deg0, deg1, ECC = edge_clustering_coeff(
            H, e[0], e[1], return_info=True
        )
        tri_list.append(triangles)
        alter_degs.append(deg0)
        ego_degs.append(deg1)

        # also record distance between nodes
        try:
            dist = nx.shortest_path_length(G, source=e[0], target=e[1])
        except:
            dist = -1
        dist_list.append(dist)


    # write graph data
    if verbose:
        print(f"Writing graph data to {outdir}graph/{outfile}")
    with open(outdir + "graph/" + outfile, "w") as f:

        # compute graph data
        if verbose:
            print("Done all edges; computing graph data")
        nnodes = nx.number_of_nodes(H)
        nedges = nx.number_of_edges(H)
        dens = nedges / (nnodes * (nnodes - 1) / 2)
        indegs = list(dict(G.in_degree(G.nodes())).values())
        outdegs = list(dict(G.out_degree(G.nodes())).values())
        ccs = sorted(nx.connected_components(H), key=len, reverse=True)
    
        data_tuple: Tuple = (
            nnodes,
            nedges,
            dens,
            np.mean(indegs),
            np.min(indegs),
            np.max(indegs),
            np.min(outdegs),
            np.max(outdegs),
            nx.transitivity(H),
            nx.average_clustering(H),
            nx.degree_assortativity_coefficient(H),
            len(ccs),
            len(ccs[0]),
        )  # note avg_in == avg_out, so we only need to record one
        
        f.write(
            "nodes edges density average_degree min_indegree max_indegree "
            + "min_outdegree max_outdegree transitivity average_clustering "
            + "assortativity "
            + "number_of_components largest_component\n"
        )  # header

        f.write("%i %i %0.8f %0.8f %i %i %i %i %0.8f %0.8f %0.8f %i %i" % data_tuple)

    # write edge data
    if verbose:
        print(f"Writing edge data to {outdir}edge/{outfile}")
    with open(outdir + "edge/" + outfile, "w") as f:
        f.write(
            "alter ego quoteProb hx distance triangles alter_deg ego_deg\n"
        )  # header
        for i in range(len(hx_list)):
            data_tuple = (
                alter_list[i],
                ego_list[i],
                qp_list[i],
                hx_list[i],
                dist_list[i],
                tri_list[i],
                alter_degs[i],
                ego_degs[i],
            )
            f.write("%i %i %0.8f %0.8f %i %i %i %i\n" % data_tuple)

    # write node data
    if verbose:
        print(f"Writing node data to {outdir}node/{outfile}")
    with open(outdir + "node/" + outfile, "w") as f:
        f.write("node indegree outdegree C h\n")  # header
        for node in G.nodes():
            time_tweets_target = words_to_tweets(
                G.nodes[node]["words"], G.nodes[node]["times"]
            )
            time_tweets_source = words_to_tweets(
                G.nodes[node]["words"], G.nodes[node]["times"]
            )
            h = timeseries_cross_entropy(
                time_tweets_target, time_tweets_source, please_sanitize=False
            )
            indeg = G.in_degree(node)
            outdeg = G.out_degree(node)
            C = nx.clustering(H, node)
            f.write("%i %i %i %0.8f %0.8f\n" % (node, indeg, outdeg, C, h))


def edge_clustering_coeff(
    G: nx.Graph, node_u: int, node_v: int, return_info: bool = False, draw: bool = False
):
    """
    Compute ECC between two nodes node_u and node_v, defined as the number of triangles containing both node_u and node_v divided by min(degrees(node_u,node_v))-1

    Args:
        G: NetworkX graph to be analysed. Must be directed
        node_u: node index of first node
        node_v: node index of second node
        return_info: if True return information about the algorithm
        draw: choose whether to visualise the graph

    Returns:
        triangles deg_u deg_v ECC (if return_info)
        ECC
    """
    u_nbrs = nx.neighbors(G, node_u)
    v_nbrs = nx.neighbors(G, node_v)
    uv_nbrs = set(u_nbrs) & set(v_nbrs)
    triangles = len(uv_nbrs)  # could be replaced by nx.triangles(G, [node_u,node_v]) or similar

    deg_u = nx.degree(G)[node_u]  # len(u_nbrs)
    deg_v = nx.degree(G)[node_v]  # len(v_nbrs)

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


def quoter_model_sim(
    G: nx.Graph,
    quote_prob: float,
    timesteps: int,
    outdir: str="./",
    outfile: str="test_output.txt",
    write_data=write_all_data,
    dunbar: Union[int, None] = None,
    verbose: bool=False,
):
    """Simulate the quoter model on a graph G. Nodes take turns generating content according to two
    mechanisms: (i) creating new content from a specified vocabulary distribution, (ii) quoting
    from a neighbor's past text.

    [1] Bagrow, J. P., & Mitchell, L. (2018). The quoter model: A paradigmatic model of the social
    flow of written information. Chaos: An Interdisciplinary Journal of Nonlinear Science, 28(7),
    075304.

    Args:
        G (nx.Graph): Directed graph to simulate quoter model on
        quote_prob (float): Quote probability q as defined in [1]
        timesteps (int): Number of time-steps to simulate for. timesteps=1000 really means 1000*nx.number_of_nodes(G), i.e. each node will have 'tweeted' ~1000 times
        outdir (string): Name of directory for data to be stored in
        outfile (string): Name of file for this simulation
        write_data (function): Can specify what data to compute & write.
        dunbar (int or None): If int, limit in-degree to dunbar's number
        verbose: <temp> giving useful output during testing
    """
    if verbose:
        # TODO would be useful to add summary statistics of provided networks in documentation
        print(f"G has {len(G.nodes())} nodes and {len(G.edges())} edges")
    
    # vocabulary distribution - NOTE: currently just uniform distribution of integers. Would like to choose optional distribution, including importing them or generating from LLMs
    alpha = 1.5
    z = 1000
    vocab = np.arange(1, z + 1)
    weights = vocab ** (-alpha)
    weights /= weights.sum()

    # limit IN-DEGREE to just dunbar's number
    if dunbar:
        for node in G.nodes():
            nbrs = list(G.predecessors(node))
            if len(nbrs) > dunbar:
                nbrs_rmv = random.sample(nbrs, len(nbrs) - dunbar)
                G.remove_edges_from([(nbr, node) for nbr in nbrs_rmv])

    # create initial tweet for each user
    startWords = 20
    for node in G.nodes():
        newWords = np.random.choice(
            vocab, size=startWords, replace=True, p=weights
        ).tolist()
        G.nodes[node]["words"] = newWords
        G.nodes[node]["times"] = [0] * len(newWords)

    if verbose:
        print("Initial vocab created; starting simulation")

    # simulate quoter model
    for timestep_ in range(1, timesteps * nx.number_of_nodes(G)):
        if verbose:
            print(timestep_)
            
        node = random.choice(list(G.nodes))

        # length of tweet
        tweetLength = np.random.poisson(lam=3)

        # quote with probability quote_prob, provided ego has alters to quote from
        nbrs = list(G.predecessors(node))
        if random.random() < quote_prob and len(nbrs) > 0:
            # pick a neighbor to quote from (simplifying assumption: uniformly at random from all neighbors)
            user_copied = random.choice(nbrs)

            # find a valid position in the neighbor's text to quote from
            words_friend = G.nodes[user_copied]["words"]
            numWords_friend = len(words_friend)
            copy_pos_start = random.choice(
                list(range(max(0, numWords_friend - tweetLength)))
            )
            copy_pos_end = min(numWords_friend - 1, copy_pos_start + tweetLength)
            newWords = words_friend[copy_pos_start:copy_pos_end]

        else:  # new content
            newWords = np.random.choice(
                vocab, size=tweetLength, replace=True, p=weights
            ).tolist()

        G.nodes[node]["words"].extend(newWords)
        G.nodes[node]["times"].extend([timestep_] * len(newWords))

    # save data
    if verbose:
        print("writing data")
    write_data(G, outdir, outfile, verbose)
