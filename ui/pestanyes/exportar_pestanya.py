import tkinter as tk
from tkinter import ttk, messagebox
from logic import exportar_json

def crear_layout_exportar(frame, aplicar_estil, colors):
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