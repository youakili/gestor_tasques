from tkinter import ttk
from ui.pestanyes.afegir_pestanya import crear_layout_afegir as crear_afegir
from ui.pestanyes.llistar_pestanya import crear_layout_llistar as crear_llistar
from ui.pestanyes.modificar_pestanya import crear_layout_modificar as crear_modificar
from ui.pestanyes.exportar_pestanya import crear_layout_exportar as crear_exportar

# Paleta de colors (compartida)
COLOR_FONS = "#F5F7FA"
COLOR_MARCS = "#FFFFFF"
COLOR_TEXT = "#333333"
COLOR_ACCENT = "#3B82F6"  
COLOR_BOTO = "#2563EB"    
COLOR_BOTO_TEXT = "#FFFFFF"
COLOR_URGENT = "#FF0000"
COLOR_VENCIDA = "#000000"
COLOR_FONS_VENCIDA = "#FFCCCC"

# Diccionari de colors
colors = {
    'fons': COLOR_FONS,
    'marcs': COLOR_MARCS,
    'text': COLOR_TEXT,
    'accent': COLOR_ACCENT,
    'boto': COLOR_BOTO,
    'boto_text': COLOR_BOTO_TEXT,
    'urgent': COLOR_URGENT,
    'vencida': COLOR_VENCIDA,
    'fons_vencida': COLOR_FONS_VENCIDA
}

def aplicar_estil(widget):
    style = ttk.Style()
    style.theme_use("clam")
    
    # Configuració bàsica
    style.configure("TFrame", background=colors['fons'])
    style.configure("TLabel", background=colors['fons'], foreground=colors['text'], 
                   font=("Segoe UI", 10))
    style.configure("TButton", background=colors['boto'], foreground=colors['boto_text'], 
                   font=("Segoe UI", 10), padding=6)
    style.map("TButton", background=[("active", "#1D4ED8")])
    style.configure("TNotebook", background=colors['fons'], tabposition='n')
    style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 6])
    style.map("TNotebook.Tab", background=[("selected", "#E0ECFF")], foreground=[("selected", "#000")])
    style.configure("TCombobox", padding=5)
    
    # Estils per al Treeview
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.map("Treeview", background=[("selected", colors['accent'])])

# Funcions que seran cridades des de window.py
def crear_layout_afegir(frame):
    return crear_afegir(frame, aplicar_estil, colors)

def crear_layout_llistar(frame):
    return crear_llistar(frame, aplicar_estil, colors)

def crear_layout_modificar(frame):
    return crear_modificar(frame, aplicar_estil, colors)

def crear_layout_exportar(frame):
    return crear_exportar(frame, aplicar_estil, colors)