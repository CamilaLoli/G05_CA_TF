from flask import Flask, request, render_template
import json
import os
from BusquedaTitulo import *
from graph import *

graph = build_graph_from_json('TFVerd.json')
# Cargar el grafo desde el archivo JSON
categorias_file = os.path.join( 'Datos', 'categorias.txt')
with open(categorias_file, 'r', encoding='utf-8') as categorias_file:
    categorias = categorias_file.read().splitlines()
with open('TFVerd.json', 'r', encoding='utf-8') as json_file:
    json_str = json_file.read()

data = json.loads(json_str)


# Agregar aristas desde la lista de aristas

# Define una función para la búsqueda en profundidad (DFS) basada en categorías
def dfs_by_category(graph, node, category, visited):
    visited.add(node)
    for neighbor, attributes in graph.graph_dict.items():
        if neighbor not in visited and 'categories' in attributes and attributes['categories'] == category:
            dfs_by_category(graph, neighbor, category, visited)


def dfs(graph, node, visited, depth_limit):
    if depth_limit <= 0:
        return
    visited.add(node)

    for neighbor,attributes in graph.graph_dict.items():
        if neighbor not in visited and 'categories' in attributes:
            dfs(graph, neighbor, visited, depth_limit - 1)
# Define una función para la búsqueda por nombre y tengo una funcion llamada def encontrar_palabra_similar(palabra_clave) y palabra clave es el name y este realize una busqueda de profundidad empezando de ese nodo encontrado por la funcion y me devuelve todos los nodos recorridos pero que se muestren pantalla
def search_by_name(graph, name, year, year_filter, category=None):
    # Buscar el nodo con el nombre más similar al nombre de búsqueda
    node = encontrar_nodo_similar(name)

    # Realizar una búsqueda en profundidad (DFS) desde el nodo encontrado
    visited = set()
    if category is None:
        dfs(graph, node['id'], visited, 100)
    else:
        dfs_by_category(graph, node['id'], category, visited)

    result = []

    if visited:
        for node_id in visited:
            attributes = graph.get_vertex(node_id)
            if 'title' in attributes and 'num_pages' in attributes and 'categories' in attributes and 'average_rating' in attributes and 'published_year' in attributes:
                año = int(attributes['published_year'])
                if year_filter == 'mayor' and año > year:
                    node_info = {
                        'title': attributes['title'],
                        'num_pages': attributes['num_pages'],
                        'categories': attributes['categories'],
                        'average_rating': attributes['average_rating'],
                        'published_year': attributes['published_year'],
                        'image': 'https://example.com/image.jpg'  # Reemplaza con la URL de la imagen correspondiente
                    }
                    result.append(node_info)
                elif year_filter == 'menor' and año < year:
                    node_info = {
                        'title': attributes['title'],
                        'num_pages': attributes['num_pages'],
                        'categories': attributes['categories'],
                        'average_rating': attributes['average_rating'],
                        'published_year': attributes['published_year'],
                        'image': 'https://example.com/image.jpg'  # Reemplaza con la URL de la imagen correspondiente
                    }
                    result.append(node_info)

    return result
  


# Crear una aplicación Flask
app = Flask(__name__)

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html', categories=categorias)

# Ruta para buscar nodos por categoría
@app.route('/search', methods=['POST'])
def search():
    # Obtener los parámetros de búsqueda
    category_to_search = request.form['category']
    año_to_search = int(request.form['year'])
    filtro_year=request.form['year_filter']
    print("Category to search: ", category_to_search)

    if category_to_search == "N/A":
        # Realiza la búsqueda solo por categoría
        result = search_by_name(graph, category_to_search, año_to_search, filtro_year)
    else:
        # Realiza la búsqueda por categoría y nombre
        name_to_search = request.form['name']
        result = search_by_name(graph, name_to_search, año_to_search, filtro_year, category_to_search)

    return render_template('results.html', result=result)


# Ruta para buscar nodos por nombre
@app.route('/search_by_name', methods=['POST'])
def search_by_name_route():
    # Obtener los parámetros de búsqueda
    name_to_search = request.form['name']
    category_to_search = request.form['category']
    año_to_search = request.form['year']
    filtro_year = request.form['year_filter']
    print("Category to search: ", category_to_search)

    try:
        año_to_search = int(año_to_search)
    except ValueError:
        año_to_search = 0

    if category_to_search == "N/A":
        # Realiza la búsqueda solo por nombre
        result = search_by_name(graph, name_to_search, año_to_search, filtro_year)
    else:
        # Realiza la búsqueda por nombre y categoría
        result = search_by_name(graph, name_to_search, año_to_search, filtro_year, category_to_search)

    if año_to_search == 0:
        filtro_year = "mayor"

    return render_template('results.html', result=result)


# Ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run()