import tkinter as tk
from tkinter import ttk, messagebox
from logic import modificar_tasca, eliminar_tasca, llistar_tasques
from utils import validar_data, validar_text, validar_categoria, validar_estat
from alert import aplicar_estil_alertes

def crear_layout_modificar(frame, aplicar_estil, colors):
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