import tkinter as tk
from tkinter.font import Font as ft

def buscar_recomendaciones():
    resultado_label.config(text="Recomendaciones")

ventana = tk.Tk()
ventana.title("Pantalla Principal")
ventana.geometry("600x400")  
ventana.iconbitmap("books.ico")

# Para titulo
titulo_font = ft(family="Verdana", size=15, weight="bold")

titulo_label = tk.Label(ventana, text="Titulo de la pagina", font=titulo_font)
titulo_label.pack(pady=10)

# Entrada de búsqueda
titulo_libro_entry = tk.Entry(ventana, width=40)
titulo_libro_entry.pack(pady=10)

# Botones
btn_font = ft(family="Verdana", size=12, weight= "normal")
buscar_button = tk.Button(ventana, text="Buscar", command=buscar_recomendaciones, font=btn_font)
buscar_button.pack()

# Resultado ─Lista─
rst_font = ft(family="Verdana", size = 12, weight="bold")
resultado_label = tk.Label(ventana, text="Recomendaciones", font=rst_font)
resultado_label.pack(pady=10)

ventana.mainloop()