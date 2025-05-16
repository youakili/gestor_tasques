import tkinter as tk
from tkinter import messagebox
from logic import llistar_tasques
from utils import calcular_dies_restants
from datetime import datetime

def mostrar_alertes():
    #Mostra alertes visuals per tasques properes a la data límit
    tasques = llistar_tasques()
    avui = datetime.today()
    
    for tasca in tasques:
        id_tasca, titol, _, estat, _, data_limit, _ = tasca
        
        if estat != "Pendent" or not data_limit:
            continue
            
        try:
            data_limit = datetime.strptime(data_limit, "%Y-%m-%d")
            dies_restants = (data_limit - avui).days
            
            if dies_restants < 0:
                # Tasca vençuda
                messagebox.showwarning(
                    "Tasca Vençuda", 
                    f"La tasca '{titol}' ha superat la data límit!\nData límit: {data_limit.strftime('%Y-%m-%d')}",
                    icon='warning'
                )
            elif dies_restants <= 2:
                # Tasca propera a vençiment
                messagebox.showwarning(
                    "Tasca Propera a Vençiment", 
                    f"La tasca '{titol}' està a punt de vençre!\nDies restants: {dies_restants}\nData límit: {data_limit.strftime('%Y-%m-%d')}",
                    icon='error'
                )
                
        except ValueError:
            continue

def aplicar_estil_alertes(treeview):
    #Aplica colors a les tasques segons la urgència
    tasques = llistar_tasques()
    avui = datetime.today()
    
    for i, tasca in enumerate(tasques):
        _, titol, _, estat, _, data_limit, _ = tasca
        
        if estat != "Pendent" or not data_limit:
            continue
            
        try:
            data_limit = datetime.strptime(data_limit, "%Y-%m-%d")
            dies_restants = (data_limit - avui).days
            
            if dies_restants < 0:
                # Tasca vençuda - color negre
                treeview.tag_configure('vencida', foreground='black', background='#FFCCCC')
                treeview.item(treeview.get_children()[i], tags=('vencida',))
            elif dies_restants <= 2:
                # Tasca urgent - color vermell
                treeview.tag_configure('urgent', foreground='red')
                treeview.item(treeview.get_children()[i], tags=('urgent',))
                
        except ValueError:
            continue