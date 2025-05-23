from tkinter import ttk
from ui.pestanyes.afegir_pestanya import crear_layout_afegir as crear_afegir
from ui.pestanyes.llistar_pestanya import crear_layout_llistar as crear_llistar
from ui.pestanyes.modificar_pestanya import crear_layout_modificar as crear_modificar
from ui.pestanyes.exportar_pestanya import crear_layout_exportar as crear_exportar
import parm

# Paletes de colors
COLORS_NORMAL = {
    'fons': "#F5F7FA", 'marcs': "#FFFFFF", 'text': "#333333",
    'accent': "#3B82F6", 'boto': "#2563EB", 'boto_text': "#FFFFFF",
    'urgent': "#FF0000", 'vencida': "#000000", 'fons_vencida': "#FFCCCC"
}

COLORS_FOSC = {
    'fons': "#1E1E1E", 'marcs': "#2D2D2D", 'text': "#E0E0E0",
    'accent': "#3B82F6", 'boto': "#2563EB", 'boto_text': "#FFFFFF",
    'urgent': "#FF6B6B", 'vencida': "#FFFFFF", 'fons_vencida': "#660000"
}

COLORS_PROTECCIO = {
    'fons': "#FFFFE0", 'marcs': "#FFFFCC", 'text': "#333300",
    'accent': "#666600", 'boto': "#999900", 'boto_text': "#FFFFFF",
    'urgent': "#FF0000", 'vencida': "#663300", 'fons_vencida': "#FFCC99"
}

def obtenir_colors():
    if parm.obtenir_parametre('--mode-fosc'):
        return COLORS_FOSC
    elif parm.obtenir_parametre('--proteccio-ulls'):
        return COLORS_PROTECCIO
    return COLORS_NORMAL

def aplicar_estil(widget):
    colors = obtenir_colors()
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configuració bàsica
    mida_font = 10 + (2 if parm.obtenir_parametre('--lupa') else 0)
    style.configure("TFrame", background=colors['fons'])
    style.configure("TLabel", background=colors['fons'], foreground=colors['text'], 
                   font=("Segoe UI", mida_font))
    style.configure("TButton", background=colors['boto'], foreground=colors['boto_text'], 
                   font=("Segoe UI", mida_font), padding=6)
    style.map("TButton", background=[("active", "#1D4ED8")])
    
    # Configuració per a alt contrast
    if parm.obtenir_parametre('--alt-contrast'):
        style.configure("TFrame", background="black")
        style.configure("TLabel", background="black", foreground="yellow")
        style.configure("TButton", background="yellow", foreground="black")

# Funcions que seran cridades des de window.py
def crear_layout_afegir(frame):
    return crear_afegir(frame, aplicar_estil, obtenir_colors())

def crear_layout_llistar(frame):
    return crear_llistar(frame, aplicar_estil, obtenir_colors())

def crear_layout_modificar(frame):
    return crear_modificar(frame, aplicar_estil, obtenir_colors())

def crear_layout_exportar(frame):
    return crear_exportar(frame, aplicar_estil, obtenir_colors())