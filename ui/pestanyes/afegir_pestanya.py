import tkinter as tk
from tkinter import ttk, messagebox
from logic import afegir_tasca
from utils import validar_data, validar_text, validar_categoria, validar_estat

def crear_layout_afegir(frame, aplicar_estil, colors):
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