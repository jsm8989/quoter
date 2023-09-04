import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    N = 200
    M = 1000
    q = 0.5
    T = 1000
    mu_list = np.arange(0.05, 0.51, 0.05)
    trials_list = range(200)

    W = np.zeros(len(mu_list))
    B = np.zeros(len(mu_list))

    for i, mu in enumerate(mu_list):
        print(mu)
        hx_AA, hx_BB, hx_AB, hx_BA = [], [], [], []
        for trial in trials_list:
            efile = "output/edge/N%i_mu%0.4f_M%i_q%0.2f_T%i_sim%i.txt" % (
                N,
                mu,
                M,
                q,
                T,
                trial,
            )

            try:
                edata = pd.read_csv(efile, sep=" ")
            except:
                print(f"No data for mu={mu}, trial={trial}")

            else:
                block1 = list(range(0, int(N / 2)))
                block2 = list(range(int(N / 2), N))

                data_AA = (
                    edata["hx"]
                    .loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block1))]
                    .values
                )
                data_BB = (
                    edata["hx"]
                    .loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block2))]
                    .values
                )
                data_AB = (
                    edata["hx"]
                    .loc[(edata["ego"].isin(block1)) & (edata["alter"].isin(block2))]
                    .values
                )
                data_BA = (
                    edata["hx"]
                    .loc[(edata["ego"].isin(block2)) & (edata["alter"].isin(block1))]
                    .values
                )
                hx_AA.extend(data_AA)
                hx_BB.extend(data_BB)
                hx_AB.extend(data_AB)
                hx_BA.extend(data_BA)

        W[i] = np.mean(hx_AA + hx_BB)
        B[i] = np.mean(hx_AB + hx_BA)

    df = pd.DataFrame(data={"mu": mu_list, "hx_w": W, "hx_b": B})
    df.to_csv("hx_SBM.csv", index=False)

    # PLOT
    data = pd.read_csv("output/summaries/hx_SBM.csv")
    plt.plot(data["mu"].values, data["hx_w"].values, label="within")
    plt.plot(data["mu"].values, data["hx_b"].values, label="between")
    plt.legend()
    plt.xlabel(r"$\mu$")
    plt.ylabel(r"$\langle h_\times \rangle$")
    plt.show()
