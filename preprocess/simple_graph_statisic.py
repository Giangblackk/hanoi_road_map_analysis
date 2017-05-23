import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.read_gexf('/home/giangblackk/Dropbox/DATN/hanoi_road_map_analysis/preprocess/graphdata/highway_line_singlepart_new_length.gexf')
G2 = nx.Graph(G)

# histogram
# hist = nx.degree_histogram(G)
neighbor_sequence = [len(G2.neighbors(node)) for node in G.nodes_iter()]
#plt.hist(neighbor_sequence, facecolor='green')
#plt.xlabel('Number of Neighbor')
#plt.ylabel('Percent')
#plt.grid(True)

"""
# degree_sequence = list(nx.degree(G).values())
degree_sequence=sorted(nx.degree(G2).values(),reverse=True)
plt.hist(degree_sequence, normed=True, facecolor='green')
plt.xlabel('Degree')
plt.ylabel('Percent')
plt.grid(True)
"""
# check if node with no neigbors

"""
#check_1
for node in G.nodes_iter():
    if len(G2.neighbors(node))==0:
        print(node)
# check_2
for node in G.nodes_iter():
    if G.in_degree()[node] == 0 and G.out_degree()[node] == 0:
        print(node)
"""
hist = np.histogram(neighbor_sequence, range=(1,7),bins=6,normed=True)
# hist = np.histogram(neighbor_sequence, range=(1,7),bins=6)
hist = list(hist)
hist[0] = hist[0]*100
hist[0] = hist[0]
hist[1] = hist[1][:-1]

fig, ax = plt.subplots()
ax.yaxis.grid(b=True, which='major', color='k', linestyle='--')
ax.set_axisbelow(True)
width = 0.75
rects1 = ax.bar(hist[1], hist[0], width, color='b',edgecolor='k')
ax.set_xlabel('Degree')
ax.set_ylabel('Percent')
plt.title('Degree Distribution')
def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.005*height,
                '%d' % int(height),
                ha='center', va='bottom',fontweight='bold')

autolabel(rects1)
