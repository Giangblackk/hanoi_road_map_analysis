#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:31:38 2017

@author: giangblackk
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.read_gexf('/home/giangblackk/Dropbox/DATN/hanoi_road_map_analysis/preprocess/graphdata/highway_line_singlepart_new_length.gexf')

### betweeness centrality 
import time
start_time = time.time()
# normalized
betweeness_norm_dict = nx.algorithms.betweenness_centrality(G,weight='length')
betweeness_norm_matrix = np.array(betweeness_norm_dict.values())
betweeness_dict = nx.algorithms.betweenness_centrality(G,weight='length',normalized=False)
betweeness_matrix = np.array(betweeness_dict.values())
print("--- %s seconds ---" % (time.time() - start_time))
# np.save('./betweeness_norm_matrix.npy', betweeness_norm_matrix)
# np.save('./betweeness_matrix.npy', betweeness_matrix)

import h5py
h5file = h5py.File('betweeness.h5', 'w')
h5file.create_dataset('betweeness_norm', data=betweeness_norm_matrix)
h5file.create_dataset('betweeness', data=betweeness_matrix)
h5file.close()

### reopen betweeness result 
import h5py
import numpy as np
h5f = h5py.File('betweeness.h5','r')
betweeness_norm = h5f['betweeness_norm'][:]
betweeness = h5f['betweeness'][:]
betweeness_norm_cdf = np.cumsum(betweeness_norm)
betweeness_cdf = np.cumsum(betweeness)


### edge betweeness centrality
import time
start_time = time.time()
# normalized
edge_betweeness_norm_dict = nx.algorithms.edge_betweenness_centrality(G,weight='length')
edge_betweeness_norm_matrix = np.array(edge_betweeness_norm_dict.values())
edge_betweeness_dict = nx.algorithms.edge_betweenness_centrality(G,weight='length',normalized=False)
edge_betweeness_matrix = np.array(edge_betweeness_dict.values())
print("--- %s seconds ---" % (time.time() - start_time))

edge_betweeness_norm_cdf = np.cumsum(edge_betweeness_norm_matrix)
edge_betweeness_cdf = np.cumsum(edge_betweeness_matrix)

hist = np.histogram(betweeness, bins=100,normed=True)
