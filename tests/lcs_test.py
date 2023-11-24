# load packages
import LCSFinder as lcs
import numpy as np
import random
import time
import quoter.quoter_model as qm
import networkx as nx
from ProcessEntropy.CrossEntropy import timeseries_cross_entropy
from typing import Iterable, Union, Tuple, List
import pickle

def write_all_data_lcsfinder(
    G: nx.Graph,
    outdir: str,
    outfile: str,
    SBM: bool = False,
    verbose: bool = False,
    swap_quote_direction_lower_hx: bool = False,
    skip_edges: bool = False,
    skip_nodes: bool = False,
    skip_graph: bool = False,
):
    """Compute and write data from quoter model simulations.
    TODO: This feels like it should be split up more.
    Also make sure the outdir exists or create it if needed.


    Args:
        G (nx.Graph): _description_
        outdir (str): _description_
        outfile (str): _description_
    """

    # graph skeleton for calculating clustering, transitivity, ASPL, etc.
    H = G.to_undirected()

    # TODO: change from single-letter variables
    N = nx.number_of_nodes(G)
    m = int(N / 2)
    A = range(0, m)
    B = range(m, N)

    if SBM:  # not sure if needed, kept now for completeness
        edges = list(G.edges())
        random.shuffle(edges)

        w_sample: List = []
        i = 0
        while len(w_sample) < 250 and i < len(edges):
            e = edges[i]
            if (e[0] in A and e[1] in A) or (e[0] in B and e[1] in B):
                w_sample.append(e)
            i += 1

        b_sample: List = []
        i = 0
        while len(b_sample) < 250 and i < len(edges):
            e_i = edges[i]
            if (e_i[0] in A and e_i[1] in A) or (e_i[0] in B and e[1] in B):
                pass
            else:
                b_sample.append(e_i)
            i += 1

        edge_sample = w_sample + b_sample

    else:
        edges = random.sample(list(G.edges()), min(500, nx.number_of_edges(G)))
        nonedges = random.sample(
            list(nx.non_edges(G)), min(500, len(list(nx.non_edges(G))))
        )

        edge_sample = edges + nonedges

    alter_list, ego_list, qp_list, hx_list, dist_list = [], [], [], [], []
    tri_list, alter_degs, ego_degs = [], [], []
    swap_list = []

    # compute edge data
    if verbose:
        print(f"Calculating for edge_sample of length: {len(edge_sample)}")
    for e in edge_sample:
        #
        # compute cross entropies. e[0] = alter, e[1] = ego
        time_tweets_target = qm.words_to_tweets(
            G.nodes[e[1]]["words"], G.nodes[e[1]]["times"]
        )
        time_tweets_source = qm.words_to_tweets(
            G.nodes[e[0]]["words"], G.nodes[e[0]]["times"]
        )
        hx = timeseries_cross_entropy(
            time_tweets_target, time_tweets_source, please_sanitize=False
        )
        if swap_quote_direction_lower_hx:
            outfile.append("_sqd")
            hx_original = hx
            hx_swapped = timeseries_cross_entropy(
                time_tweets_source, time_tweets_target, please_sanitize=False
            )
            # print(f"For this edge, original hx = {hx_original}, swapped hx = {hx_swapped}")
            # TODO: how often to keep the new hx ie what to do now?
            hx = min(hx_original, hx_swapped)
            if hx_swapped < hx_original:
                swap_list.append(1)
            else:
                swap_list.append(0)
        else:
            swap_list.append(0)

        hx_list.append(hx)
        alter_list.append(e[0])
        ego_list.append(e[1])

        #
        # also record quote probability -- in this case it is the chance,
        # if the ego decides to quote in a given timestep, that it will quote from this particular alter.
        # it is NOT the q we initialised the quoter model with
        try:
            qp_list.append(1 / len(list(G.predecessors(e[1]))))
        except:
            if verbose:
                print("no predecessors for this node => nothing to quote from => qp=0")
            qp_list.append(0)

        #
        # also record edge embeddeness & edge clustering coefficient
        triangles, deg0, deg1, ECC = qm.edge_clustering_coeff(
            H, e[0], e[1], return_info=True
        )
        tri_list.append(triangles)
        alter_degs.append(deg0)
        ego_degs.append(deg1)

        #
        # also record distance between nodes
        try:
            dist = nx.shortest_path_length(G, source=e[0], target=e[1])
        except:
            dist = -1
        dist_list.append(dist)

    if not skip_edges:
        # write edge data
        if verbose:
            print(f"Writing edge data to {outdir}edge-{outfile}")
        with open(f"{outdir}edge-{outfile}", "w") as f:
            f.write(
                "alter ego quoteProb hx distance triangles alter_deg ego_deg swapped_hx\n"
            )  # header
            for i in range(len(hx_list)):
                edge_data_tuple = (
                    alter_list[i],
                    ego_list[i],
                    qp_list[i],
                    hx_list[i],
                    dist_list[i],
                    tri_list[i],
                    alter_degs[i],
                    ego_degs[i],
                    swap_list[i],
                )
                f.write("%i %i %0.8f %0.8f %i %i %i %i %i\n" % edge_data_tuple)

    if not skip_graph:
        # write graph data - TODO: embed calculated attributes in pickled graph object
        if verbose:
            print(f"Writing graph data to {outdir}graph-{outfile}")
        with open(f"{outdir}graph-{outfile}", "w") as f:
            # compute graph data
            if verbose:
                print("Done all edges; computing graph data")
            nnodes = nx.number_of_nodes(H)
            nedges = nx.number_of_edges(H)
            dens = nedges / (nnodes * (nnodes - 1) / 2)
            indegs = list(dict(G.in_degree(G.nodes())).values())
            outdegs = list(dict(G.out_degree(G.nodes())).values())
            ccs = nx.connected_components(H)

            community_dict = {x: 0 for x in A}
            community_dict.update({x: 1 for x in B})
            modularity = qm.get_modularity(H, community_dict)

            graph_data_tuple: Tuple = (
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
                len([ccs]),
                len(max(ccs, key=len)),
                modularity,
            )  # note avg_in == avg_out, so we only need to record one

            f.write(
                "nodes edges density average_degree min_indegree max_indegree "
                + "min_outdegree max_outdegree transitivity average_clustering "
                + "assortativity "
                + "number_of_components largest_component modularity\n"
            )  # header

            f.write(
                "%i %i %0.8f %0.8f %i %i %i %i %0.8f %0.8f %0.8f %i %i %0.6f"
                % graph_data_tuple
            )
        with open(f"{outdir}graph-{outfile[:-3]}pkl", "wb") as f_pickle:
            # note this is not robust to people using output files with a file extension of length != 3
            pickle.dump(G, f_pickle)

    if not skip_nodes:
        # write node data
        if verbose:
            print(f"Writing node data to {outdir}node-{outfile}")
        with open(f"{outdir}node-{outfile}", "w") as f:
            f.write("node indegree outdegree C h\n")  # header
            for node in G.nodes():
                # NOTE: source and target are the same, so just returns the true entropy rate of the solo text
                time_tweets_target = qm.words_to_tweets(
                    G.nodes[node]["words"], G.nodes[node]["times"]
                )
                time_tweets_source = time_tweets_target
                h = timeseries_cross_entropy(
                    time_tweets_target, time_tweets_source, please_sanitize=False
                )
                indeg = G.in_degree(node)
                outdeg = G.out_degree(node)
                C = nx.clustering(H, node)
                f.write("%i %i %i %0.8f %0.8f\n" % (node, indeg, outdeg, C, h))

if __name__=="__main__":
    network_type = "ER"
    N = 500
    q_list = [
        0.5,
    ]
    k_list = [5]
    T = 100
    trials_list = list(range(1))
    outdir = "./output/"

    """
    for N=50, T=1000:
    Python Only: 260.3832244873047
    LSCFinder: 224.34911823272705

    for N=500, T=100:
    Python Only: 15.421194791793823
    LSCFinder: 10.91908597946167

    Note however that T=1000 is typically chosen to ensure the entropy estimator converges
    (even though it is by far the limiting factor in calculations)

    """

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
    outfile = "%s_N%i_k%i_q%0.4f_T%i_sim%i.txt" % (network_type, N, k_list[0], q_list[0], T, trial)
    # watch; this will always start at trial 0

    G_post_sim = qm.quoter_model_sim(
        G0,
        quote_prob=q_list[0],
        timesteps=T,
        outdir=outdir,
        outfile="PO_"+outfile,
        verbose=True,
        write_data=None
    )
    print("created G_post_sim")

    # PythonOnly
    start1 = time.time()
    qm.write_all_data(G=G_post_sim,
    outdir=outdir,
    outfile="PO_"+outfile,
    verbose=True,)
    end1 = time.time()

    print("done PO")

    # LCSFinder
    start2 = time.time()
    write_all_data_lcsfinder(G=G_post_sim,
    outdir=outdir,
    outfile="LCSF_"+outfile,
    verbose=True,)
    end2 = time.time()

    print(f"Python Only: {end1-start1}")
    print(f"LSCFinder: {end2-start2}")

# def BruteForceLCSs(inds, s1, s2):
#     '''
#     Brute force version for testing.
#     '''
#     brute_lcss = []
#     for ind in inds:
#         mx = 0
#         for i in range(ind[1]):
#             k = 0
#             while ind[0]+k < len(s1) and i+k < ind[1] and s1[ind[0]+k] == s2[i+k]:
#                 k += 1
#             mx = max(mx, k)
#         brute_lcss.append(mx)
#     return brute_lcss


# def run_tests():
#     # initialise arrays
#     s1_l = np.arange(7)
#     s2_l = np.arange(8,12)

#     s1 = lcs.Vector1D([int(x) for x in ([np.floor(x) for x in s1_l])])
#     s2 = lcs.Vector1D([int(x) for x in ([np.floor(x) for x in s2_l])])
    
#     ob = lcs.LCSFinder(s1,s2) # s1 and then s2

#     assert ob.GetS() == (1, 2, 3, 4, 5, 6, 7, 0, 8, 9, 10, 11)
#     assert ob.GetSA() == (7, 0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11)


#     s1_l = [0, 1, 1, 1, 1, 0, 0, 0]
#     s2_l = [0, 1, 1, 0, 0, 1, 0, 0]

#     # set up objects
#     s2 = lcs.Vector1D([int(x) for x in ([np.floor(x) for x in s2_l])])
#     s1 = lcs.Vector1D([int(x) for x in ([np.floor(x) for x in s1_l])])
#     ob = lcs.LCSFinder(s1,s2) 

#     # set up indices to search from
#     assert ob.GetS() == (1, 2, 2, 2, 2, 1, 1, 1, 0, 1, 2, 2, 1, 1, 2, 1, 1)
#     assert ob.GetSA() == (8, 16, 7, 15, 6, 5, 12, 13, 9, 0, 14, 4, 11, 3, 10, 2, 1)

#     l_t =  lcs.Vector2D(tuple((i,i+1) for i in range(len(s1_l))))

#     assert ob.ComputeAllLCSs(l_t) == (1, 1, 2, 3, 3, 2, 2, 1)
#     assert BruteForceLCSs(l_t,s1,s2) == list(ob.ComputeAllLCSs(l_t)) 

#     cases = 10000
#     max_len = 100
#     alpha_sz = 2

#     for tc in range(cases):
#         s1_l = [random.randint(0, alpha_sz-1) for _ in range(random.randint(0, max_len-1))]
#         s2_l = [random.randint(0, alpha_sz-1) for _ in range(random.randint(0, max_len-1))]

#         s1 = lcs.Vector1D([int(x) for x in ([np.floor(x) for x in s1_l])])
#         s2 = lcs.Vector1D([int(x) for x in ([np.floor(x) for x in s2_l])])

#         ob = lcs.LCSFinder(s1, s2)

#         # Test suffix array construction
#         s = ob.GetS()
#         sa = ob.GetSA()

#         # Naive suffix array construction using O(N^2 log N) time
#         brute_sa = list(range(len(s)))
#         brute_sa.sort(key=lambda i: (s[i:], i))
#         # print("tc", tc, len(s1), len(s2))
#         assert brute_sa == list(sa)

#         # Test LCP
#         a, b = random.randint(0, len(s)-1), random.randint(0, len(s)-1)
#         lcp = ob.FindLCP(a, b)
#         brute_lcp = 0
#         for k in range(len(s)-max(a, b)):
#             if s[a+k] != s[b+k]:
#                 break
#             brute_lcp += 1
#         # print("lcp", a, b, lcp, brute_lcp)
#         assert lcp == brute_lcp

#         # Test LCSs
#         inds = []
#         s2idx = 0
#         for i in range(len(s1)):
#             if s2idx < len(s2):
#                 inds.append((i, s2idx))
#             if s2idx < len(s2) and random.randint(0, 1) == 1:
#                 s2idx += 1

#         brute_lcss = BruteForceLCSs(inds, s1, s2)

#         inds_ob = lcs.Vector2D(tuple(inds))
#         lcss = ob.ComputeAllLCSs(inds_ob)
        
#         assert brute_lcss == list(lcss)

# def __main__():
#     run_tests()
#     print('LCSFinder working.')

# __main__()