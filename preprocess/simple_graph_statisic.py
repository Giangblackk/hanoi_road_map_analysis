import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
G = nx.read_gexf('/home/giangblackk/Dropbox/DATN/hanoi_road_map_analysis/preprocess/graphdata/highway_line_singlepart_new_length.gexf')
hist = nx.degree_histogram(G)
neighbor_sequence = [len(G.neighbors(node)) for node in G.nodes_iter()]
# degree_sequence = list(nx.degree(G).values())
degree_sequence=sorted(nx.degree(G).values(),reverse=True)
plt.hist(degree_sequence, normed=True, facecolor='green')
plt.xlabel('Degree')
plt.ylabel('Percent')
plt.grid(True)
#plt.hist(neighbor_sequence, range= (0,5),normed=True, facecolor='green')
#plt.xlabel('Number of Neighbor')
#plt.ylabel('Percent')
#plt.grid(True)
#for node in G.nodes_iter():
#    if len(G.neighbors(node)) ==5:
#        print(G.node[node])