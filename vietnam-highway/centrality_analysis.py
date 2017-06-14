# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 13:55:25 2017

@author: giangblackk
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.read_gexf('./R_VN_NHW_Inventory_1_connected_component.gexf')

### betweeness centrality 
import time
start_time = time.time()
# normalized
betweeness_norm_dict = nx.algorithms.betweenness_centrality(G,weight='length')
betweeness_norm_matrix = np.array(betweeness_norm_dict.values())
betweeness_dict = nx.algorithms.betweenness_centrality(G,weight='length',normalized=False)
betweeness_matrix = np.array(betweeness_dict.values())
print("--- %s seconds ---" % (time.time() - start_time))

#import h5py
#h5file = h5py.File('betweeness.h5', 'w')
#h5file.create_dataset('betweeness_norm', data=betweeness_norm_matrix)
#h5file.create_dataset('betweeness', data=betweeness_matrix)
#h5file.close()
#betweeness_matrix_sorted = np.sort(betweeness_matrix)

### reopen betweeness result 
#import h5py
#import numpy as np
#h5f = h5py.File('betweeness.h5','r')
#betweeness_norm = h5f['betweeness_norm'][:]
#betweeness = h5f['betweeness'][:]
#betweeness_norm_cdf = np.cumsum(betweeness_norm)
#betweeness_cdf = np.cumsum(betweeness)

### edge betweeness centrality
import time
start_time = time.time()
# normalized
edge_betweeness_norm_dict = nx.algorithms.edge_betweenness_centrality(G,weight='length')
edge_betweeness_norm_matrix = np.array(edge_betweeness_norm_dict.values())
edge_betweeness_dict = nx.algorithms.edge_betweenness_centrality(G,weight='length',normalized=False)
edge_betweeness_matrix = np.array(edge_betweeness_dict.values())
print("--- %s seconds ---" % (time.time() - start_time))

for key,value in betweeness_dict.iteritems():
    G.node[key]['betweeness'] = float(value)

# nx.write_gexf(G,'./R_VN_NHW_Inventory_1_connected_component_betweeness.gexf')
# hist = np.histogram(betweeness_matrix, range=(np.amin(betweeness_matrix),np.amax(betweeness_matrix)),bins=len(betweeness_matrix)/10)
hist = np.histogram(edge_betweeness_matrix, range=(np.amin(edge_betweeness_matrix),np.amax(edge_betweeness_matrix)),bins=len(edge_betweeness_matrix)/10)
hist = list(hist)
#hist[0] = hist[0]*100
#hist[0] = hist[0]
hist[1] = hist[1][:-1]

fig, ax = plt.subplots()
ax.yaxis.grid(b=True, which='major', color='k', linestyle='--')
ax.set_axisbelow(True)
width = 0.75
rects1 = ax.bar(hist[1], hist[0], width, color='b',edgecolor='k')
ax.set_xlabel(u'Chỉ số trung tâm trung gian cho cạnh')
ax.set_ylabel(u'Số cạnh')
# plt.title('Degree Distribution')
plt.title(u'Thống kê tần xuất chỉ số trung tâm trung gian cho cạnh')
