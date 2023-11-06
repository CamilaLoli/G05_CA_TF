import json
import networkx as nx
from matplotlib import pyplot as plt

with open('TF2.json', 'r', encoding='utf-8') as json_file:
    json_str = json_file.read()

data = json.loads(json_str)

nodes = data['nodes']
edges = data['edges']

G = nx.Graph()

for node in nodes:
    G.add_node(node['id'], **node)

for edge in edges:
    G.add_edge(edge['source'], edge['target'], **edge)

pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=False, node_size=50, node_color='skyblue', font_size=8, font_color='black', font_weight='bold', edge_color='gray')
plt.title("Visualización de Grafo")
plt.show()