#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 16:51:21 2017

@author: giangblackk
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# G = nx.read_gexf('./R_VN_NHW_Inventory.gexf')
G = nx.read_gexf('./R_VN_NHW_Inventory_1_connected_component.gexf')
# x = nx.betweenness_centrality(G)
#degree_sequence=sorted(nx.degree(G).values(),reverse=True)
#plt.hist(degree_sequence, normed=True, facecolor='green')
#plt.xlabel('Degree')
#plt.ylabel('Percent')
#plt.grid(True)
neighbor_sequence=sorted(nx.degree(G).values(),reverse=True)
neighbor_sequence_2 = []
for i in neighbor_sequence:
    if i != 2:
        neighbor_sequence_2.append(i)
hist = np.histogram(neighbor_sequence_2, range=(1,7),bins=6,normed=True)
# hist = np.histogram(neighbor_sequence, range=(1,7),bins=6)
hist = list(hist)
#hist[0] = hist[0]*100
#hist[0] = hist[0]
hist[1] = hist[1][:-1]

fig, ax = plt.subplots()
ax.yaxis.grid(b=True, which='major', color='k', linestyle='--')
ax.set_axisbelow(True)
width = 0.75
rects1 = ax.bar(hist[1], hist[0], width, color='b',edgecolor='k')
ax.set_xlabel(u'Số bậc')
ax.set_ylabel(u'Phần trăm (%)')
# plt.title('Degree Distribution')
plt.title(u'Phân phối bậc')
def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                '%.2f' % round(height,2),
                #'%d' % height,
                ha='center', va='bottom',fontweight='bold')

autolabel(rects1)
