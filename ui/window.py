import tkinter as tk
from tkinter import ttk

def crear_finestra(finestra):
    
    #Crea la finestra principal amb pestanyes (afegir, llistar, modificar, exportar)
    
    finestra.title("Gestor de Tasques")  # Títol de la finestra
    finestra.geometry("900x600")         # Mida per defecte
    finestra.resizable(False, False)     # No permet redimensionar

    # Crear el notebook (pestanyes superiors)
    pestanyes = ttk.Notebook(finestra)
    pestanyes.pack(expand=True, fill="both")

    # Crear frames per cada pestanya
    pestanya_afegir = ttk.Frame(pestanyes)
    pestanya_llistar = ttk.Frame(pestanyes)
    pestanya_modificar = ttk.Frame(pestanyes)
    pestanya_exportar = ttk.Frame(pestanyes)

    # Afegir pestanyes al notebook
    pestanyes.add(pestanya_afegir, text="Afegir Tasca")
    pestanyes.add(pestanya_llistar, text="Llistar Tasques")
    pestanyes.add(pestanya_modificar, text="Modificar / Eliminar")
    pestanyes.add(pestanya_exportar, text="Exportar")

