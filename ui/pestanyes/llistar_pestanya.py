import tkinter as tk
from tkinter import ttk
from logic import llistar_tasques
from utils import calcular_dies_restants
from alert import aplicar_estil_alertes

def crear_layout_llistar(frame, aplicar_estil, colors):
    aplicar_estil(frame)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(1, weight=1)

    # Filtre
    top = ttk.Frame(frame, padding=10)
    top.grid(row=0, column=0, columnspan=2, sticky="ew")

    ttk.Label(top, text="Buscar/Filtrar:", font=("Segoe UI", 10)).pack(side="left", padx=5)
    entrada_filtre = ttk.Entry(top, width=40)
    entrada_filtre.pack(side="left", padx=5)

    # Llista tasques (Treeview)
    esquerra = ttk.Frame(frame, padding=10)
    esquerra.grid(row=1, column=0, sticky="nsw")

    ttk.Label(esquerra, text="Tasques:", font=("Segoe UI", 12, "bold")).pack(anchor="w")

    tree = ttk.Treeview(esquerra, columns=('titol', 'estat', 'data_limit'), show='headings', height=25)
    tree.column('titol', width=200, anchor='w')
    tree.column('estat', width=100, anchor='center')
    tree.column('data_limit', width=120, anchor='center')
    tree.heading('titol', text='Títol')
    tree.heading('estat', text='Estat')
    tree.heading('data_limit', text='Data límit')
    tree.pack(pady=5)

    # Detalls
    dreta = ttk.Frame(frame, padding=10)
    dreta.grid(row=1, column=1, sticky="nsew")

    ttk.Label(dreta, text="Detalls de la tasca", font=("Segoe UI", 12, "bold")).grid(column=0, row=0, sticky="w", pady=(0, 10))

    valors_detall = {}
    camps = ["Títol", "Descripció", "Estat", "Categoria", "Data límit", "Dies restants"]
    for i, camp in enumerate(camps, start=1):
        ttk.Label(dreta, text=f"{camp}:", font=("Segoe UI", 10, "bold")).grid(column=0, row=i, sticky="w", pady=3)
        valor = ttk.Label(dreta, text="", font=("Segoe UI", 10))
        valor.grid(column=1, row=i, sticky="w")
        valors_detall[camp] = valor

    tasques_cache = []

    def carregar_tasques():
        nonlocal tasques_cache
        filtre = entrada_filtre.get().strip().lower()
        tasques = llistar_tasques()
        tree.delete(*tree.get_children())
        tasques_cache = []

        for tasca in tasques:
            id_, titol, descripcio, estat, categoria, data_limit, _ = tasca
            if filtre in titol.lower() or (descripcio and filtre in descripcio.lower()):
                tasques_cache.append(tasca)
                tree.insert('', 'end', values=(titol, estat, data_limit if data_limit else "-"))
        
        aplicar_estil_alertes(tree)

    def mostrar_detalls(event):
        item = tree.focus()
        if not item:
            return
            
        index = tree.index(item)
        tasca = tasques_cache[index]
        id_, titol, descripcio, estat, categoria, data_limit, _ = tasca

        valors_detall["Títol"].config(text=titol)
        valors_detall["Descripció"].config(text=descripcio or "-")
        valors_detall["Estat"].config(text=estat)
        valors_detall["Categoria"].config(text=categoria or "-")
        valors_detall["Data límit"].config(text=data_limit or "-")
        
        dies = calcular_dies_restants(data_limit) if data_limit else None
        valors_detall["Dies restants"].config(text=dies if dies is not None else "-")

    entrada_filtre.bind("<KeyRelease>", lambda e: carregar_tasques())
    tree.bind("<<TreeviewSelect>>", mostrar_detalls)
    carregar_tasques()