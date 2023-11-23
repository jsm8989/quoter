import networkx as nx
import random
import os
import quoter.quoter_model as qm
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle


def simulation(
    network_type="ER",  # "BA", "WS"
    N=100,
    q_list=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] + [0.99, 0.999, 0.9999],
    k_list=[6, 20],
    T=1000,
    trials_list=list(range(200)),
    outdir="output/ER/",
    check_simulation_output=False,
):
    params_init = itertools.product(q_list, k_list, trials_list)
    params = [P for i, P in enumerate(params_init)]

    for q, k, trial in params:
        outfile = "N%i_k%i_q%0.4f_T%i_sim%i.txt" % (N, k, q, T, trial)

        if not os.path.isfile(f"{outdir}edge-{outfile}"):
            if network_type == "BA":
                G0 = nx.barabasi_albert_graph(N, int(k / 2))
            elif network_type == "ER":
                G0 = nx.erdos_renyi_graph(N, k / (N - 1))
            else:  # default to small networks
                p = k  # TODO: double check original difference here
                G0 = nx.watts_strogatz_graph(n=N, k=k, p=p)

            G = nx.DiGraph(G0)  # assume this just gives a symmetric DiGraph...
            print("Entering simulation...")
            qm.quoter_model_sim(
                G, q, T, outdir, outfile, write_data=qm.write_all_data, verbose=False
            )
            print("simulation done and data written")

            if check_simulation_output:
                graph_data = pd.read_csv(
                    f"{outdir}graph-{outfile}",
                    sep=" ",
                )  # probably more useful in later processing steps

                node_data = pd.read_csv(
                    f"{outdir}node-{outfile}",
                    sep=" ",
                )

                plt.plot(
                    node_data["node"], node_data["h"], label="entropy rate of node text"
                )
                plt.plot(node_data["node"], node_data["indegree"], label="in degree")
                plt.plot(node_data["node"], node_data["outdegree"], label="out degree")
                plt.plot(
                    node_data["node"], node_data["C"], label="clustering coefficient"
                )
                plt.xlabel("Node")
                plt.legend()
                # plt.show()

                # find hx distribution across the graph:
                ## then code two possible ways of "total info flow":
                ## -- the distribution across all nodes(solo-entropy rate)/edges (cross-entropy)
                ## -- the overall entropy of all written text from all nodes

                # first: 2D edge hx distribution
                edge_data = pd.read_csv(
                    f"{outdir}edge-{outfile}",
                    sep=" ",
                )

                node_data = pd.read_csv(
                    f"{outdir}node-{outfile}",
                    sep=" ",
                )

                with open(
                    f"{outdir}graph-{outfile[:-3]}pkl",  # note this is not robust to people using output files with a file extension of length != 3
                    "rb",
                ) as f:
                    G = pickle.load(f)

                fig = plt.figure()
                ax1 = fig.add_subplot(projection="3d")

                def hx_z(x, y):
                    # for nodes x,y as ego, alter; create function for drawing semi-continuous 3d surface
                    # if x != y:
                    z_out = edge_data.loc[
                        edge_data["ego"] == x and edge_data["alter"] == y
                    ]["hx"]
                    print(z_out)
                    return z_out
                    # elif x == y:
                    #     return node_data.loc[node_data["node"] == x]["h"]
                    X = np.arange(len(G.nodes()))
                    print(X)
                    Y = X

                    X, Y = np.meshgrid(X, Y)
                    print(X)
                    Z = hx_z(X, Y)

                x, y, z = edge_data["ego"], edge_data["alter"], edge_data["hx"]

                # ax1.plot_surface(X, Y, Z)
                # TODO: now would like to distinguish between hx where an edge exists vs where it doesnt
                x_node, z_node = node_data["node"], node_data["h"]
                ax1.stem(x, y, z, basefmt=" ")
                ax1.stem(x_node, x_node, z_node, linefmt="r", basefmt=" ")
                # ax1.bar3d(x_node, x_node, z_node, "r")
                mean_hx = np.mean(list(z) + list(z_node))
                var_hx = np.var(list(z) + list(z_node))

                ax1.set_title(
                    f"2D hx distribution. Mean={mean_hx:0.4f}, var={var_hx:0.4f}"
                )
                # would be SO cool to see this evolve in real time as quoter_model continues
                ax1.set_xlabel("ego")
                plt.xticks(G.nodes())
                plt.yticks(G.nodes())
                ax1.set_ylabel("alter")

                fig_1d_dist = plt.figure()
                plt.hist(z)
                plt.title(
                    f"1D hx distribution. Mean={np.mean(z):0.4f}, var={np.var(z):0.4f}"
                )
                plt.xlabel("h_x")
                plt.ylabel("frequency")

                ## now calculate "global information flow" in the graph
                time_tweets_global = []
                for node in G.nodes:
                    time_tweets_global.extend(
                        qm.words_to_tweets(
                            G.nodes[node]["words"], G.nodes[node]["times"]
                        )
                    )
                global_entropy_rate = qm.timeseries_cross_entropy(
                    time_tweets_global, time_tweets_global, please_sanitize=False
                )  # might take a long time to calculate, and TODO: NEEDS CHECKING. Should overwrite into saved graph file

                fig1 = plt.figure()
                nx.draw_networkx(G)
                plt.title(
                    f"Global entropy rate on all combined words for this graph = {global_entropy_rate:0.4f}"
                )

                fig_degree = plt.figure()
                plt.plot(nx.degree_histogram(G.to_undirected()))
                plt.title(
                    "Degree distribution of the original (undirected) graph post quoter-model"
                )
                plt.xlabel("degree")
                plt.ylabel("frequency")

                plt.show()
        else:
            print(
                f"The experiment has already been run with these parameters in the proposed save location: {outfile}"
            )
            simulation(
                network_type,
                N,
                q_list,
                k_list,
                T,
                trials_list=[trials_list[-1] + 1],
                outdir=outdir,
                check_simulation_output=check_simulation_output,
            )


def process_results(
    network_type="ER",  # "BA", "WS"
    N=100,
    q_list=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] + [0.99, 0.999, 0.9999],
    k_list=[6, 20],
    T=1000,
    trials_list=list(range(200)),
    outdir="output/ER/",
    plot: bool = False,
):
    # average hx vs average degree
    for k in k_list:
        mean_hx_data = np.zeros((len(q_list)))  # , len(lam_list)))
        for i, q in enumerate(q_list):
            hx_list = []
            for trial in trials_list:
                outfile = "N%i_k%i_q%0.4f_T%i_sim%i.txt" % (
                    N,
                    k,
                    q,
                    T,
                    trial,
                )
                efile = f"{outdir}edge-{outfile}"

                if os.path.isfile(efile):
                    edata = pd.read_csv(efile, sep=" ")
                    hx_list.extend(edata["hx"].values)

                else:
                    print(f"file not found for k={k}, q={q}, trial={trial}")

            mean_hx_data[i] = np.mean(hx_list)

        df = pd.DataFrame(data={"q": q_list, "mean_hx": mean_hx_data})
        df.to_csv(f"{outdir}hx_{network_type}_k{k}.csv", index=False)

    # TODO: add plotting, like in SBM case
    if plot:
        for k in k_list:
            data_k = pd.read_csv(f"{outdir}hx_{network_type}_k{k}.csv")
            plt.plot(data_k["q"].values, data_k["mean_hx"].values, label=f"k={k}")
        plt.legend()
        plt.xlabel(r"$q$")
        plt.ylabel(r"$\langle h_\times \rangle$")
        plt.show()


def explore_file_outputs(filename):
    outdir = "./output/output_swap/"
    # TODO: for multiple runs since they are "the same"

    if os.path.isfile(outdir + filename):
        output_data = pd.read_csv(outdir + filename, sep=" ")
    else:
        raise Exception(f"{filename} does not exist inside {outdir}")
    plt.plot(output_data["quoteProb"], output_data["hx"], "o")
    plt.xlabel("quoteProb")
    plt.ylabel("hx for edge")
    plt.show()


if __name__ == "__main__":
    simulation(
        N=10,
        q_list=[0, 0.1],
        k_list=[6],
        T=100,
        trials_list=list(range(5)),
    )

    process_results(
        N=10,
        q_list=[0, 0.1],
        k_list=[6],
        T=100,
        trials_list=list(range(5)),
    )
