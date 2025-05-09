from datetime import datetime
import logging

def validar_data(data_str):
    #Valida si la data té el format correcte (YYYY-MM-DD).
    try:
        datetime.strptime(data_str, "%Y-%m-%d")
        return True
    except ValueError:
        logging.warning(f"Data no vàlida: {data_str}")
        return False
