import json
import requests
import os
import ctypes
import sys
import configparser
import os
from pathlib import Path
import logging
from PIL import Image
import numpy as np
from py_real_esrgan.model import RealESRGAN
import torch

def main():
    setupApp()

    API_key = leggi_config_ini('./config.ini', 'settings', 'API_keys')
    save_folder = leggi_config_ini('./config.ini', 'settings', 'save_folder')

    params = {'api_key': API_key}
    response = requests.get('https://api.nasa.gov/planetary/apod', params=params)

    response_json = response.json()
    if isError(response_json):
        customStringLog("Errore: "+str(response_json['error']))
        return

    if not isImage(response_json):
        customStringLog("L'evento di oggi non è una immagine. Il wallpaper non sarà modificato")
        return
    
    url_image = response_json["hdurl"]
    tokens = url_image.split("/")
    size = len(tokens)
    filename = save_folder + "" + tokens[size - 1]

    with open(filename, 'wb') as f:
        f.write(requests.get(url_image).content)
    
    img = Image.open(filename)
    logImageData(img, filename)

    if(isToUpscale(img)):
        logging.info("Image to small. Scaling x4:")
        imageScale(filename)
    
    set_wallpaper_ctypes(filename)
    logging.info("##############################################################################################")

def isImage(response_json):
    return "hdurl" in response_json.keys()

def isError(response_json):
    return "error" in response_json.keys()

def customStringLog(message):
    logging.info(message)
    logging.info("##############################################################################################")
    
def imageScale(filename):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = RealESRGAN(device, scale=4)
    model.load_weights('weights/RealESRGAN_x4.pth', download=True)

    image = Image.open(filename).convert('RGB')
    sr_image = model.predict(image)
    sr_image.save(filename)
    logging.info("Scale success! New size: "+str(sr_image.size))

def isToUpscale(img):
    imgSize = img.size
    
    fullHDTotalPixels = 1092*1080
    imgTotalPixels = imgSize[0]*imgSize[1]
    
    if(imgTotalPixels < fullHDTotalPixels):
        return True

    return False

def logImageData(img, filename):
    logging.info(filename)
    logging.info(f"Dimensioni: {img.size}")
    logging.info(f"Dimensioni (pixel totali): "+str(img.size[0]*img.size[1]))
    logging.info(f"Formato: {img.format}")
    logging.info(f"Modalità: {img.mode}")

def set_wallpaper_ctypes(image_path):
    
    # Converte in path assoluto
    image_path = os.path.abspath(image_path)
    
    # Verifica che il file esista
    if not os.path.exists(image_path):
        logging.error(f"Errore: File non trovato: {image_path}")
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
            logging.info(f"Wallpaper impostato con successo: {image_path}")
            return True
        else:
            logging.error("Errore nell'impostazione del wallpaper")
            return False
            
    except Exception as e:
        logging.error(f"Errore: {e}")
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
            logging.error(f"Chiave '{chiave}' non trovata nella sezione '{sezione}'")
            return valore_default
            
    except Exception as e:
        logging.error(f"Errore durante la lettura del file config: {e}")
        return valore_default

def setupApp():
    #nascondi_terminale()
    logging.basicConfig(filename='apod.log',level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

main()