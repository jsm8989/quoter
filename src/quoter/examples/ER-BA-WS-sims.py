import networkx as nx
import random
import os
import quoter.quoter_model as qm
import itertools


def write_data(G, outdir, outfile):
    """
    Compute and write data from quoter model simulations.
    TODO compare to similar functions in other files.

    :param G: NetworkX graph to be analysed
    :param outdir: Path to output directory for data to be written
    :param outfile: Path to output file for data to be written
    """

    H = nx.Graph(G)

    edge_sample = random.sample(list(G.edges()), min(500, nx.number_of_edges(G)))

    # compute edge data
    for edge in edge_sample:
        # compute all cross entropies. edge[0] = alter, edge[1] = ego
        time_tweets_target = qm.words_to_tweets(
            G.nodes[edge[1]]["words"], G.nodes[edge[1]]["times"]
        )
        time_tweets_source = qm.words_to_tweets(
            G.nodes[edge[0]]["words"], G.nodes[edge[0]]["times"]
        )
        hx = qm.timeseries_cross_entropy(
            time_tweets_target, time_tweets_source, please_sanitize=False
        )

        # record cross-entropy
        G[edge[0]][edge[1]]["hx"] = hx

        # record quote probability
        G[edge[0]][edge[1]]["quoteProb"] = 1 / len(list(G.predecessors(edge[1])))

        # record edge embeddeness & edge clustering coefficient
        triangles, deg0, deg1, ECC = qm.edge_clustering_coeff(
            H, edge[0], edge[1], return_info=True
        )
        G[edge[0]][edge[1]]["tri"] = triangles
        G[edge[0]][edge[1]]["deg0"] = deg0
        G[edge[0]][edge[1]]["deg1"] = deg1

    # write edge data
    print(f"writing to {outdir}edge/{outfile}")
    with open(f"{outdir}edge/{outfile}", "w") as f:
        f.write("alter ego quoteProb hx triangles alter_deg ego_deg\n")  # header
        for e in edge_sample:
            f.write(
                "%i %i %0.8f %0.8f %i %i %i\n"
                % (
                    e[0],
                    e[1],
                    G[e[0]][e[1]]["quoteProb"],
                    G[e[0]][e[1]]["hx"],
                    G[e[0]][e[1]]["tri"],
                    G[e[0]][e[1]]["deg0"],
                    G[e[0]][e[1]]["deg1"],
                )
            )


if __name__ == "__main__":
    network_type = "ER"  # "BA", "WS"

    N = 100
    q_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] + [0.99, 0.999, 0.9999]
    # lam_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    k_list = [6, 20]
    T = 1000
    trials_list = list(range(10))

    params_init = itertools.product(
        q_list, k_list, trials_list
    )  # lam_list, k_list, trials_list)
    params = [P for i, P in enumerate(params_init)]

    for q, k, trial in params:  # lam,
        outdir = "output/"
        # outfile = "N%i_k%i_q%0.4f_lam%i_T%i_sim%i.txt" % (N, k, q, lam, T, trial)
        outfile = "N%i_k%i_q%0.4f_T%i_sim%i.txt" % (N, k, q, T, trial)

        if not os.path.isfile(os.path.join(outdir, "edge", outfile)):
            if network_type == "BA":
                G0 = nx.barabasi_albert_graph(N, int(k / 2))
            elif network_type == "ER":
                G0 = nx.erdos_renyi_graph(N, k / (N - 1))
            else:  # default to small networks
                p = k  # TODO: double check original difference here
                G0 = nx.watts_strogatz_graph(n=N, k=k, p=p)

            G = nx.DiGraph(G0)  # convert to directed
            print("Entering simulation...")
            qm.quoter_model_sim(G, q, T, outdir, outfile, write_data=write_data)
