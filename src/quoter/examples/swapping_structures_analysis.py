import quoter.quoter_model as qm
import itertools
import networkx as nx
import os
import matplotlib.pyplot as plt
import quoter.examples.ER_BA_WS_sims as ERBA
import numpy as np
import pickle
import glob


if __name__ == "__main__":

    network_type="ER"
    N=100
    q_list=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] + [0.99, 0.999, 0.9999, 1]
    k_list=[6, 10, 19]
    T=1000
    trials_list=list(range(10))
    outdir="./output_swap/"


    run_sim = False
    process_results = True

    # ERBA.simulation(network_type=network_type,
    # N=N,
    # q_list=q_list,
    # k_list=k_list,
    # T=T,
    # trials_list=trials_list,
    # outdir=outdir)

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
                degree_sequence = sorted((d for n, d in updated_graph_undirected.degree()), reverse=True)
                dmax = max(degree_sequence)

                fig = plt.figure("Degree of a random graph", figsize=(8, 8))
                # Create a gridspec for adding subplots of different sizes
                axgrid = fig.add_gridspec(5, 4)

                ax0 = fig.add_subplot(axgrid[0:3, :])
                Gcc = updated_graph_undirected.subgraph(sorted(nx.connected_components(updated_graph_undirected), key=len, reverse=True)[0])
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
                #plt.show()
                #print("should have plotted 3 figures")
                # save the mpl figure as pickle format
                with open(f"{outdir}figure-{outfile}.pkl", 'wb') as fs:
                    pickle.dump(fig, fs)
                print("saved pickled figure")

                qm.write_all_data(updated_graph, outdir, outfile, verbose = True, swap_edges_lower_hx=True)
            else:
                print(
                    f"The experiment has already been run with these parameters in the proposed save location: {outfile}"
                )

    if process_results:
        ERBA.process_results(network_type=network_type,
        N=N,
        q_list=q_list,
        k_list=k_list,
        T=T,
        trials_list=trials_list,
        outdir=outdir,
        plot=True)

        # for figure_file in glob.glob(f"{outdir}figure*"):
        #     with open(figure_file, "rb") as f:
        #         fig = pickle.load(f)
        #         plt.suptitle(figure_file[len(outdir):]+"\n")
        #         plt.show()


                # TODO: better to aggregate overall trials of the same graph
