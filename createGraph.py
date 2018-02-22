import csv

with open('passengers-location_day1.csv', 'r') as csvfile:
    passenger_file = csv.reader(csvfile, delimiter=';', quotechar='|')
    data = []
    for row in passenger_file:
        data.append(row)


legend = data[1]
data = data[2:]
travel_directions = {}
for row in data:
    direct_dict = {legend[i]:int(row[i]) for i in range(2, len(row))}
    if row[1] in travel_directions:
        travel_directions[row[1]] = {key: travel_directions[row[1]].get(key, 0) + direct_dict.get(key, 0) for key in set(travel_directions[row[1]]) | set(direct_dict)}
    else:
        travel_directions[row[1]] = direct_dict


locations = list(travel_directions.keys())

loc_table = [0]*(len(locations)+1)
loc_table = [[0 for i in range(len(loc_table))] for i in range(len(loc_table))]
for i in range(1,len(locations)+1):
    loc_table[0][i] = locations[i-1]
    loc_table[i][0] = locations[i-1]

for i in range(1,len(locations)+1):
    for j in range(1,len(locations)+1):
        loc_table[i][j] = travel_directions[locations[i-1]][locations[j-1]]


import plotly.offline as py
import plotly.graph_objs as go

trace = go.Table(
    cells=dict(values=loc_table))

data = [trace]
py.iplot(data,image='png')


xs = [27, 11, 31, 22, 21, 11, 25, 11, 26, 25, 17, 4, 31, 17, 19, 35, 6, 10, 38, 14, 23, 24, 25, 15]
ys = [7, 4, 30, 21, 18, 18, 30, 9, 24, 18, 14, 12, 13, 11, 3, 10, 26, 13, 11, 1, 16, 13, 11, 4]

loc_pos = {}
i=0
for loc in travel_directions.keys():
    loc_pos[loc] = [xs[i]*10, ys[i]*10]
    i+=1

import networkx as nx
import pylab as plt

G = nx.Graph()

for node in travel_directions.keys():
    G.add_node(node, name=node)
    for next_node in travel_directions[node].keys():
        if next_node not in G:
            G.add_node(next_node, name=next_node)
        if G.has_edge(node, next_node):
            G[node][next_node]['weight'] += travel_directions[node][next_node]
        else:
            G.add_edge(node, next_node,weight=travel_directions[node][next_node])


edges = [x for x in G.edges()]
weights = [G[u][v]['weight'] for u,v in edges]
weights_s = [G[u][v]['weight']/60 for u,v in edges]

new_edges = [(u,v) for (u,v) in G.edges() if G[u][v]['weight'] > sorted(weights)[-15]]

for edge in edges:
    if edge not in new_edges:
        G.remove_edge(edge[0],edge[1])

edges = [x for x in G.edges()]
weights = [G[u][v]['weight'] for u,v in edges]
weights_s = [G[u][v]['weight']/60 for u,v in edges]
maxWeight=float(max(weights))
minWeight=float(min(weights))
a_netw_colors = [plt.cm.Blues((weight-(minWeight-30))/(maxWeight-(minWeight-30))) for weight in weights]
# plt.ioff()
colors_unscaled=[tuple(map(lambda x: maxWeight*x, y)) for y in a_netw_colors]
heatmap = plt.pcolor(colors_unscaled,cmap=plt.cm.Blues)
# plt.ion()

fig,axes = plt.subplots()

nx.draw_networkx(G,pos=loc_pos, width=weights_s, edge_color=a_netw_colors, with_labels=True)


axes.get_xaxis().set_visible(False)
axes.get_yaxis().set_visible(False)

cbar = plt.colorbar(heatmap)
cbar.ax.set_ylabel('Number of Passengers per Day',labelpad=15,rotation=270)
plt.show()
