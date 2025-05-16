import tkinter as tk
from tkinter import ttk, messagebox
from logic import afegir_tasca, llistar_tasques, modificar_tasca, eliminar_tasca, exportar_json
from utils import validar_data, validar_text, validar_categoria, validar_estat, calcular_dies_restants
from alert import aplicar_estil_alertes
from datetime import datetime

# Paleta de colors
COLOR_FONS = "#F5F7FA"
COLOR_MARCS = "#FFFFFF"
COLOR_TEXT = "#333333"
COLOR_ACCENT = "#3B82F6"  
COLOR_BOTO = "#2563EB"    
COLOR_BOTO_TEXT = "#FFFFFF"
COLOR_URGENT = "#FF0000"
COLOR_VENCIDA = "#000000"
COLOR_FONS_VENCIDA = "#FFCCCC"

# Estil global
def aplicar_estil(widget):
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configuració bàsica
    style.configure("TFrame", background=COLOR_FONS)
    style.configure("TLabel", background=COLOR_FONS, foreground=COLOR_TEXT, font=("Segoe UI", 10))
    style.configure("TButton", background=COLOR_BOTO, foreground=COLOR_BOTO_TEXT, 
                   font=("Segoe UI", 10), padding=6)
    style.map("TButton", background=[("active", "#1D4ED8")])
    style.configure("TNotebook", background=COLOR_FONS, tabposition='n')
    style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 6])
    style.map("TNotebook.Tab", background=[("selected", "#E0ECFF")], foreground=[("selected", "#000")])
    style.configure("TCombobox", padding=5)
    
    # Estils per al Treeview
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.map("Treeview", background=[("selected", COLOR_ACCENT)])

def crear_layout_afegir(frame):
    #Afegeix una nova tasca a la base de dades.
    aplicar_estil(frame)
    frame.columnconfigure(0, weight=1)
    contenidor = ttk.Frame(frame, padding=30, style="TFrame")
    contenidor.grid(column=0, row=0, sticky="nsew")

    ttk.Label(contenidor, text="Afegir una nova tasca", font=("Segoe UI", 14, "bold")).grid(column=0, row=0, columnspan=2, pady=(0, 20))

    # Camps del formulari
    camps = [
        ("Títol:*", ttk.Entry(contenidor, width=50)),
        ("Descripció:", tk.Text(contenidor, width=50, height=5, bg="white", bd=0, 
                              highlightbackground="#ccc", relief="flat", font=("Segoe UI", 10))),
        ("Estat:*", ttk.Combobox(contenidor, values=["Pendent", "Completada"], state="readonly", width=47)),
        ("Categoria:", ttk.Entry(contenidor, width=50)),
        ("Data límit (AAAA-MM-DD):", ttk.Entry(contenidor, width=50))
    ]

    entrada_estat = camps[2][1]
    entrada_estat.set("Pendent")

    for i, (label, widget) in enumerate(camps, start=1):
        ttk.Label(contenidor, text=label).grid(column=0, row=i, sticky="w", pady=(10 if i>1 else 0))
        widget.grid(column=1, row=i, pady=5)

    entrada_titol, entrada_desc, entrada_estat, entrada_categoria, entrada_data = [camp[1] for camp in camps]

    def afegir_callback():
        # Obtenir valors
        titol = entrada_titol.get().strip()
        descripcio = entrada_desc.get("1.0", tk.END).strip()
        estat = entrada_estat.get()
        categoria = entrada_categoria.get().strip()
        data_limit = entrada_data.get().strip()

        # Validacions
        if not validar_text(titol, min_len=1, max_len=100):
            messagebox.showwarning("Títol invàlid", "El títol és obligatori (1-100 caràcters)")
            return

        if not validar_estat(estat):
            messagebox.showwarning("Estat invàlid", "Selecciona un estat vàlid")
            return

        if categoria and not validar_categoria(categoria):
            messagebox.showwarning("Categoria invàlida", "Utilitza només lletres, números o guions")
            return

        if data_limit and not validar_data(data_limit):
            messagebox.showwarning("Data invàlida", "Format correcte: AAAA-MM-DD")
            return

        # Afegir tasca
        afegir_tasca(titol, descripcio, estat, categoria, data_limit if data_limit else None)
        messagebox.showinfo("Èxit", "Tasca afegida correctament")

        # Netejar camps
        entrada_titol.delete(0, tk.END)
        entrada_desc.delete("1.0", tk.END)
        entrada_estat.set("Pendent")
        entrada_categoria.delete(0, tk.END)
        entrada_data.delete(0, tk.END)

    ttk.Button(contenidor, text="Afegir Tasca", command=afegir_callback).grid(column=0, row=6, columnspan=2, pady=20)

def crear_layout_llistar(frame):
    #Retorna totes les tasques de la base de dades.
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

def crear_layout_modificar(frame):
    #Modifica els camps d'una tasca específica si es proporcionen.
    aplicar_estil(frame)
    frame.columnconfigure(1, weight=1)

    # Llista tasques (Treeview)
    esquerra = ttk.Frame(frame, padding=10)
    esquerra.grid(row=0, column=0, sticky="nsw")

    ttk.Label(esquerra, text="Tasques:", font=("Segoe UI", 12, "bold")).pack(anchor="w")

    tree = ttk.Treeview(esquerra, columns=('titol', 'estat'), show='headings', height=25)
    tree.column('titol', width=200, anchor='w')
    tree.column('estat', width=100, anchor='center')
    tree.heading('titol', text='Títol')
    tree.heading('estat', text='Estat')
    tree.pack()

    # Formulari modificació
    dreta = ttk.Frame(frame, padding=20)
    dreta.grid(row=0, column=1, sticky="nsew")

    ttk.Label(dreta, text="Modificar / Eliminar", font=("Segoe UI", 14, "bold")).grid(column=0, row=0, columnspan=2, pady=10)

    # Camps formulari
    camps = [
        ("Títol:*", ttk.Entry(dreta, width=50)),
        ("Descripció:", tk.Text(dreta, width=50, height=5, bg="white", bd=0, 
                              highlightbackground="#ccc", relief="flat", font=("Segoe UI", 10))),
        ("Estat:*", ttk.Combobox(dreta, values=["Pendent", "Completada"], state="readonly", width=47)),
        ("Categoria:", ttk.Entry(dreta, width=50)),
        ("Data límit (AAAA-MM-DD):", ttk.Entry(dreta, width=50))
    ]

    for i, (label, widget) in enumerate(camps, start=1):
        ttk.Label(dreta, text=label).grid(column=0, row=i, sticky="w", pady=(10 if i>1 else 0))
        widget.grid(column=1, row=i, pady=5)

    entrada_titol, entrada_desc, entrada_estat, entrada_categoria, entrada_data = [camp[1] for camp in camps]

    # Botons
    boto_frame = ttk.Frame(dreta)
    boto_frame.grid(column=0, row=6, columnspan=2, pady=20)

    boto_guardar = ttk.Button(boto_frame, text="Guardar Canvis")
    boto_guardar.pack(side="left", padx=10)

    boto_eliminar = ttk.Button(boto_frame, text="Eliminar Tasca")
    boto_eliminar.pack(side="left", padx=10)

    tasques_cache = []
    id_seleccionada = None

    def carregar_tasques():
        nonlocal tasques_cache
        tasques_cache = llistar_tasques()
        tree.delete(*tree.get_children())
        for tasca in tasques_cache:
            tree.insert('', 'end', values=(tasca[1], tasca[3]))
        
        aplicar_estil_alertes(tree)

    def omplir_dades(event):
        nonlocal id_seleccionada
        item = tree.focus()
        if not item:
            return
            
        index = tree.index(item)
        tasca = tasques_cache[index]
        id_seleccionada = tasca[0]
        
        entrada_titol.delete(0, tk.END)
        entrada_titol.insert(0, tasca[1])
        
        entrada_desc.delete("1.0", tk.END)
        entrada_desc.insert(tk.END, tasca[2] or "")
        
        entrada_estat.set(tasca[3])
        
        entrada_categoria.delete(0, tk.END)
        entrada_categoria.insert(0, tasca[4] or "")
        
        entrada_data.delete(0, tk.END)
        entrada_data.insert(0, tasca[5] or "")

    def guardar_canvis():
        if id_seleccionada is None:
            messagebox.showwarning("Error", "Selecciona una tasca primer")
            return

        titol = entrada_titol.get().strip()
        descripcio = entrada_desc.get("1.0", tk.END).strip()
        estat = entrada_estat.get()
        categoria = entrada_categoria.get().strip()
        data_limit = entrada_data.get().strip()

        # Validacions
        if not validar_text(titol, min_len=1, max_len=100):
            messagebox.showwarning("Títol invàlid", "El títol és obligatori (1-100 caràcters)")
            return

        if not validar_estat(estat):
            messagebox.showwarning("Estat invàlid", "Selecciona un estat vàlid")
            return

        if categoria and not validar_categoria(categoria):
            messagebox.showwarning("Categoria invàlida", "Utilitza només lletres, números o guions")
            return

        if data_limit and not validar_data(data_limit):
            messagebox.showwarning("Data invàlida", "Format correcte: AAAA-MM-DD")
            return

        modificar_tasca(
            id_seleccionada,
            titol,
            descripcio if descripcio else None,
            estat,
            categoria if categoria else None,
            data_limit if data_limit else None
        )
        
        messagebox.showinfo("Èxit", "Tasca modificada correctament")
        carregar_tasques()

    def eliminar_tasca_seleccionada():
        if id_seleccionada is None:
            messagebox.showwarning("Error", "Selecciona una tasca primer")
            return
            
        if messagebox.askyesno("Confirmar", "Estàs segur que vols eliminar aquesta tasca?"):
            eliminar_tasca(id_seleccionada)
            messagebox.showinfo("Èxit", "Tasca eliminada correctament")
            carregar_tasques()
            
            # Netejar camps
            entrada_titol.delete(0, tk.END)
            entrada_desc.delete("1.0", tk.END)
            entrada_estat.set("")
            entrada_categoria.delete(0, tk.END)
            entrada_data.delete(0, tk.END)

    tree.bind("<<TreeviewSelect>>", omplir_dades)
    boto_guardar.config(command=guardar_canvis)
    boto_eliminar.config(command=eliminar_tasca_seleccionada)
    carregar_tasques()

def crear_layout_exportar(frame):
    #Exporta totes les tasques de la base de dades a un fitxer JSON.    
    aplicar_estil(frame)
    contenidor = ttk.Frame(frame, padding=30)
    contenidor.pack(expand=True)

    ttk.Label(contenidor, text="Exportar Tasques", font=("Segoe UI", 14, "bold")).pack(pady=10)
    ttk.Label(contenidor, text="Les dades s'exportaran a un fitxer .json amb les tasques actuals.").pack(pady=10)

    def exportar_callback():
        if exportar_json():
            messagebox.showinfo("Èxit", "Tasques exportades correctament a tasques_exportades.json")
        else:
            messagebox.showerror("Error", "No s'ha pogut exportar les tasques")

    ttk.Button(contenidor, text="Exportar a JSON", command=exportar_callback).pack(pady=20)