# -*- coding: utf-8 -*-

import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor 
from matplotlib.widgets import Cursor  
import datetime



def calculate_VIX_ratios(data = ''):
    
    df = data.copy()
    VIX_ratios = {}
    
    # RATIO VIX/VIX3M
    ratio_VIX_VIX3M = pd.merge(df['VIX'][['Date', 'Close']], df['VIX3M'][['Date', 'Close']], on='Date', how='inner')
    ratio_VIX_VIX3M.rename(columns={'Close_x': 'VIX', 'Close_y': 'VIX3M'}, inplace = True)
    ratio_VIX_VIX3M['VIX/VIX3M'] = ratio_VIX_VIX3M['VIX'] / ratio_VIX_VIX3M['VIX3M']
    # Agregar el nuevo dataframe al diccionario de ratios
    VIX_ratios['VIX/VIX3M'] = ratio_VIX_VIX3M

    # RATIO VIX9D/VIX3M
    ratio_VIX9D_VIX3M = pd.merge(df['VIX9D'][['Date', 'Close']], df['VIX3M'][['Date', 'Close']], on='Date', how='inner')
    ratio_VIX9D_VIX3M.rename(columns={'Close_x': 'VIX9D', 'Close_y': 'VIX3M'}, inplace = True)
    ratio_VIX9D_VIX3M['VIX9D/VIX3M'] = ratio_VIX9D_VIX3M['VIX9D'] / ratio_VIX9D_VIX3M['VIX3M']
    # Agregar el nuevo dataframe al diccionario de ratios
    VIX_ratios['VIX9D/VIX3M'] = ratio_VIX9D_VIX3M

    # RATIO VIX9D/VIX
    ratio_VIX9D_VIX = pd.merge(df['VIX9D'][['Date', 'Close']], df['VIX'][['Date', 'Close']], on='Date', how='inner')
    ratio_VIX9D_VIX.rename(columns={'Close_x': 'VIX9D', 'Close_y': 'VIX'}, inplace = True)
    ratio_VIX9D_VIX['VIX9D/VIX'] = ratio_VIX9D_VIX['VIX9D'] / ratio_VIX9D_VIX['VIX']
    # Agregar el nuevo dataframe al diccionario de ratios
    VIX_ratios['VIX9D/VIX'] = ratio_VIX9D_VIX

    return VIX_ratios    
    
def graph_vixratios(data = ''):

    data = data.copy()
    
    date_threshold = datetime.datetime.strptime('2016-01-01', '%Y-%m-%d').date()

    data['VIX9D/VIX3M'] = data['VIX9D/VIX3M'][data['VIX9D/VIX3M']['Date'] > date_threshold]
    data['VIX9D/VIX'] = data['VIX9D/VIX'][data['VIX9D/VIX']['Date'] > date_threshold]
    data['VIX/VIX3M'] = data['VIX/VIX3M'][data['VIX/VIX3M']['Date'] > date_threshold]
    data['SPX']= data['SPX'][data['SPX']['Date'] > date_threshold]
    

    plt.figure(figsize=(12, 6))
    
    # Graficar las series de los dataframes del diccionario
    plt.plot(data['VIX9D/VIX3M']['Date'], data['VIX9D/VIX3M']['VIX9D/VIX3M'], label='VIX9D/VIX3M')
    plt.plot(data['VIX9D/VIX']['Date'], data['VIX9D/VIX']['VIX9D/VIX'], label='VIX9D/VIX')
    plt.plot(data['VIX/VIX3M']['Date'], data['VIX/VIX3M']['VIX/VIX3M'], label='VIX/VIX3M')
    plt.axhline(1, color='r', linestyle='--')   
    
    ax = plt.gca()
    ax2 = ax.twinx()
    ax2.plot(data['SPX']['Date'], data['SPX']['Close'], color='purple', label='SPX Close')
    ax2.set_ylabel('SPX Close', color='purple')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('VIX Ratios and SPX')
    # plt.legend()
    ax.legend()
    
    # multi = MultiCursor(None, (ax, ax2), color='r', lw=1)
    cursor = Cursor(ax2, color='r', lw=1)
    plt.show()