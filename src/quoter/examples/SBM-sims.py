import os
import networkx as nx
import numpy as np
import random
import itertools
import quoter.quoter_model as qm
from processing.make_SBM import make_SBM_simple, get_modularity


def write_data(G, outdir, outfile):
    """
    Compute and write data from quoter model simulations.
    TODO compare to similar functions in other files.

    :param G: NetworkX graph to be analysed
    :param outdir: Path to output directory for data to be written
    :param outfile: Path to output file for data to be written
    """

    # graph skeleton for calculating clustering, transitivity, ASPL, etc.
    H = G.to_undirected()

    N = nx.number_of_nodes(G)
    m = int(N / 2)
    A = range(0, m)
    B = range(m, N)

    edges = list(G.edges())
    random.shuffle(edges)

    w_sample = list()
    i = 0
    while len(w_sample) < 250 and i < len(edges):
        e = edges[i]
        if (e[0] in A and e[1] in A) or (e[0] in B and e[1] in B):
            w_sample.append(e)
        i += 1

    b_sample = list()
    i = 0
    while len(b_sample) < 250 and i < len(edges):
        e_i = edges[i]
        if (e_i[0] in A and e_i[1] in A) or (e_i[0] in B and e[1] in B):
            pass
        else:
            b_sample.append(e_i)
        i += 1

    full_sample = w_sample + b_sample

    sources = []
    targets = []
    quoteProba_list = []
    hx_list = []
    dist_list = []
    triangles_list = []
    deg0_list = []
    deg1_list = []
    for e in full_sample:
        s = e[0]
        t = e[1]
        sources.append(s)
        targets.append(t)

        time_tweets_source = qm.words_to_tweets(
            G.nodes[s]["words"], G.nodes[s]["times"]
        )
        time_tweets_target = qm.words_to_tweets(
            G.nodes[t]["words"], G.nodes[t]["times"]
        )
        hx = qm.timeseries_cross_entropy(
            time_tweets_target, time_tweets_source, please_sanitize=False
        )
        hx_list.append(hx)

        # also record quote probability
        if s in G.predecessors(t):
            quoteProba = 1 / len(list(G.predecessors(t)))
        else:
            quoteProba = 0
        quoteProba_list.append(quoteProba)

        # also record distance between nodes
        try:
            dist = nx.shortest_path_length(G, source=s, target=t)
        except:
            dist = 0
        dist_list.append(dist)

        # also record edge embeddeness & edge clustering coefficient
        triangles, deg0, deg1, _ = qm.edge_clustering_coeff(
            H, e[0], e[1], return_info=True
        )
        triangles_list.append(triangles)
        deg0_list.append(deg0)
        deg1_list.append(deg1)

    # write edge data
    with open(f"{outdir}edge/{outfile}", "w") as f:
        f.write("alter ego quoteProb hx triangles alter_deg ego_deg dist\n")  # header
        for i in range(len(targets)):
            f.write(
                "%i %i %0.8f %0.8f %i %i %i %i\n"
                % (
                    sources[i],
                    targets[i],
                    quoteProba_list[i],
                    hx_list[i],
                    triangles_list[i],
                    deg0_list[i],
                    deg1_list[i],
                    dist_list[i],
                )
            )
    # compute graph data
    nnodes = nx.number_of_nodes(H)
    nedges = nx.number_of_edges(H)
    dens = nedges / (nnodes * (nnodes - 1) / 2)
    indegs = list(dict(G.in_degree(G.nodes())).values())
    outdegs = list(dict(G.out_degree(G.nodes())).values())
    ccs = sorted(nx.connected_components(H), key=len, reverse=True)
    comm_dict = {x: 0 for x in A}
    comm_dict.update({x: 1 for x in B})
    Q = get_modularity(H, comm_dict)

    data_tuple = (
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
        Q,
    )  # note avg_in == avg_out, so we only need to record one

    # write graph data
    with open(f"{outdir}graph/{outfile}", "w") as f:
        f.write(
            "nodes edges density average_degree min_indegree max_indegree "
            + "min_outdegree max_outdegree transitivity average_clustering "
            + "assortativity "
            + "number_of_components largest_component modularity\n"
        )  # header

        f.write(
            "%i %i %0.8f %0.8f %i %i %i %i %0.8f %0.8f %0.8f %i %i %0.6f" % data_tuple
        )

    # write node data
    with open(f"{outdir}node/{outfile}", "w") as f:
        f.write("node indegree outdegree C h\n")  # header
        for node in G.nodes():
            time_tweets_target = qm.words_to_tweets(
                G.nodes[node]["words"], G.nodes[node]["times"]
            )
            time_tweets_source = qm.words_to_tweets(
                G.nodes[node]["words"], G.nodes[node]["times"]
            )
            h = qm.timeseries_cross_entropy(
                time_tweets_target, time_tweets_source, please_sanitize=False
            )
            indeg = G.in_degree(node)
            outdeg = G.out_degree(node)
            C = nx.clustering(H, node)
            f.write("%i %i %i %0.8f %0.8f\n" % (node, indeg, outdeg, C, h))


## write edgelist for SBM
# nx.write_edgelist(G, os.path.join(outdir, "edgelist_" + outfile), delimiter=" ", data=False)


if __name__ == "__main__":
    N = 200
    M = 1000
    q = 0.5
    T = 1000
    mu_list = np.arange(0.05, 0.51, 0.05)
    trials_list = range(200)

    params_init = itertools.product(mu_list, trials_list)
    params = [P for i, P in enumerate(params_init)]

    for mu, trial in params:
        outdir = "output/"
        outfile = "N%i_mu%0.4f_M%i_q%0.2f_T%i_sim%i.txt" % (N, mu, M, q, T, trial)

        if not os.path.isfile(os.path.join(outdir, "edge/", outfile)):
            G0 = make_SBM_simple(N, mu, M)
            G = nx.DiGraph(G0)  # convert to directed
            qm.quoter_model_sim(G, q, T, outdir, outfile, write_data)
