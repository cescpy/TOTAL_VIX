# -*- coding: utf-8 -*-
"""
DESCARGA DE DATOS DE FUTUROS VIX E INDICES VIX

Els arxius csv es descarreguen de la web: https://www.cboe.com/us/futures/market_statistics/historical_data/
"""

import yfinance as yf
import datetime
import os
import requests
import re


def del_VIX_Data(path):
    print("Borrado de csv's antiguos")
    os.chdir(path)
    archivos = os.listdir()
    # Iterar sobre los archivos y eliminarlos uno por uno
    for archivo in archivos:
        ruta_archivo = os.path.join(path, archivo)
        os.remove(ruta_archivo)


def get_VIXfut_expiries(expiry_period = 'mo', is_current = True, is_expired = True):
# Obtener el contenido HTML de la página web
    url = "https://www.cboe.com/us/futures/market_statistics/historical_data/"
    response = requests.get(url)
    html_content = response.text
    html_content = html_content.replace('"', '')
    
    # Buscar los enlaces ".csv" y extraer los nombres de archivo
    if expiry_period == 'wk':
        # Tots els venciments
        expiry_list = re.findall(r'futures/market_statistics/historical_data/VX/VX_(.{10})', html_content)
    if expiry_period == 'mo':
        # Venciments mensuals
        expiry_list = re.findall(r'duration_type:M,path:data/us/futures/market_statistics/historical_data/VX/VX_(.{10})', html_content)

    current_date = datetime.date.today()
    if is_current == True and is_expired == False:    
        expiry_list = [expiry_date for expiry_date in expiry_list if datetime.datetime.strptime(expiry_date, '%Y-%m-%d').date() > current_date]
    elif is_current == False and is_expired == True:
        expiry_list = [expiry_date for expiry_date in expiry_list if datetime.datetime.strptime(expiry_date, '%Y-%m-%d').date() <= current_date]
    else:
        print('Lista creada con todos los vencimientos disponibles./n Tambien puede seleccionar los parámetros True o False en is_expiry y is_current')
        
    expiry_list.sort(reverse = True)
        
    return expiry_list # csv_list

def download_VIXfutures(expiry_list = [], clean_path = False, current_path = ''):
    '''
    DESCARREGA ELS csv DE DADES DELS FUTURS
    DE LA WEB https://cdn.cboe.com/data/us/futures/market_statistics/historical_data
    '''
    # Definir directori VIX_DATA
    CURRENT_PATH = current_path    
    path_data = "\\VIX_DATA" 
    path = CURRENT_PATH + path_data
    
    # Si el directorio VIX_DATA no existe, se crea
    if not os.path.exists(path):
        os.mkdir(path)        
    os.chdir(path)
   
    #Si s'ha seleccionart esborrar data antiga
    if clean_path == True:
        del_VIX_Data(path = path)
    
    # Descarregar csv's
    urlbase = "https://cdn.cboe.com/data/us/futures/market_statistics/historical_data/VX/"

    # DESCARREGUEM ELS ARXIUS
    current_date = datetime.date.today()
    current_expiry_list = [expiry_date for expiry_date in expiry_list if datetime.datetime.strptime(expiry_date, '%Y-%m-%d').date() > current_date]
    current_expiry_list.sort(reverse = False)
    past_expiry_list = [expiry_date for expiry_date in expiry_list if datetime.datetime.strptime(expiry_date, '%Y-%m-%d').date() <= current_date]

    i = 1
    for expiry in current_expiry_list: 
        filename = 'FUT_' + str(i) + '_' + expiry + '.csv'
        i +=1 
        url= urlbase + 'VX_' + expiry + '.csv'
        response = requests.get(url)
        # Si el archivo ya existe, se sobrescribe
        with open(filename, "wb") as f:
            f.write(response.content)       
        print(f"Archivo {filename} descargado exitosamente en {path}") 


    for expiry in past_expiry_list: 
        filename = 'VX_' + expiry + '.csv'
        url= urlbase + 'VX_' + expiry + '.csv'
        response = requests.get(url)
        # Si el archivo ya existe, se sobrescribe
        with open(filename, "wb") as f:
            f.write(response.content)       
        print(f"Archivo {filename} descargado exitosamente en {path}")    
    
def download_VIXindexes(current_path = ''):
    '''
    DESCARREGA ELS csv DE DADES DELS INDEX VIX, VI9D I VVIX
    DE LA WEB https://cdn.cboe.com/data/us/futures/market_statistics/historical_data
    '''    
    # Definir directori VIX_DATA
    CURRENT_PATH = current_path    
    path_data = "\\VIX_DATA" 
    path = CURRENT_PATH + path_data
    
    # Si el directorio VIX_DATA no existe, se crea
    if not os.path.exists(path):
        os.mkdir(path)        
    os.chdir(path)
    
    # URL's BASE DELS HISTORICS DEL VIX INDEX
    urlbase = "https://cdn.cboe.com/api/global/us_indices/daily_prices/"
    urlVIX = "VIX_History.csv"
    urlVVIX = "VVIX_History.csv"
    urlVIX9D = "VIX9D_History.csv"
    # Diccionari de url's, la clau es el nom amb el que es guarda l'arxiu i el valor la url del arxiu per descarregar
    urls = {"VIX.csv": urlbase + urlVIX , "VVIX.csv": urlbase + urlVVIX, "VIX9D.csv": urlbase + urlVIX9D}
    
    # DESCARREGUEM ELS ARXIUS
    for filenames, url in urls.items(): 
        # NOM DE CADA ARXIU
        filename = filenames
        response = requests.get(url)  
        # Si el archivo ya existe, se sobrescribe el contenido
        with open(filename, "wb") as f:
            f.write(response.content)       
        print(f"Archivo {filename} descargado exitosamente en {path}")
    
    # DESCARGA DEL VIX3M (DESDE YFINANCE)
    ruta = path + '\\VIX3M.csv'
    yf.download('^VIX3M', period = 'max', interval = '1d').to_csv(ruta, index=True)
    # df.to_csv(ruta, index=True)
    print(f"Archivo {ruta} descargado exitosamente")
