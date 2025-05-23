import sys

# Paràmetres disponibles
PARAMS = {
    '--mode-fosc': False,          # Activa el mode d'interfície fosc
    '--proteccio-ulls': False,     # Activa el mode de protecció ocular (filtre groc)
    '--lupa': False,               # Activa el mode lupa (incrementa la mida del text)
    '--alt-contrast': False,       # Activa el mode d'alt contrast
    '--minim': False              # Obre l'aplicació minimitzada
}

def processar_parametres():
    for arg in sys.argv[1:]:
        if arg in PARAMS:
            PARAMS[arg] = True

def obtenir_parametre(nom):
    return PARAMS.get(nom, False)