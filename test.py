import sys
import time
from tkinter import Tk, ttk
from logic import crear_db, afegir_tasca, llistar_tasques, modificar_tasca, eliminar_tasca
from ui.window import crear_finestra
from ui.pestanyes.afegir_pestanya import crear_layout_afegir
from ui.pestanyes.llistar_pestanya import crear_layout_llistar
from ui.pestanyes.modificar_pestanya import crear_layout_modificar

def run_tests():
    #Funció principal per executar els tests
    print("⏳ Iniciant tests...")
    
    # Configuració inicial
    crear_db()  # Assegurar que la BBDD existeix
    
    # 1. Test Afegir Tasca
    print("\n🔵 TEST 1: Afegir nova tasca 'asd'")
    test_afegir_tasca()
    
    # 2. Test Llistar Tasques (verificar que existeix)
    print("\n🔵 TEST 2: Buscar tasca 'asd' a la llista")
    test_llistar_tasques("asd", True)
    
    # 3. Test Modificar Tasca (canviar a 'dsa')
    print("\n🔵 TEST 3: Modificar tasca 'asd' a 'dsa'")
    test_modificar_tasca()
    
    # 4. Test Llistar Tasques (verificar canvi)
    print("\n🔵 TEST 4: Buscar tasca 'dsa' a la llista")
    test_llistar_tasques("dsa", True)
    
    # 5. Test Eliminar Tasca
    print("\n🔵 TEST 5: Eliminar tasca 'dsa'")
    test_eliminar_tasca()
    
    # 6. Test Verificar Eliminació
    print("\n🔵 TEST 6: Verificar que 'dsa' ja no existeix")
    test_llistar_tasques("dsa", False)
    
    print("\n✅ Tots els tests executats correctament!")

def test_afegir_tasca():
    #Test per afegir una nova tasca
    try:
        # Crear finestra temporal per les operacions GUI
        root = Tk()
        root.withdraw()  # No mostrar la finestra
        
        # Crear frame temporal
        frame = ttk.Frame(root)
        
        # Simular afegir tasca
        afegir_tasca("asd", "Descripció de prova", "Pendent", "Test", "2023-12-31")
        print("✓ Tasca 'asd' afegida correctament")
        
        root.destroy()
    except Exception as e:
        print(f"❌ Error en test_afegir_tasca: {e}")
        sys.exit(1)

def test_llistar_tasques(nom_tasca, hauria_existir):
    #Test per verificar si una tasca existeix a la llista
    try:
        root = Tk()
        root.withdraw()
        frame = ttk.Frame(root)
        
        # Obtenir totes les tasques
        tasques = llistar_tasques()
        trobada = any(tasca[1] == nom_tasca for tasca in tasques)
        
        if trobada and hauria_existir:
            print(f"✓ Tasca '{nom_tasca}' trobada com s'esperava")
        elif not trobada and not hauria_existir:
            print(f"✓ Tasca '{nom_tasca}' no trobada com s'esperava")
        else:
            print(f"❌ Resultat inesperat en buscar '{nom_tasca}'")
            sys.exit(1)
            
        root.destroy()
    except Exception as e:
        print(f"❌ Error en test_llistar_tasques: {e}")
        sys.exit(1)

def test_modificar_tasca():
    #Test per modificar una tasca existent
    try:
        root = Tk()
        root.withdraw()
        frame = ttk.Frame(root)
        
        # Trobar ID de la tasca 'asd'
        tasques = llistar_tasques()
        tasca_asd = next((t for t in tasques if t[1] == "asd"), None)
        
        if not tasca_asd:
            print("❌ No s'ha trobat la tasca 'asd' per modificar")
            sys.exit(1)
            
        # Modificar a 'dsa'
        modificar_tasca(tasca_asd[0], "dsa", "Descripció modificada", "Pendent", "Test", "2023-12-31")
        print("✓ Tasca modificada de 'asd' a 'dsa'")
        
        root.destroy()
    except Exception as e:
        print(f"❌ Error en test_modificar_tasca: {e}")
        sys.exit(1)

def test_eliminar_tasca():
    #Test per eliminar una tasca
    try:
        root = Tk()
        root.withdraw()
        frame = ttk.Frame(root)
        
        # Trobar ID de la tasca 'dsa'
        tasques = llistar_tasques()
        tasca_dsa = next((t for t in tasques if t[1] == "dsa"), None)
        
        if not tasca_dsa:
            print("❌ No s'ha trobat la tasca 'dsa' per eliminar")
            sys.exit(1)
            
        # Eliminar tasca
        eliminar_tasca(tasca_dsa[0])
        print("✓ Tasca 'dsa' eliminada correctament")
        
        root.destroy()
    except Exception as e:
        print(f"❌ Error en test_eliminar_tasca: {e}")
        sys.exit(1)

run_tests()
    