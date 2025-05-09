import tkinter as tk
from tkinter import ttk
from ui.layout import crear_layout_afegir, crear_layout_llistar, crear_layout_modificar, crear_layout_exportar

def crear_finestra(finestra):
    
    #Crea la finestra principal amb pestanyes i carrega els layouts visuals
    
    finestra.title("Gestor de Tasques")
    finestra.geometry("900x600")
    finestra.resizable(False, False)

    pestanyes = ttk.Notebook(finestra)
    pestanyes.pack(expand=True, fill="both")

    # Crear els frames de les pestanyes
    frame_afegir = ttk.Frame(pestanyes)
    frame_llistar = ttk.Frame(pestanyes)
    frame_modificar = ttk.Frame(pestanyes)
    frame_exportar = ttk.Frame(pestanyes)

    pestanyes.add(frame_afegir, text="Afegir Tasca")
    pestanyes.add(frame_llistar, text="Llistar Tasques")
    pestanyes.add(frame_modificar, text="Modificar / Eliminar")
    pestanyes.add(frame_exportar, text="Exportar")

    # Disseny visual de cada pestanya 
    crear_layout_afegir(frame_afegir)
    crear_layout_llistar(frame_llistar)
    crear_layout_modificar(frame_modificar)
    crear_layout_exportar(frame_exportar)
