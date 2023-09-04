import numpy as np
import pandas as pd
import os


if __name__ == "__main__":
    N = 100
    q_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9] + [0.99, 0.999, 0.9999]
    lam_list = [1]
    k_list = [6, 20]
    T = 1000
    trials_list = list(range(10))

    network_type = "ER"  # "BA", "WS"

    # average hx vs average degree
    for k in k_list:
        data = np.zeros((len(q_list), len(lam_list)))
        for i, q in enumerate(q_list):
            for j, lam in enumerate(lam_list):
                print("k%i q%0.4f lambda%i" % (k, q, lam))
                hx_list = []
                for trial in trials_list:
                    efile = "output/edge/N%i_k%i_q%0.4f_T%i_sim%i.txt" % (
                        N,
                        k,
                        q,
                        T,
                        trial,
                    )

                    if os.path.isfile(efile):
                        edata = pd.read_csv(efile, sep=" ")
                        hx_list.extend(edata["hx"].values)

                    else:
                        print(
                            f"file not found for k={k}, q={q}, lam={lam}, trial={trial}"
                        )

                data[i, j] = np.mean(hx_list)

        df = pd.DataFrame(data=data)
        df.to_csv(
            f"output/summaries/hx_{network_type}_k{k}.csv", header=False, index=False
        )
