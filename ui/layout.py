import tkinter as tk
from tkinter import ttk
from logic import afegir_tasca, llistar_tasques
from utils import validar_data
from tkinter import messagebox

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
    entrada_titol = ttk.Entry(contenidor, width=50)
    entrada_titol.grid(column=1, row=1, pady=5)

    ttk.Label(contenidor, text="Descripció:").grid(column=0, row=2, sticky="nw", pady=(10, 0))
    entrada_desc = tk.Text(contenidor, width=50, height=5, bg="white", bd=0, highlightbackground="#ccc", relief="flat", font=("Segoe UI", 10))
    entrada_desc.grid(column=1, row=2, pady=5)

    ttk.Label(contenidor, text="Estat inicial:").grid(column=0, row=3, sticky="w", pady=(10, 0))
    entrada_estat = ttk.Combobox(contenidor, values=["Pendent", "Completada"], state="readonly", width=47)
    entrada_estat.set("Pendent")
    entrada_estat.grid(column=1, row=3, pady=5)

    ttk.Label(contenidor, text="Categoria:").grid(column=0, row=4, sticky="w", pady=(10, 0))
    entrada_categoria = ttk.Entry(contenidor, width=50)
    entrada_categoria.grid(column=1, row=4, pady=5)

    ttk.Label(contenidor, text="Data límit (AAAA-MM-DD):").grid(column=0, row=5, sticky="w", pady=(10, 0))
    entrada_data = ttk.Entry(contenidor, width=50)
    entrada_data.grid(column=1, row=5, pady=5)

    def afegir_callback():
        titol = entrada_titol.get().strip()
        descripcio = entrada_desc.get("1.0", tk.END).strip()
        estat = entrada_estat.get()
        categoria = entrada_categoria.get().strip()
        data_limit = entrada_data.get().strip()

        if not titol:
            messagebox.showwarning("Camp requerit", "El camp 'Títol' és obligatori.")
            return

        if data_limit and not validar_data(data_limit):
            messagebox.showwarning("Data invàlida", "El format de la data ha de ser YYYY-MM-DD.")
            return

        afegir_tasca(titol, descripcio, estat, categoria, data_limit)
        messagebox.showinfo("Èxit", "Tasca afegida correctament.")

        entrada_titol.delete(0, tk.END)
        entrada_desc.delete("1.0", tk.END)
        entrada_estat.set("Pendent")
        entrada_categoria.delete(0, tk.END)
        entrada_data.delete(0, tk.END)

    ttk.Button(contenidor, text="Afegir Tasca", command=afegir_callback).grid(column=0, row=6, columnspan=2, pady=20)

#Crear la pestanya de llistar tasques
def crear_layout_llistar(frame):
    from datetime import datetime
    aplicar_estil(frame)
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(1, weight=1)

    # TOP: Filtre per paraula clau
    top = ttk.Frame(frame, padding=10)
    top.grid(row=0, column=0, columnspan=2, sticky="ew")

    ttk.Label(top, text="Buscar/Filtrar:", font=("Segoe UI", 10)).pack(side="left", padx=5)
    entrada_filtre = ttk.Entry(top, width=40)
    entrada_filtre.pack(side="left", padx=5)

    # ESQUERRA: Llista de tasques
    esquerra = ttk.Frame(frame, padding=10)
    esquerra.grid(row=1, column=0, sticky="nsw")

    ttk.Label(esquerra, text="Tasques:", font=("Segoe UI", 12, "bold")).pack(anchor="w")

    llista = tk.Listbox(esquerra, width=40, height=25, bd=0, highlightthickness=1,
                        highlightbackground="#ccc", relief="flat", font=("Segoe UI", 10))
    llista.pack(pady=5)

    # DRETA: Detalls de la tasca seleccionada
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

    tasques_cache = []  # S'actualitzarà cada vegada que es carreguin

    def calcular_dies_restants(data_limit):
        try:
            avui = datetime.today()
            limit = datetime.strptime(data_limit, "%Y-%m-%d")
            return (limit - avui).days
        except:
            return "-"

    def carregar_tasques():
        nonlocal tasques_cache
        filtre = entrada_filtre.get().strip().lower()
        tasques = llistar_tasques()
        llista.delete(0, tk.END)
        tasques_cache = []

        for tasca in tasques:
            id_, titol, descripcio, estat, categoria, data_limit, _ = tasca
            if filtre in titol.lower() or filtre in (descripcio or "").lower():
                tasques_cache.append(tasca)
                llista.insert(tk.END, f"{titol}")

    def mostrar_detalls(event):
        index = llista.curselection()
        if not index:
            return
        tasca = tasques_cache[index[0]]
        id_, titol, descripcio, estat, categoria, data_limit, _ = tasca

        valors_detall["Títol"].config(text=titol)
        valors_detall["Descripció"].config(text=descripcio or "-")
        valors_detall["Estat"].config(text=estat)
        valors_detall["Categoria"].config(text=categoria or "-")
        valors_detall["Data límit"].config(text=data_limit or "-")
        valors_detall["Dies restants"].config(text=calcular_dies_restants(data_limit) if data_limit else "-")

    entrada_filtre.bind("<KeyRelease>", lambda e: carregar_tasques())
    llista.bind("<<ListboxSelect>>", mostrar_detalls)

    carregar_tasques()
    

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
