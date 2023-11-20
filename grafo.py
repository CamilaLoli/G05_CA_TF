import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

from graph import *

# Leer el archivo CSV y crear un diccionario de nodos
data = pd.read_csv('CrearGrafo/TrabajoFinalSergio.csv', delimiter=';')

# Rellenar filas con valores faltantes con ceros
data.fillna(0, inplace=True)

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = []

    def add_node(self, node_id, attrs):
        self.nodes[node_id] = attrs

    def add_edge(self, node1_id, node2_id, weight):
        self.edges.append((node1_id, node2_id, weight))

    def get_edge_data(self, node1_id, node2_id):
        for edge in self.edges:
            if (edge[0] == node1_id and edge[1] == node2_id) or (edge[0] == node2_id and edge[1] == node1_id):
                return {'weight': edge[2]}
        return None

    def edges(self):
        return self.edges

# Crear un diccionario de nodos
nodes = {}
for index, row in data.iterrows():
    node_id = str(index+1) 

    # Se utiliza el índice del dataframe como id del nodo
    node_attrs = {
        'title': row['title'],
        'subtitle': row['subtitle'],
        'categories': row['categories'],
        'average_rating': row['average_rating']
    }
    
    # Rellenar campos faltantes con ceros
    for key in node_attrs:
        if node_attrs[key] == '':
            node_attrs[key] = 0
    
    nodes[node_id] = node_attrs
    
nodes[1826] = node_attrs

# Preprocesamiento de texto


categories = [node['categories'] if isinstance(node['categories'], str) else '' for node in nodes.values()]
vectorizer = TfidfVectorizer()

category_features = vectorizer.fit_transform(categories)
titles = [node['title'] for node in nodes.values()]
title_features = vectorizer.fit_transform(titles)
# Cálculo de la similitud del coseno
title_similarity = cosine_similarity(title_features)
category_similarity = cosine_similarity(category_features)

# Creación de las aristas
edges = []
similarity2=0

Noconnected_nodes = nodes

for i, node1_id in enumerate(Noconnected_nodes.keys()):
    for j, node2_id in enumerate(list(Noconnected_nodes.keys())[i+1:]):
        title_sim = title_similarity[int(node1_id), int(node2_id)]
        category_sim = category_similarity[int(node1_id), int(node2_id)]
        similarity = (abs(title_sim) * 0.5) + (abs(category_sim) * 0.3) + (abs(nodes[node1_id]['average_rating'] - nodes[node2_id]['average_rating']) * 0.2)

        edges.append((node2_id, node1_id, similarity))

# Ordenar las aristas por peso de manera inversa
edges.sort(key=lambda x: x[2], reverse=True)

# Crear un grafo vacío


# Eliminar bucles utilizando el algoritmo de Kruskal
class Kruskal:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        self.parent = {}
        self.rank = {}
        self.mst_edges = []

    def find(self, node):
        if self.parent[node] == node:
            return node
        return self.find(self.parent[node])

    def union(self, node1, node2):
        root1 = self.find(node1)
        root2 = self.find(node2)

        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2
        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1
        else:
            self.parent[root2] = root1
            self.rank[root1] += 1

    def run(self):
        for node in self.nodes:
            self.parent[node] = node
            self.rank[node] = 0

        for edge in self.edges:
            node1, node2, weight = edge

            if self.find(node1) != self.find(node2):
                self.mst_edges.append(edge)
                self.union(node1, node2)

        mst = Graph()

        for edge in reversed(self.mst_edges):  # Iterar en orden inverso para obtener el MST de mayor peso
            node1, node2, weight = edge
            mst.add_edge(node1, node2, weight=weight)

        return mst

# Crear objeto Kruskal y ejecutar el algoritmo
kruskal = Kruskal(nodes.keys(), edges)
mst = kruskal.run()

# Escribir los datos del grafo en un nuevo archivo CSV
with open('grafos.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['source', 'target', 'weight'])
    for edge in mst.edges:
        writer.writerow([edge[0], edge[1], mst.get_edge_data(edge[0], edge[1])['weight']])
