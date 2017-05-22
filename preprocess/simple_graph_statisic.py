import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
G = nx.read_gexf('/home/giangblackk/Dropbox/DATN/hanoi_road_map_analysis/preprocess/graphdata/highway_line_singlepart_new_length.gexf')
G2 = nx.Graph(G)

# histogram
hist = nx.degree_histogram(G)
neighbor_sequence = [len(G.neighbors(node)) for node in G.nodes_iter()]
plt.hist(neighbor_sequence, normed=True, facecolor='green')
plt.xlabel('Number of Neighbor')
plt.ylabel('Percent')
plt.grid(True)

# degree_sequence = list(nx.degree(G).values())
degree_sequence=sorted(nx.degree(G2).values(),reverse=True)
plt.hist(degree_sequence, normed=True, facecolor='green')
plt.xlabel('Degree')
plt.ylabel('Percent')
plt.grid(True)

# check if node with no neigbors

#check_1
for node in G.nodes_iter():
    if len(G2.neighbors(node))==0:
        print(node)
# check_2
for node in G.nodes_iter():
    if G.in_degree()[node] == 0 and G.out_degree()[node] == 0:
        print(G.node[node])
