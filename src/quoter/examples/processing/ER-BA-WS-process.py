import numpy as np
import pandas as pd
import os


if __name__ == "__main__":
    N = 100
    q_list = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.99, 0.999, 1]
    lam_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    k_list = [5, 10, 15, 20, 25]
    T = 1000
    trials_list = list(range(100))

    network_type = "ER"  # "BA", "WS"

    # average hx vs average degree
    for k in k_list:
        data = np.zeros((len(q_list), len(lam_list)))
        for i, q in enumerate(q_list):
            for j, lam in enumerate(lam_list):
                print("k%i q%0.4f lambda%i" % (k, q, lam))
                hx_list = []
                for trial in trials_list:
                    efile = f"./data_{network_type}/edge/*.txt"  # add appropriate filename from previous simulations

                    if os.path.isfile(efile):
                        edata = pd.read_csv(efile, sep=" ")
                        hx_list.extend(edata["hx"].values)

                    else:
                        print("file not found", k, q, lam, trial)

                data[i, j] = np.mean(hx_list)

        df = pd.DataFrame(data=data)
        df.to_csv("hx_ER_k%i.csv" % k, header=False, index=False)
