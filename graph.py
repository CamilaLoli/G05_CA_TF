import json
class Graph:
    def __init__(self):
        self.graph_dict = {}

    def add_vertex(self, vertex_id, attributes):
        if vertex_id not in self.graph_dict:
            self.graph_dict[vertex_id] = attributes

    def add_edge(self, vertex1, vertex2, weight):
        if vertex1 in self.graph_dict and vertex2 in self.graph_dict:
            if 'edges' not in self.graph_dict[vertex1]:
                self.graph_dict[vertex1]['edges'] = {}
            if 'edges' not in self.graph_dict[vertex2]:
                self.graph_dict[vertex2]['edges'] = {}
            self.graph_dict[vertex1]['edges'][vertex2] = weight
            self.graph_dict[vertex2]['edges'][vertex1] = weight  # Debido a que es un grafo no dirigido

    def get_vertices(self):
        return list(self.graph_dict.keys())
    def get_vertex(self, vertex_id):
        if vertex_id in self.graph_dict:
            return self.graph_dict[vertex_id]
        else:
            return None
    def get_neighbours(self, vertex):
        return self.graph_dict[vertex]

def build_graph_from_json(json_file):

    with open(json_file, 'r', encoding='utf-8') as json_file:
        json_str = json_file.read()

    data = json.loads(json_str)


    graph = Graph()

    for node in data['nodes']:
        vertex_id = node['id']
        attributes = node['attributes']
        graph.add_vertex(vertex_id, attributes)


    for edge in data['edges']:
        source = edge['source']
        target = edge['target']
        weight = edge['size']  

        graph.add_edge(source, target, weight)

    return graph




