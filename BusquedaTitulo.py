import json

from Levenshtein import ratio
import numpy as np

nodes = {}

with open('TFVerd.json', 'r', encoding='utf-8') as json_file:
    json_str = json_file.read()

data = json.loads(json_str)

# Crear un diccionario para representar el grafo
graph = {}

# Agregar aristas desde la lista de aristas
for edge in data['edges']:
    source = edge['source']
    target = edge['target']

    if source not in graph:
        graph[source] = []
    graph[source].append(target)

    if target not in graph:
        graph[target] = []
    graph[target].append(source)


titles = []  # Define the 'titles' list

for node in data['nodes']:
    if node and 'attributes' in node and 'title' in node['attributes']:
        titles.append(node['attributes']['title'])

def encontrar_nodo_similar(palabra_clave):
    # Calcular la similitud de Levenshtein entre la palabra clave y los títulos de los nodos
    similitudes = [ratio(palabra_clave, titulo) for titulo in titles]

    # Encontrar el índice del nodo con la mayor similitud a la palabra clave
    indice_max_similitud = np.argmax(similitudes)
    nodo_max_similitud = data['nodes'][indice_max_similitud]

    # Devolver el nodo con la mayor similitud
    return nodo_max_similitud
