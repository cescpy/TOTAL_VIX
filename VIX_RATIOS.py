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
    pass

    data = data.copy()
    
    date_threshold = datetime.datetime.strptime('2016-01-01', '%Y-%m-%d').date()

    data['VIX9D/VIX3M'] = data['VIX9D/VIX3M'][data['VIX9D/VIX3M']['Date'] > date_threshold]
    data['VIX9D/VIX'] = data['VIX9D/VIX'][data['VIX9D/VIX']['Date'] > date_threshold]
    data['VIX/VIX3M'] = data['VIX/VIX3M'][data['VIX/VIX3M']['Date'] > date_threshold]
    data['SPX']= data['SPX'][data['SPX']['Date'] > date_threshold]
    

    plt.figure(figsize=(12, 6))
    
    # Graficar las series de los dataframes del diccionario
    plt.plot(data['VIX9D/VIX3M']['Date'], data['VIX9D/VIX3M']['VIX9D/VIX3M'], label='VIX9D/VIX3M')
    # plt.plot(data['VIX9D/VIX']['Date'], data['VIX9D/VIX']['VIX9D/VIX'], label='VIX9D/VIX')
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

    
 
    
    
'''
df['VIX_VIX3M'] = df['VIX'] / df['VIX3M']
df['VIX_VVIX'] = df['VIX'] / df['VVIX']

df.dropna(axis= 0, inplace = True)





# Grafico de las series
fig, axs = plt.subplots(2, 1, figsize= (24,14))
fig.suptitle('SERIES', fontsize = 20)

axs[0].grid()
axs[0].plot(df['SPY'], linewidth=1, color= 'blue')
axs[0].set_title('S', fontsize = 18)

axs0 = axs[0].twinx()
axs0.plot(df['VIX'], linewidth=0.5, color = 'grey')
axs0.plot(df['VIX3M'], linewidth=0.5, color = 'red')
axs0.plot(df['VVIX'], linewidth=0.5, color = 'red')   

# axs[0].set_ylim(-5,)

axs[1].grid()
axs[1].plot(df['SPY'], linewidth=1, color= 'blue')
axs[1].set_title('S', fontsize = 18)

axs1 = axs[1].twinx()
axs1.plot(df['VIX_VIX3M'], linewidth=0.5, color = 'grey')
axs1.plot(df['VIX_VVIX'], linewidth=0.5, color = 'red')

axs11 = axs[1].twinx()
axs11.plot(df['VIX'], linewidth=0.5, color = 'green')


# Grafico de las series
fig, axs = plt.subplots(figsize= (24,10))
fig.suptitle('SPY - VIX/VIX3M', fontsize = 20)

axs.grid()
axs.plot(df['SPY'][df.index > '2020-01-01'], linewidth=1, color= 'blue')

axs0.set_ylabel('SPY', color='blue') # agregar etiqueta al  eje
axs0.tick_params(axis='y', labelcolor='blue') # ajustar color de la etiqueta del eje


axs0 = axs.twinx()
axs0.plot(df['VIX_VIX3M'][df.index > '2020-01-01'], linewidth=0.5, color = 'green')

axs0.axhline(y=1, color='red', linestyle='--') # dibujar la línea horizontal
axs0.axhline(y=df['VIX_VIX3M'].mean(), color='grey', linestyle='--') # dibujar la línea horizontal
axs0.axhline(y=0.85, color='red', linestyle='--') # dibujar la línea horizontal

axs0.set_ylabel('VIX_VIX3M', color='green') # agregar etiqueta al segundo eje
axs0.tick_params(axis='y', labelcolor='green') # ajustar color de la etiqueta del segundo eje
   
plt.show()

# (df['VIX'][df.index > '2020-01-01'])
'''