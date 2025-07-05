import json
import requests
import os
import ctypes
import sys
import configparser
import os
from pathlib import Path

def main():
    nascondi_terminale()
    API_key = leggi_config_ini('./config.ini', 'settings', 'API_keys')
    save_folder = leggi_config_ini('./config.ini', 'settings', 'save_folder')

    params = {'api_key': API_key}
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)

    response_json = response.json()
    url_image = response_json["hdurl"]
    tokens = url_image.split("/")
    size = len(tokens)
    filename = save_folder + "" + tokens[size - 1]

    with open(filename, 'wb') as f:
        f.write(requests.get(url_image).content)

    set_wallpaper_ctypes(filename)

def set_wallpaper_ctypes(image_path):
    
    # Converte in path assoluto
    image_path = os.path.abspath(image_path)
    
    # Verifica che il file esista
    if not os.path.exists(image_path):
        print(f"Errore: File non trovato: {image_path}")
        return False
    
    # Costanti Windows
    SPI_SETDESKWALLPAPER = 20
    
    try:
        # Chiamata all'API Windows
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            image_path,
            3  # SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
        
        if result:
            print(f"Wallpaper impostato con successo: {image_path}")
            return True
        else:
            print("Errore nell'impostazione del wallpaper")
            return False
            
    except Exception as e:
        print(f"Errore: {e}")
        return False
    
def nascondi_terminale():
    """Nasconde la finestra del terminale su Windows"""
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def leggi_config_ini(percorso_file, sezione, chiave, valore_default=None):

    try:
        config = configparser.ConfigParser()
        config.read(percorso_file, encoding='utf-8')
        
        if sezione in config and chiave in config[sezione]:
            return config[sezione][chiave]
        else:
            print(f"Chiave '{chiave}' non trovata nella sezione '{sezione}'")
            return valore_default
            
    except Exception as e:
        print(f"Errore durante la lettura del file config: {e}")
        return valore_default

main()