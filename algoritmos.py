import json
from graph import build_graph_from_json

graph = build_graph_from_json('TF2.json')
def dfs_by_category(graph, node, category, visited):
    visited.add(node)
    print("Visitando nodo:", node, "de categoría:", category)
    for neighbor in graph.get_neighbours(node):
        if neighbor not in visited:
            node_data = graph.get_vertex(neighbor)
            if node_data and 'attributes' in node_data:
                attributes = node_data['attributes']
                if 'categories' in attributes and attributes['categories'] == category:
                    dfs_by_category(graph, neighbor, category, visited)

# Especifica la categoría por la que deseas buscar
category_to_search = "History"

# Verifica si los nodos tienen la categoría "History" asignada

# Encuentra un nodo de inicio que tenga la categoría deseada
start_nodes = graph.get_vertex(1027)

for start_node in graph.get_vertices():
    visited_nodes = set()
    if start_node not in visited_nodes:
        dfs_by_category(graph, start_node, category_to_search, visited_nodes)

if start_nodes:
    visited_nodes = set()
    print(f"Búsqueda en profundidad (DFS) basada en la categoría '{category_to_search}':")
    for start_node in start_nodes:
        dfs_by_category(graph, start_node, category_to_search, visited_nodes)
else:
    print(f"No se encontraron nodos con la categoría '{category_to_search}'.")


