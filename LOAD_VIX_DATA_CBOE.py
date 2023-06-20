# -*- coding: utf-8 -*-
"""
Cesc_py
"""
import pandas as pd
import datetime
import os
import requests
import re


def load_current_VIXfutures(current_path = ''):

    # Definir el directori on estan els arxius CSV
    os.chdir(current_path + '\\VIX_DATA')  
    list_files = os.listdir()
    # Filtrar los elementos que empiezan con "FUT"
    list_current = [elemento for elemento in list_files if elemento.startswith("FUT")]

    # CREO DICCIONARIO DE CURRENT FUTUROS
    data_current_futures = {}
    for i, file in enumerate(list_current):
        df = pd.read_csv(file, usecols=['Trade Date', 'Futures', 'Open', 'High', 'Low', 'Close', 'Settle'], dtype={'Futures': str})
        df = df.rename(columns={'Trade Date': 'Date', 'Futures': 'id_fut', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Settle': 'Liqclose'})
        # Defineix el nom del venciment aaaa_mm i posicio temporal del futur
        id_fut = list_current[i][6:10] + '_' +  list_current[i][11:13]
        position_fut = list_current[i][4:5]
        df['id_fut'] = id_fut
        df['position_fut'] = position_fut #i+1

        # NETEJA DE LES DADES
        # Ceros o nulos se reemplaza toda la fila por el 'Liqclose'
        mask = df[['Open', 'High', 'Low', 'Close']].isin([0, None]).any(axis=1)
        df.loc[mask, ['Open', 'High', 'Low', 'Close']] = df.loc[mask, 'Liqclose']
        df.drop('Liqclose', axis=1, inplace=True)
        df= df.reset_index(drop=True)
        
        # Posem els valors de la columna 'date' com a dates aaaa-mm-dd
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        # Reordeno les columnes
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'id_fut', 'position_fut']]
        
        # Guardar el dataframe al diccionari
        data_current_futures[id_fut] = df        

    return data_current_futures 



def load_expired_VIXfutures(current_path = ''):    

    # Definir el directori on estan els arxius CSV
    os.chdir(current_path + '\\VIX_DATA')  
    list_files = os.listdir()
    # Filtrar los elementos que empiezan con "VX"
    list_expired = [elemento for elemento in list_files if elemento.startswith("VX")]

    # CREO DICCIONARIO DE EXPIRED FUTUROS
    data_expired_futures = {}
    for i, file in enumerate(list_expired):
        df = pd.read_csv(file, usecols=['Trade Date', 'Futures', 'Open', 'High', 'Low', 'Close', 'Settle'], dtype={'Futures': str})
        df = df.rename(columns={'Trade Date': 'Date', 'Futures': 'id_fut', 'Open': 'Open', 'High': 'High', 'Low': 'Low', 'Close': 'Close', 'Settle': 'Liqclose'})
        # Defineix el nom del venciment aaaa_mm
        id_fut = list_expired[i][3:7] + '_' +  list_expired[i][8:10]
        df['id_fut'] = id_fut

        # NETEJA DE LES DADES
        # Ceros o nulos se reemplaza toda la fila por el 'Liqclose'
        mask = df[['Open', 'High', 'Low', 'Close']].isin([0, None]).any(axis=1)
        df.loc[mask, ['Open', 'High', 'Low', 'Close']] = df.loc[mask, 'Liqclose']
        df.drop('Liqclose', axis=1, inplace=True)
        df= df.reset_index(drop=True)
        
        # Posem els valors de la columna 'date' com a dates aaaa-mm-dd
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        # Reordeno les columnes
        df = df[['Date', 'Open', 'High', 'Low', 'Close', 'id_fut']]
        
        # Guardar el dataframe al diccionari
        data_expired_futures[id_fut] = df        

    return data_expired_futures     
  
    
  
def load_VIXindexs(current_path = ''):    
    
    # Definir el directori on estan els arxius CSV
    os.chdir(current_path + '\\VIX_DATA')  
    list_files = os.listdir()
    # Filtrar los elementos que no empiezan con "FUT" ni "VX"
    list_indexs = [elemento for elemento in list_files if not (elemento.startswith("FUT") or elemento.startswith("VX"))]

    # CREO DICCIONARIO DE INDICES VIX
    data_VIX_indexs = {}
    for i, file in enumerate(list_indexs):
        # Defineix el nom del index
        id_index = list_indexs[i].split(".")[0]

        if id_index == 'SPX' or id_index == 'VIX3M':
            df = pd.read_csv(file, usecols=['Date', 'Open', 'High', 'Low', 'Close'])
        
        if id_index == 'VIX' or id_index == 'VIX9D':
            df = pd.read_csv(file, usecols=['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE'])
            df = df.rename(columns={'DATE': 'Date', 'OPEN': 'Open', 'HIGH': 'High', 'LOW': 'Low', 'CLOSE': 'Close'})

        if id_index == 'VVIX':        
            df = pd.read_csv(file, usecols=['DATE','VVIX'])
            df = df.rename(columns={'DATE': 'Date', 'VVIX': 'Close'})

        df['id_index'] = id_index
        
        # NETEJA DE LES DADES
        df.dropna(inplace=True)
        df= df.reset_index(drop=True)
        
        # Posem els valors de la columna 'date' com a dates aaaa-mm-dd
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        
        # Guardar el dataframe al diccionari
        data_VIX_indexs[id_index] = df        

    return data_VIX_indexs    
    