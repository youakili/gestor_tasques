import tkinter as tk
from tkinter import ttk
from ui.layout import crear_layout_afegir, crear_layout_llistar, crear_layout_modificar, crear_layout_exportar

def crear_finestra(finestra):
    # Configuració bàsica de la finestra
    finestra.title("Reyos")
    finestra.geometry("900x600")
    finestra.resizable(False, False)

    # Crear pestanyes
    pestanyes = ttk.Notebook(finestra)
    pestanyes.pack(expand=True, fill="both")

    # Crear frames per cada pestanya
    frames = {
        "afegir": ttk.Frame(pestanyes),
        "llistar": ttk.Frame(pestanyes),
        "modificar": ttk.Frame(pestanyes),
        "exportar": ttk.Frame(pestanyes)
    }

    # Afegir pestanyes
    pestanyes.add(frames["afegir"], text="Afegir Tasca")
    pestanyes.add(frames["llistar"], text="Llistar Tasques")
    pestanyes.add(frames["modificar"], text="Modificar/Eliminar")
    pestanyes.add(frames["exportar"], text="Exportar")

    # Carregar layouts
    crear_layout_afegir(frames["afegir"])
    crear_layout_llistar(frames["llistar"])
    crear_layout_modificar(frames["modificar"])
    crear_layout_exportar(frames["exportar"])