#!/usr/bin/env python
# -*- coding: utf-8 -*-

# read-edgelist.py
# Jim Bagrow
# Last Modified: 2019-10-15

import sys, os
import csv
import networkx as nx


def digraph_from_edges(edges, name=None):
    graph = nx.DiGraph()
    if name is not None:
        graph.name = name
    graph.add_edges_from(edges)
    return graph


if __name__ == '__main__':
    
    d_edges_all = set()
    with open('emails__from_to_mid.csv') as csvfile:
        reader = csv.reader(csvfile)
        for fr,to,mid in reader:
            d_edges_all.add( (fr,to) )
    
    d_edges = [(i,j) for i,j in d_edges_all if i != j] # no self-loops
    d_edges_enron = [ (i,j) for i,j in d_edges if "@enron.com" in i and "@enron.com" in j]
    
    G_all   = digraph_from_edges(d_edges_all,   name='Enron emails (all edges)'           )
    G       = digraph_from_edges(d_edges,       name='Enron emails (no self-loops)'       )
    G_enron = digraph_from_edges(d_edges_enron, name='Enron emails (no SLs, enron addresses only)')
    
    for g in [G_all, G, G_enron]:
        print(nx.info(g))
        print()

    nx.write_edgelist(G_enron, "enron-edgelist.txt", delimiter=" ", data=False)
    
    # conclusion: let's use the enron-only messages, 10k nodes and 66k edges...
"""
Name: Enron emails (all edges)
Type: DiGraph
Number of nodes: 44447
Number of edges: 116190
Average in degree:   2.6141
Average out degree:   2.6141
Name: Enron emails (no self-loops)
Type: DiGraph
Number of nodes: 44146
Number of edges: 114940
Average in degree:   2.6036
Average out degree:   2.6036
Name: Enron emails (no SLs, enron addresses only)
Type: DiGraph
Number of nodes: 10773
Number of edges: 66393
Average in degree:   6.1629
Average out degree:   6.1629
"""
