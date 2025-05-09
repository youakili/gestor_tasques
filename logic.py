import sqlite3
import logging
from datetime import datetime

# Configuració del logging
logging.basicConfig(filename="logging.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


# Crear i connectar a la BBDD
def crear_db():
    """Connecta o crea la base de dades 'tasques.db' i la taula si no existeix."""
    try:
        conn = sqlite3.connect("tasques.db")
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasques (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titol TEXT NOT NULL,
                descripcio TEXT,
                estat TEXT CHECK(estat IN ('Pendent', 'Completada')) NOT NULL DEFAULT 'Pendent',
                categoria TEXT,
                data_limit TEXT,
                data_creacio TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        logging.info("Base de dades creada o oberta correctament.")
    except Exception as e:
        logging.error(f"Error en crear_db: {e}")


def afegir_tasca(titol, descripcio="", estat="Pendent", categoria="", data_limit=None):
    #Afegeix una nova tasca a la base de dades.
    try:
        conn = sqlite3.connect("tasques.db")
        cursor = conn.cursor()
        data_creacio = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('''
            INSERT INTO tasques (titol, descripcio, estat, categoria, data_limit, data_creacio)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (titol, descripcio, estat, categoria, data_limit, data_creacio))
        conn.commit()
        conn.close()
        logging.info(f"Tasca afegida: {titol}")
    except Exception as e:
        logging.error(f"Error en afegir_tasca: {e}")

def llistar_tasques():
    #Retorna totes les tasques de la base de dades.
    try:
        conn = sqlite3.connect("tasques.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasques")
        resultats = cursor.fetchall()
        conn.close()
        logging.info("Tasques llistades correctament.")
        return resultats
    except Exception as e:
        logging.error(f"Error en llistar_tasques: {e}")
        return []

def eliminar_tasca(id_tasca):
    #Elimina una tasca a partir del seu ID.
    try:
        conn = sqlite3.connect("tasques.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasques WHERE id = ?", (id_tasca,))
        conn.commit()
        conn.close()
        logging.info(f"Tasca amb ID {id_tasca} eliminada.")
    except Exception as e:
        logging.error(f"Error en eliminar_tasca: {e}")

def modificar_tasca(id_tasca, titol=None, descripcio=None, estat=None, categoria=None, data_limit=None):
    #Modifica els camps d'una tasca específica si es proporcionen.
    try:
        conn = sqlite3.connect("tasques.db")
        cursor = conn.cursor()

        camps = []
        valors = []

        if titol:
            camps.append("titol = ?")
            valors.append(titol)
        if descripcio:
            camps.append("descripcio = ?")
            valors.append(descripcio)
        if estat:
            camps.append("estat = ?")
            valors.append(estat)
        if categoria:
            camps.append("categoria = ?")
            valors.append(categoria)
        if data_limit:
            camps.append("data_limit = ?")
            valors.append(data_limit)

        if camps:
            consulta = f"UPDATE tasques SET {', '.join(camps)} WHERE id = ?"
            valors.append(id_tasca)
            cursor.execute(consulta, tuple(valors))
            conn.commit()
            logging.info(f"Tasca {id_tasca} modificada.")
        conn.close()
    except Exception as e:
        logging.error(f"Error en modificar_tasca: {e}")
