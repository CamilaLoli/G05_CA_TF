import tkinter as tk
from tkinter.font import Font as ft
from graph import build_graph_from_json

graph = build_graph_from_json('TF2.json')

def dfs_by_category(graph, node, category, visited):
    visited.add(node)
    if 'categories' in graph.graph_dict[node] and graph.graph_dict[node]['categories'] == category:
        result_listbox.insert(tk.END, f"Nodo {node}: {category}")

# Especifica la categoría por la que deseas buscar
category_to_search = "History"

# Encuentra un nodo de inicio que tenga la categoría deseada
start_nodes = [vertex for vertex, attributes in graph.graph_dict.items() if 'categories' in attributes and attributes['categories'] == category_to_search]

def buscar_recomendaciones():
    result_listbox.delete(0, tk.END)  # Limpiar resultados anteriores
    visited_nodes = set()
    for start_node in start_nodes:
        dfs_by_category(graph, start_node, category_to_search, visited_nodes)

ventana = tk.Tk()
ventana.title("Búsqueda de Categorías")
ventana.geometry("600x400")
ventana.iconbitmap("books.ico")

titulo_font = ft(family="Verdana", size=15, weight="bold")
titulo_label = tk.Label(ventana, text="Búsqueda de Categorías", font=titulo_font)
titulo_label.pack(pady=10)

titulo_libro_entry = tk.Entry(ventana, width=40)
titulo_libro_entry.pack(pady=10)

btn_font = ft(family="Verdana", size=12, weight="normal")
buscar_button = tk.Button(ventana, text="Buscar", command=buscar_recomendaciones, font=btn_font)
buscar_button.pack()

result_listbox = tk.Listbox(ventana, width=60, height=10)
result_listbox.pack(pady=10)

ventana.mainloop()

ventana.mainloop()
