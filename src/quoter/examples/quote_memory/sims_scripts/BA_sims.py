import quoter.quoter_model as qm
import os
import numpy as np
import networkx as nx
import itertools


def closest(num, arr):
    """
    Find the closest value in an array to a given number. This is used to find the parameter 'm' such that the ACTUAL average degree (2m-2m^2/N) is actually close to the DESIRED average degree

    :param num: The number to find the closest value to
    :param arr: The array of values to search through. Must be sorted
    :returns: The index of the closest value in the array to
    """

    curr = arr[0]
    i = 0
    for j, val in enumerate(arr):
        if abs(num - val) < abs(num - curr):
            curr = val
            i = j
    return i


if __name__ == "__main__":
    N = 200
    q = 0.5
    T = 1000

    trials_list = list(range(200))

    # this whole block here is just to find 'm' such that the ACTUAL average
    # degree (2m-2m^2/N) is actually close to the DESIRED average degree.
    # We could just loop over all 'actual k', but that would take longer
    desired_k = np.arange(2, 21, 2)
    m_list = np.arange(1, 50.1, 1)  # candidate 'm's
    actual_k = [
        2 * m - 2 * m**2 / N for m in m_list
    ]  # actual degree for each candidate 'm'
    # for each desired k, find index of 'm' in m_list which has closest actual k
    ind = [closest(k, [2 * m - 2 * m**2 / N for m in m_list]) for k in desired_k]
    # best 'm's
    m_list = m_list[ind]

    params_init = itertools.product(m_list, trials_list)
    params = [P for i, P in enumerate(params_init)]

    for m0, trial in params:
        m = int(m0)
        outdir = "../data_BA/"
        outfile = "N%i_m%i_q%0.1f_T%i_sim%i.txt" % (N, m, q, T, trial)
        if not os.path.isfile(
            os.path.join(outdir, "edge", outfile)
        ):  # avoid re-doing & overwriting
            G0 = nx.barabasi_albert_graph(n=N, m=m).to_directed()  # bidirectional
            G = nx.DiGraph(G0)  # convert to directed
            qm.quoter_model_sim(G, q, T, outdir, outfile)
