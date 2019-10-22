# -*- coding: utf-8 -*-

# make_configMod.py
# Tyson Pond
# Last Modified: 2019-10-21

import networkx as nx
import numpy as np
from read_networks import *
import matplotlib.pyplot as plt


def make_configMod(G):
    degree_seq = list(G.degree().values())
    if sum(degree_seq) % 2 != 0:
        degree_seq[0] += 1

    G=nx.configuration_model(degree_seq,create_using=nx.Graph())

    return G


networks_dict = {"Adolescent health": read_adolescent,
                "Arxiv CondMat": read_arxiv_CondMat,
##                "Arxiv GrQc": read_arxiv_GrQc,
                "CKM physicians": read_ckm,
                "Dolphins": read_dolphins,
                "Email Spain": read_email,
                "Email Enron": read_enron,
##                "Email Eu Core": read_Eu_Core,
                "Freeman's EIES": read_Freemans,
                "Golden Age": read_golden,
##                "Hypertext": read_hypertext,
                "Kapferer tailor": read_kapf,
                "Les Miserables": read_lesmis,
##                "Marvel": read_Marvel, 
                "Hollywood music": read_movies,
##                "Network science": read_netscience,
##                "NFL": read_NFL,
##                "Intra-organizational": read_org,
##                "Web of Trust": read_pgp,
                "Sampson's monastery": read_Sampson,
                "Terrorist": read_terrorist}
##                "UC Irvine": read_UC_Irvine

if __name__ == "__main__":
    before = []
    after = []
    for name in networks_dict:
        print(name)
        G0 = read_any(name)
        before.append(nx.transitivity(G0))

        G = make_ConfigMod(G0)
        after.append(nx.transitivity(G))

    for i,name in enumerate(networks_dict.keys()):
        print(name.ljust(15), "\t", before[i], "\t", after[i])

