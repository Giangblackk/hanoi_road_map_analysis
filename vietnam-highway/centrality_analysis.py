#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 16:51:21 2017

@author: giangblackk
"""

import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_gexf('./R_VN_NHW_Inventory.gexf')
# x = nx.betweenness_centrality(G)
degree_sequence=sorted(nx.degree(G).values(),reverse=True)
plt.hist(degree_sequence, normed=True, facecolor='green')
plt.xlabel('Degree')
plt.ylabel('Percent')
plt.grid(True)
