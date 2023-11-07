import networkx as nx
import random
import os
import quoter.quoter_model as qm
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def simulation(
    network_type="ER",  # "BA", "WS"
    N=100,
    q_list=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] + [0.99, 0.999, 0.9999],
    k_list=[6, 20],
    T=1000,
    trials_list=list(range(200)),
    outdir="output/ER/",
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

            G = nx.DiGraph(G0)
            print("Entering simulation...")
            qm.quoter_model_sim(
                G, q, T, outdir, outfile, write_data=qm.write_all_data, verbose=True
            )
        else:
            print(
                f"The experiment has already been run with these parameters in the proposed save location: {outfile}"
            )


def process_results(
    network_type="ER",  # "BA", "WS"
    N=100,
    q_list=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] + [0.99, 0.999, 0.9999],
    k_list=[6, 20],
    T=1000,
    trials_list=list(range(200)),
    outdir="output/ER/",
):
    # average hx vs average degree
    for k in k_list:
        data = np.zeros((len(q_list)))  # , len(lam_list)))
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

                data[i] = np.mean(hx_list)

        df = pd.DataFrame(data=data)
        df.to_csv(f"{outdir}hx_{network_type}_k{k}.csv", header=False, index=False)

    # TODO: add plotting, like in SBM case


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
