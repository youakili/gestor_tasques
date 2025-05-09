import tkinter as tk
from ui.window import crear_finestra
from logic import crear_db

# Inicialitzar base de dades
crear_db()

# Crear la finestra de l'aplicació
finestra = tk.Tk()
crear_finestra(finestra)

# Iniciar l'aplicació
finestra.mainloop()
