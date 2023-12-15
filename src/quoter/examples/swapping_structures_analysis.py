import quoter.quoter_model as qm
import itertools
import networkx as nx
import os
import matplotlib.pyplot as plt
import quoter.examples.ER_BA_WS_sims as ERBA
import numpy as np
import pickle
import glob
import pandas as pd


if __name__ == "__main__":
    network_type = "ER"
    entropy_change_promoted = "raise" # or "decrease"
    swapping_mech = nx.double_edge_swap # or nx.directed_edge_swap
    N = 500
    q_list = [
        0.5,
    ]
    k_list = [30]
    T = 10
    trials_list = list(range(1))
    outdir = "./output/simple_swap/"

    if network_type == "BA":
        G0 = nx.barabasi_albert_graph(N, int(k_list[0] / 2))
    elif network_type == "ER":
        G0 = nx.erdos_renyi_graph(N, k_list[0] / (N - 1))
    else:  # default to small networks
        p = k_list[0]  # TODO: double check original difference here
        G0 = nx.watts_strogatz_graph(n=N, k=k_list[0], p=p)
        network_type="WS"

    G0 = nx.DiGraph(G0)

    

    trial = trials_list[0]
    outfile = "%s_N%i_k%i_q%0.4f_T%i_sim%i.txt" % (network_type+entropy_change_promoted, N, k_list[0], q_list[0], T, trial)
    # watch; this will always start at trial 0

    G_post_sim = qm.quoter_model_sim(
        G0,
        quote_prob=q_list[0],
        timesteps=T,
        outdir=outdir,
        outfile=outfile,
        verbose=True,
    )  # ideally do multiple and average the global entropy
    print("created G_post_sim")

    ## now calculate "global information flow" in the graph
    time_tweets_global = []
    for node in G_post_sim.nodes:
        time_tweets_global.extend(
            qm.words_to_tweets(
                G_post_sim.nodes[node]["words"], G_post_sim.nodes[node]["times"]
            )
        )
    global_entropy_rate = qm.timeseries_cross_entropy(
        time_tweets_global, time_tweets_global, please_sanitize=False
    )  # might take a long time to calculate, and TODO: NEEDS CHECKING. Should overwrite into saved graph file
    print(f"global entropy rate for trial {trial} = {global_entropy_rate:0.4f}")


    # TODO: get more quantitative comparison eg hx distributions, degree distributions, connectivity/clustering etc
    fig1 = plt.figure(f"original graph of entropy {global_entropy_rate:0.4f}")
    nx.draw_networkx(G0)
    #plt.show()

    # to avoid saving different filenames, will in this case use trial number as index for how many pairs of edges have attempted to be swapped.
    # while str(input("Do you want to continue? (n): ")) != "n":
    for _ in range(100):
        outfile = "%s_N%i_k%i_q%0.4f_T%i_sim%i.txt" % (network_type+entropy_change_promoted, N, k_list[0], q_list[0], T, trial)

        if not os.path.isfile(f"{outdir}edge-{outfile}"):
            # random edge swapping step; other possible mechanisms

            potential_new_G = nx.double_edge_swap(G0.to_undirected()).to_directed() # or directed_edge_swap(G0).to_directed() ; can't get to work
            potential_new_G_post_sim = qm.quoter_model_sim(
                potential_new_G,
                quote_prob=q_list[0],
                timesteps=T,
                outdir=outdir,
                outfile=outfile,
            )
            # TODO: calculate new cross entropies
            ## now calculate "global information flow" in the graph
            time_tweets_instance = []
            for node in potential_new_G_post_sim.nodes:
                time_tweets_instance.extend(
                    qm.words_to_tweets(
                        potential_new_G.nodes[node]["words"],
                        potential_new_G.nodes[node]["times"],
                    )
                )
            new_global_entropy = qm.timeseries_cross_entropy(
                time_tweets_instance, time_tweets_instance, please_sanitize=False
            )  # might take a long time to calculate, and TODO: NEEDS CHECKING. Should overwrite into saved graph file

            # fig1 = plt.figure(f"previous graph of entropy {global_entropy_rate}")
            # nx.draw_networkx(G0)

            if (new_global_entropy < global_entropy_rate and entropy_change_promoted=="decrease") or (new_global_entropy > global_entropy_rate and entropy_change_promoted=="raise"):
                G0 = potential_new_G
                global_entropy_rate = new_global_entropy
                # could output the swapped edge here

            print(f"global entropy {trial} = {global_entropy_rate:0.4f}")
        else:
            print(f"trial {trial} skipped, pls continue")
        trial += 1

    fig2 = plt.figure(f"new graph of entropy {global_entropy_rate:0.4f}")
    nx.draw_networkx(G0)
    plt.show()

    exit(0)

    run_sim = False
    process_results = False
    if run_sim:
        params_init = itertools.product(q_list, k_list, trials_list)
        params = [P for i, P in enumerate(params_init)]

        for q, k, trial in params:
            outfile = f"N{N}_k{k}_q{q:0.4f}_T{T}_sim{trial}.txt"

            if not os.path.isfile(f"{outdir}edge-{outfile}"):
                G0 = nx.erdos_renyi_graph(N, k / (N - 1))

                G = nx.DiGraph(G0)
                print("\nEntering simulation...")
                updated_graph = qm.quoter_model_sim(
                    G, q, T, outdir, outfile, write_data=None, verbose=True
                )

                # plt.title(f"{network_type} graph with {len(updated_graph.nodes())} nodes and {len(updated_graph.edges())} edges after simulating the quoter model")
                # nx.draw(updated_graph)
                # plt.show()

                updated_graph_undirected = updated_graph.to_undirected()

                print("calculating plot stuff")
                degree_sequence = sorted(
                    (d for n, d in updated_graph_undirected.degree()), reverse=True
                )
                dmax = max(degree_sequence)

                fig = plt.figure("Degree of a random graph", figsize=(8, 8))
                # Create a gridspec for adding subplots of different sizes
                axgrid = fig.add_gridspec(5, 4)

                ax0 = fig.add_subplot(axgrid[0:3, :])
                Gcc = updated_graph_undirected.subgraph(
                    sorted(
                        nx.connected_components(updated_graph_undirected),
                        key=len,
                        reverse=True,
                    )[0]
                )
                pos = nx.spring_layout(Gcc, seed=10396953)
                nx.draw_networkx_nodes(Gcc, pos, ax=ax0, node_size=20)
                nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.4)
                ax0.set_title("Connected components of G")
                ax0.set_axis_off()

                ax1 = fig.add_subplot(axgrid[3:, :2])
                ax1.plot(degree_sequence, "b-", marker="o")
                ax1.set_title("Degree Rank Plot")
                ax1.set_ylabel("Degree")
                ax1.set_xlabel("Rank")

                ax2 = fig.add_subplot(axgrid[3:, 2:])
                ax2.bar(*np.unique(degree_sequence, return_counts=True))
                ax2.set_title("Degree histogram")
                ax2.set_xlabel("Degree")
                ax2.set_ylabel("# of Nodes")

                fig.tight_layout()
                # plt.show()
                # print("should have plotted 3 figures")
                # save the mpl figure as pickle format
                with open(f"{outdir}figure-{outfile}.pkl", "wb") as fs:
                    pickle.dump(fig, fs)
                print("saved pickled figure")

                qm.write_all_data(
                    updated_graph,
                    outdir,
                    outfile,
                    verbose=True,
                    swap_quote_direction_lower_hx=True,
                )
            else:
                print(
                    f"The experiment has already been run with these parameters in the proposed save location: {outfile}"
                )

    if process_results:
        ERBA.process_results(
            network_type=network_type,
            N=N,
            q_list=q_list,
            k_list=k_list,
            T=T,
            trials_list=trials_list,
            outdir=outdir,
            plot=True,
        )

        # for figure_file in glob.glob(f"{outdir}figure*"):
        #     with open(figure_file, "rb") as f:
        #         fig = pickle.load(f)
        #         plt.suptitle(figure_file[len(outdir):]+"\n")
        #         plt.show()

        # TODO: better to aggregate overall trials of the same graph
