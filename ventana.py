import tkinter as tk
from tkinter.font import Font as ft
from graph import *

def dfs_by_category(graph, node, category, visited):
    visited.add(node)
    if 'categories' in graph.graph_dict[node] and graph.graph_dict[node]['categories'] == category:
        result_listbox.insert(tk.END, f"Nodo {node}: {category}")

graph = build_graph_from_json('TF2.json')

def buscar_recomendaciones():
    # Obtiene la categoría escogida por el usuario
    categoria = titulo_libro_entry.get()
    start_nodes = [vertex for vertex, attributes in graph.graph_dict.items() if 'categories' in attributes and attributes['categories'] == categoria]
    result_listbox.delete(0, tk.END) # Evita que se mantenga el resultado que dio anteriormente
    visited_nodes = set()
    for start_node in start_nodes:
        dfs_by_category(graph, start_node, categoria, visited_nodes)

ventana = tk.Tk()
ventana.title("Pantalla Principal")
ventana.geometry("600x400")  
ventana.iconbitmap("books.ico")

titulo_font = ft(family="Verdana", size=15, weight="bold")

titulo_label = tk.Label(ventana, text="BiblioCat", font=titulo_font)
titulo_label.pack(pady=10)


titulo_libro_entry = tk.Entry(ventana, width=40)
titulo_libro_entry.pack(pady=10)


btn_font = ft(family="Verdana", size=12, weight="normal")
buscar_button = tk.Button(ventana, text="Buscar", command=buscar_recomendaciones, font=btn_font)
buscar_button.pack()

rst_font = ft(family="Verdana", size=12, weight="bold")
resultado_label = tk.Label(ventana, text="Recomendaciones", font=rst_font)
resultado_label.pack(pady=10)
result_listbox = tk.Listbox(ventana, width=60, height=10)
result_listbox.pack(pady=10)
ventana.mainloop()
