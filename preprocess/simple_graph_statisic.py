import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
G = nx.read_gexf('./highway_line_singlepart_new.gexf')
hist = nx.degree_histogram(G)
#hist_np = np.array(hist)
#plt.hist(hist_np)
#gaussian_numbers = np.random.randn(1000)
#plt.hist(gaussian_numbers)
#plt.hist(np.histogram(hist_np))
#plt.hist([1,2,3,4,5,6,6])
# degree_sequence = list(nx.degree(G).values())
degree_sequence=sorted(nx.degree(G).values(),reverse=True)
plt.hist(degree_sequence, range=(0,6), normed=True, facecolor='green')
plt.xlabel('Degree')
plt.ylabel('Number of Node')
plt.grid(True)
for node in G.nodes_iter():
    if len(G.neighbors(node)) > 10:
        print(node)