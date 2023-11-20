import json

# Cargar el grafo desde el archivo JSON
with open('myproject\TFVerd.json', 'r', encoding='utf-8') as json_file:
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

# Verifica si los nodos tienen la categoría "History" asignada
categorias = set()  # Define the categorias set

for node in data['nodes']:
    for atributos in node['attributes']:
        if atributos == "categories":
            categorias.add(node['attributes']['categories'])

with open('myproject\Datos\categorias.txt', 'w', encoding='utf-8') as file:
    for categoria in categorias:
        file.write(categoria + '\n')
