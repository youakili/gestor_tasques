import tkinter as tk
from tkinter import ttk

# Paleta de colors
COLOR_FONS = "#F5F7FA"
COLOR_MARCS = "#FFFFFF"
COLOR_TEXT = "#333333"
COLOR_ACCENT = "#3B82F6"  
COLOR_BOTO = "#2563EB"    
COLOR_BOTO_TEXT = "#FFFFFF"

# Estil global
def aplicar_estil(widget):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background=COLOR_FONS)
    style.configure("TLabel", background=COLOR_FONS, foreground=COLOR_TEXT, font=("Segoe UI", 10))
    style.configure("TButton", background=COLOR_BOTO, foreground=COLOR_BOTO_TEXT, font=("Segoe UI", 10), padding=6)
    style.map("TButton", background=[("active", "#1D4ED8")])
    style.configure("TNotebook", background=COLOR_FONS, tabposition='n')
    style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 6])
    style.map("TNotebook.Tab", background=[("selected", "#E0ECFF")], foreground=[("selected", "#000")])
    style.configure("TCombobox", padding=5)


def estil_entry(canvas, parent, width=300, height=30):

    #Simula un Entry arrodonit utilitzant un canvas
    
    rounded_box = canvas.create_rectangle(5, 5, width, height, outline="#ccc", width=1, fill="white")
    entry = tk.Entry(parent, bd=0, font=("Segoe UI", 10), relief="flat", highlightthickness=0)
    canvas.create_window(width // 2, height // 2, window=entry)
    return entry

#Crear la pestanya de afegir tasques
def crear_layout_afegir(frame):
    aplicar_estil(frame)
    frame.columnconfigure(0, weight=1)
    contenidor = ttk.Frame(frame, padding=30, style="TFrame")
    contenidor.grid(column=0, row=0, sticky="nsew")

    ttk.Label(contenidor, text="Afegir una nova tasca", font=("Segoe UI", 14, "bold")).grid(column=0, row=0, columnspan=2, pady=(0, 20))

    ttk.Label(contenidor, text="Títol:").grid(column=0, row=1, sticky="w")
    ttk.Entry(contenidor, width=50).grid(column=1, row=1, pady=5)

    ttk.Label(contenidor, text="Descripció:").grid(column=0, row=2, sticky="nw", pady=(10, 0))
    text = tk.Text(contenidor, width=50, height=5, bg="white", bd=0, highlightbackground="#ccc", relief="flat", font=("Segoe UI", 10))
    text.grid(column=1, row=2, pady=5)

    ttk.Label(contenidor, text="Estat inicial:").grid(column=0, row=3, sticky="w", pady=(10, 0))
    estat_menu = ttk.Combobox(contenidor, values=["Pendent", "Completada"], state="readonly", width=47)
    estat_menu.set("Pendent")
    estat_menu.grid(column=1, row=3, pady=5)

    ttk.Label(contenidor, text="Categoria:").grid(column=0, row=4, sticky="w", pady=(10, 0))
    ttk.Entry(contenidor, width=50).grid(column=1, row=4, pady=5)

    ttk.Label(contenidor, text="Data límit (AAAA-MM-DD):").grid(column=0, row=5, sticky="w", pady=(10, 0))
    ttk.Entry(contenidor, width=50).grid(column=1, row=5, pady=5)

    ttk.Button(contenidor, text="Afegir Tasca").grid(column=0, row=6, columnspan=2, pady=20)

#Crear la pestanya de llistar tasques
def crear_layout_llistar(frame):
    aplicar_estil(frame)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(1, weight=1)

    top = ttk.Frame(frame, padding=10)
    top.grid(row=0, column=0, columnspan=2, sticky="ew")

    ttk.Label(top, text="Buscar/Filtrar:", font=("Segoe UI", 10)).pack(side="left", padx=5)
    ttk.Entry(top, width=40).pack(side="left", padx=5)

    esquerra = ttk.Frame(frame, padding=10)
    esquerra.grid(row=1, column=0, sticky="nsw")

    ttk.Label(esquerra, text="Tasques:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
    llista = tk.Listbox(esquerra, width=40, height=25, bd=0, highlightthickness=1, highlightbackground="#ccc", relief="flat", font=("Segoe UI", 10))
    llista.pack(pady=5)

    dreta = ttk.Frame(frame, padding=10)
    dreta.grid(row=1, column=1, sticky="nsew")

    ttk.Label(dreta, text="Detalls de la tasca", font=("Segoe UI", 12, "bold")).grid(column=0, row=0, sticky="w", pady=(0, 10))

    camps = ["Títol", "Descripció", "Estat", "Categoria", "Data límit", "Dies restants"]
    for i, camp in enumerate(camps, start=1):
        ttk.Label(dreta, text=f"{camp}:", font=("Segoe UI", 10)).grid(column=0, row=i, sticky="w", pady=3)

#Crear la pestanya de modificar o/i eliminar tasques
def crear_layout_modificar(frame):
    aplicar_estil(frame)
    frame.columnconfigure(1, weight=1)

    esquerra = ttk.Frame(frame, padding=10)
    esquerra.grid(row=0, column=0, sticky="nsw")

    ttk.Label(esquerra, text="Tasques:", font=("Segoe UI", 12, "bold")).pack(anchor="w")
    tk.Listbox(esquerra, width=40, height=25, bd=0, highlightthickness=1, highlightbackground="#ccc", relief="flat", font=("Segoe UI", 10)).pack()

    dreta = ttk.Frame(frame, padding=20)
    dreta.grid(row=0, column=1, sticky="nsew")

    ttk.Label(dreta, text="Modificar / Eliminar", font=("Segoe UI", 14, "bold")).grid(column=0, row=0, columnspan=2, pady=10)

    ttk.Label(dreta, text="Títol:").grid(column=0, row=1, sticky="w")
    ttk.Entry(dreta, width=50).grid(column=1, row=1, pady=5)

    ttk.Label(dreta, text="Descripció:").grid(column=0, row=2, sticky="nw", pady=(10, 0))
    tk.Text(dreta, width=50, height=5, bg="white", bd=0, highlightbackground="#ccc", relief="flat", font=("Segoe UI", 10)).grid(column=1, row=2, pady=5)

    ttk.Label(dreta, text="Estat:").grid(column=0, row=3, sticky="w", pady=(10, 0))
    ttk.Combobox(dreta, values=["Pendent", "Completada"], state="readonly", width=47).grid(column=1, row=3, pady=5)

    ttk.Label(dreta, text="Categoria:").grid(column=0, row=4, sticky="w", pady=(10, 0))
    ttk.Entry(dreta, width=50).grid(column=1, row=4, pady=5)

    ttk.Label(dreta, text="Data límit:").grid(column=0, row=5, sticky="w", pady=(10, 0))
    ttk.Entry(dreta, width=50).grid(column=1, row=5, pady=5)

    boto_frame = ttk.Frame(dreta)
    boto_frame.grid(column=0, row=6, columnspan=2, pady=20)

    ttk.Button(boto_frame, text="Guardar Canvis").pack(side="left", padx=10)
    ttk.Button(boto_frame, text="Eliminar Tasca").pack(side="left", padx=10)

#Crear la pestanya de exportar tasques en format JSON
def crear_layout_exportar(frame):
    aplicar_estil(frame)
    contenidor = ttk.Frame(frame, padding=30)
    contenidor.pack(expand=True)

    ttk.Label(contenidor, text="Exportar Tasques", font=("Segoe UI", 14, "bold")).pack(pady=10)
    ttk.Label(contenidor, text="Les dades s'exportaran a un fitxer .json amb les tasques actuals.").pack(pady=10)

    ttk.Button(contenidor, text="Exportar a JSON").pack(pady=20)
