import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import sys
import configparser
import os
from pathlib import Path

def cancella_file_vecchi_cartella(percorso_cartella, giorni=30):
    try:
        cartella = Path(percorso_cartella)
        
        if not cartella.exists():
            print(f"La cartella {percorso_cartella} non esiste")
            return
        
        data_limite = datetime.now() - timedelta(days=giorni)
        file_cancellati = 0
        
        for file in cartella.iterdir():
            if file.is_file():
                timestamp_modifica = file.stat().st_mtime
                data_modifica = datetime.fromtimestamp(timestamp_modifica)
                
                if data_modifica < data_limite:
                    try:
                        file.unlink()
                        print(f"Cancellato: {file.name}")
                        file_cancellati += 1
                    except Exception as e:
                        print(f"Errore cancellando {file.name}: {e}")
        
        print(f"Operazione completata. File cancellati: {file_cancellati}")
        
    except Exception as e:
        print(f"Errore durante la scansione della cartella: {e}")

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

if __name__ == "__main__":
    nascondi_terminale()
    percorso_cartella = leggi_config_ini('./config.ini', 'settings', 'save_folder')
    cancella_file_vecchi_cartella(percorso_cartella, giorni=0)