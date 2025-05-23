import tkinter as tk
from ui.window import crear_finestra
from logic import crear_db
from alert import mostrar_alertes
import test
import parm

# Processar paràmetres
parm.processar_parametres()

# Inicialitzar base de dades
crear_db()

# Crear la finestra de l'aplicació
finestra = tk.Tk()
crear_finestra(finestra)

# Minimitzar si cal
if parm.obtenir_parametre('--minim'):
    finestra.iconify()

# Iniciar l'aplicació
finestra.mainloop()