# utils.py
from datetime import datetime
import logging
import re

def validar_data(data_str):
    #Valida si la data té el format correcte (YYYY-MM-DD).
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        logging.warning(f"Data no vàlida: {data_str}")
        return False

def validar_text(text, min_len=1, max_len=100):
    #Valida que el text tingui la longitud adequada.
    if not isinstance(text, str):
        return False
    return min_len <= len(text.strip()) <= max_len

def validar_categoria(categoria):
    #Valida que la categoria sigui vàlida (alfanumèrica amb espais i guions).
    if not categoria:  # Permet categories buides
        return True
    return bool(re.match(r'^[a-zA-ZÀ-ÿ0-9\s\-]+$', categoria))

def validar_estat(estat):
    #Valida que l'estat sigui 'Pendent' o 'Completada'.
    return estat in ['Pendent', 'Completada']

def calcular_dies_restants(data_limit):
    #Calcula els dies restants fins a una data límit.
    try:
        avui = datetime.today()
        limit = datetime.strptime(data_limit, "%Y-%m-%d")
        dies = (limit - avui).days
        return dies if dies >= 0 else 0
    except:
        return None