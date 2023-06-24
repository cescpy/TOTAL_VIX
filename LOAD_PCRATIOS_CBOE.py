# -*- coding: utf-8 -*-
"""
Cesc_py
"""
import pandas as pd
import datetime 
import time
import os
import requests
import re
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor 
from matplotlib.widgets import Cursor  

current_path = CURRENT_PATH









'''
CARREGAR ARXIUS HISTORICS (PRIMER COP)
https://www.cboe.com/us/options/market_statistics/historical_data/
'''
# CARREGAR LA DATA D'ARXIU
os.chdir(current_path + '\\PC_RATIOS_DATA')  
list_files = os.listdir()
# Filtrar los elementos que empiezan con "PC"
list_current = [elemento for elemento in list_files if elemento.startswith("HIST")]

historicos_pc_ratios = {}
for file in list_current:
    df = pd.read_csv(file)
    df['Date'] = pd.to_datetime(df['Date']).dt.date 
    id_pc = file.split('.')[0]    
    # Guardar el dataframe al diccionari
    historicos_pc_ratios[id_pc] = df         
     

'''
SCRAPER DATA NOVA - INICI 2019-10-07 (PRIMER COP)
https://cdn.cboe.com/data/us/options/market_statistics/daily/2019-10-07_daily_options
'''

df_total = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
df_index = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
df_etp = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
df_equity = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
df_VIX = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
df_SPX = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
df_OEX = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
df_RUT = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])

init_date = '2019-10-07'
long_spx = yf.download('^SPX', start = init_date)
long_spx['Date'] = long_spx.index
long_spx['Date'] = long_spx['Date'].astype(str)
date_list = list(long_spx['Date'])


for date in date_list[:-1]: 
    url = f"https://cdn.cboe.com/data/us/options/market_statistics/daily/{date}_daily_options"
    response = requests.get(url)
    content = response.text
    # contentjson = response.json()
    # Extraer del archivo
    PC = re.findall(r'"value": "(.{4})', content)
    PC = [float(value) for value in PC]
    CALL = re.findall(r'"call": ([^,]+)', content)
    CALL = [int(value) for value in CALL]
    PUT = re.findall(r'"put": ([^,]+)', content)
    PUT = [int(value) for value in PUT]
    TOTAL = re.findall(r'"total": ([^\n]+)', content)
    TOTAL = [int(value) for value in TOTAL]
    
    PC_total = {'Date': date, 'PC_RATIO': PC[0], 'VOL_CALL': CALL[0], 'OI_CALL': CALL[1], 'VOL_PUT': PUT[0], 'OI_PUT': PUT[1], 'VOL_TOTAL': TOTAL[0], 'OI_TOTAL': TOTAL[1]}
    df_total.loc[len(df_total)] = PC_total
    PC_index = {'Date': date, 'PC_RATIO': PC[1], 'VOL_CALL': CALL[2], 'OI_CALL': CALL[3], 'VOL_PUT': PUT[2], 'OI_PUT': PUT[3], 'VOL_TOTAL': TOTAL[2], 'OI_TOTAL': TOTAL[3]}
    df_index.loc[len(df_index)] = PC_index
    PC_etp = {'Date': date, 'PC_RATIO': PC[2], 'VOL_CALL': CALL[4], 'OI_CALL': CALL[5], 'VOL_PUT': PUT[4], 'OI_PUT': PUT[5], 'VOL_TOTAL': TOTAL[4], 'OI_TOTAL': TOTAL[5]}
    df_etp.loc[len(df_etp)] = PC_etp
    PC_equity = {'Date': date, 'PC_RATIO': PC[3], 'VOL_CALL': CALL[6], 'OI_CALL': CALL[7], 'VOL_PUT': PUT[6], 'OI_PUT': PUT[7], 'VOL_TOTAL': TOTAL[6], 'OI_TOTAL': TOTAL[7]}
    df_equity.loc[len(df_equity)] = PC_equity
    PC_VIX = {'Date': date, 'PC_RATIO': PC[4], 'VOL_CALL': CALL[8], 'OI_CALL': CALL[9], 'VOL_PUT': PUT[8], 'OI_PUT': PUT[9], 'VOL_TOTAL': TOTAL[8], 'OI_TOTAL': TOTAL[9]}
    df_VIX.loc[len(df_VIX)] = PC_VIX
    PC_SPX = {'Date': date, 'PC_RATIO': PC[5], 'VOL_CALL': CALL[10], 'OI_CALL': CALL[11], 'VOL_PUT': PUT[10], 'OI_PUT': PUT[11], 'VOL_TOTAL': TOTAL[10], 'OI_TOTAL': TOTAL[11]}
    df_SPX.loc[len(df_SPX)] = PC_SPX
    PC_OEX = {'Date': date, 'PC_RATIO': PC[6], 'VOL_CALL': CALL[12], 'OI_CALL': CALL[13], 'VOL_PUT': PUT[12], 'OI_PUT': PUT[13], 'VOL_TOTAL': TOTAL[12], 'OI_TOTAL': TOTAL[13]}
    df_OEX.loc[len(df_OEX)] = PC_OEX
    PC_RUT = {'Date': date, 'PC_RATIO': PC[7], 'VOL_CALL': CALL[14], 'OI_CALL': CALL[15], 'VOL_PUT': PUT[14], 'OI_PUT': PUT[15], 'VOL_TOTAL': TOTAL[14], 'OI_TOTAL': TOTAL[15]}
    df_RUT.loc[len(df_RUT)] = PC_RUT
    time.sleep(2)

df_total['Date'] = pd.to_datetime(df_total['Date']).dt.date
df_index['Date'] = pd.to_datetime(df_index['Date']).dt.date
df_etp['Date'] = pd.to_datetime(df_etp['Date']).dt.date
df_equity['Date'] = pd.to_datetime(df_equity['Date']).dt.date
df_VIX['Date'] = pd.to_datetime(df_VIX['Date']).dt.date
df_SPX['Date'] = pd.to_datetime(df_SPX['Date']).dt.date
df_OEX['Date'] = pd.to_datetime(df_OEX['Date']).dt.date
df_RUT['Date'] = pd.to_datetime(df_RUT['Date']).dt.date

# SALVAR A csv
df_total.to_csv('df_total.csv', index=False) 
df_index.to_csv('df_index.csv', index=False) 
df_etp.to_csv('df_etp.csv', index=False) 
df_equity.to_csv('df_equity.csv', index=False) 
df_VIX.to_csv('df_VIX.csv', index=False) 
df_SPX.to_csv('df_SPX.csv', index=False) 
df_OEX.to_csv('df_OEX.csv', index=False) 
df_RUT.to_csv('df_RUT.csv', index=False) 


'''
ACTUALITZAR ARXIUS csv AMB LES NOVES DADES (1ER COP)
'''
PCR_equity = pd.concat([historicos_pc_ratios['HIST_equity'], df_equity], ignore_index=True)
PCR_etp = pd.concat([historicos_pc_ratios['HIST_etp'], df_etp], ignore_index=True)
PCR_index = pd.concat([historicos_pc_ratios['HIST_index'], df_index], ignore_index=True)
PCR_SPX = pd.concat([historicos_pc_ratios['HIST_SPX'], df_SPX], ignore_index=True)
PCR_total = pd.concat([historicos_pc_ratios['HIST_total'], df_total], ignore_index=True)
PCR_VIX = pd.concat([historicos_pc_ratios['HIST_VIX'], df_VIX], ignore_index=True)
PCR_OEX = df_OEX.copy()
PCR_RUT = df_RUT.copy()

PCR_total.to_csv('PCR_total.csv', index=False) 
PCR_index.to_csv('PCR_index.csv', index=False) 
PCR_etp.to_csv('PCR_etp.csv', index=False) 
PCR_equity.to_csv('PCR_equity.csv', index=False) 
PCR_VIX.to_csv('PCR_VIX.csv', index=False) 
PCR_SPX.to_csv('PCR_SPX.csv', index=False) 
PCR_OEX.to_csv('PCR_OEX.csv', index=False) 
PCR_RUT.to_csv('PCR_RUT.csv', index=False) 



def update_PCR_archive(current_path = ''):

    current_path = current_path
    
    os.chdir(current_path + '\\PC_RATIOS_DATA')  
    df_archive = pd.read_csv('PCR_total.csv')
    
    end_hist_date = df_archive['Date'].iloc[-1]
    end_hist_date = datetime.datetime.strptime(end_hist_date, '%Y-%m-%d')
    init_update_date = end_hist_date + datetime.timedelta(days=1)
    init_update_date = init_update_date.strftime('%Y-%m-%d')  

    long_spx = yf.download('^SPX', start = '2023-06-01')
    long_spx['Date'] = long_spx.index
    long_spx['Date'] = long_spx['Date'].astype(str)
    date_list = list(long_spx['Date'])


    df_total = pd.DataFrame(columns=['Date', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'PC_RATIO', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
    df_index = pd.DataFrame(columns=['Date', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL','PC_RATIO',  'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
    df_etp = pd.DataFrame(columns=['Date', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'PC_RATIO', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
    df_equity = pd.DataFrame(columns=['Date', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'PC_RATIO', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
    df_VIX = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
    df_SPX = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
    df_OEX = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])
    df_RUT = pd.DataFrame(columns=['Date', 'PC_RATIO', 'VOL_CALL', 'VOL_PUT', 'VOL_TOTAL', 'OI_CALL', 'OI_PUT', 'OI_TOTAL'])


    for date in date_list[:-1]: 
        url = f"https://cdn.cboe.com/data/us/options/market_statistics/daily/{date}_daily_options"
        response = requests.get(url)
        content = response.text
        # contentjson = response.json()
        # Extraer del archivo
        PC = re.findall(r'"value": "(.{4})', content)
        PC = [float(value) for value in PC]
        CALL = re.findall(r'"call": ([^,]+)', content)
        CALL = [int(value) for value in CALL]
        PUT = re.findall(r'"put": ([^,]+)', content)
        PUT = [int(value) for value in PUT]
        TOTAL = re.findall(r'"total": ([^\n]+)', content)
        TOTAL = [int(value) for value in TOTAL]
        
        PC_total = {'Date': date, 'PC_RATIO': PC[0], 'VOL_CALL': CALL[0], 'OI_CALL': CALL[1], 'VOL_PUT': PUT[0], 'OI_PUT': PUT[1], 'VOL_TOTAL': TOTAL[0], 'OI_TOTAL': TOTAL[1]}
        df_total.loc[len(df_total)] = PC_total
        PC_index = {'Date': date, 'PC_RATIO': PC[1], 'VOL_CALL': CALL[2], 'OI_CALL': CALL[3], 'VOL_PUT': PUT[2], 'OI_PUT': PUT[3], 'VOL_TOTAL': TOTAL[2], 'OI_TOTAL': TOTAL[3]}
        df_index.loc[len(df_index)] = PC_index
        PC_etp = {'Date': date, 'PC_RATIO': PC[2], 'VOL_CALL': CALL[4], 'OI_CALL': CALL[5], 'VOL_PUT': PUT[4], 'OI_PUT': PUT[5], 'VOL_TOTAL': TOTAL[4], 'OI_TOTAL': TOTAL[5]}
        df_etp.loc[len(df_etp)] = PC_etp
        PC_equity = {'Date': date, 'PC_RATIO': PC[3], 'VOL_CALL': CALL[6], 'OI_CALL': CALL[7], 'VOL_PUT': PUT[6], 'OI_PUT': PUT[7], 'VOL_TOTAL': TOTAL[6], 'OI_TOTAL': TOTAL[7]}
        df_equity.loc[len(df_equity)] = PC_equity
        PC_VIX = {'Date': date, 'PC_RATIO': PC[4], 'VOL_CALL': CALL[8], 'OI_CALL': CALL[9], 'VOL_PUT': PUT[8], 'OI_PUT': PUT[9], 'VOL_TOTAL': TOTAL[8], 'OI_TOTAL': TOTAL[9]}
        df_VIX.loc[len(df_VIX)] = PC_VIX
        PC_SPX = {'Date': date, 'PC_RATIO': PC[5], 'VOL_CALL': CALL[10], 'OI_CALL': CALL[11], 'VOL_PUT': PUT[10], 'OI_PUT': PUT[11], 'VOL_TOTAL': TOTAL[10], 'OI_TOTAL': TOTAL[11]}
        df_SPX.loc[len(df_SPX)] = PC_SPX
        PC_OEX = {'Date': date, 'PC_RATIO': PC[6], 'VOL_CALL': CALL[12], 'OI_CALL': CALL[13], 'VOL_PUT': PUT[12], 'OI_PUT': PUT[13], 'VOL_TOTAL': TOTAL[12], 'OI_TOTAL': TOTAL[13]}
        df_OEX.loc[len(df_OEX)] = PC_OEX
        PC_RUT = {'Date': date, 'PC_RATIO': PC[7], 'VOL_CALL': CALL[14], 'OI_CALL': CALL[15], 'VOL_PUT': PUT[14], 'OI_PUT': PUT[15], 'VOL_TOTAL': TOTAL[14], 'OI_TOTAL': TOTAL[15]}
        df_RUT.loc[len(df_RUT)] = PC_RUT
        time.sleep(2)
    
    df_total['Date'] = pd.to_datetime(df_total['Date']).dt.date
    df_index['Date'] = pd.to_datetime(df_index['Date']).dt.date
    df_etp['Date'] = pd.to_datetime(df_etp['Date']).dt.date
    df_equity['Date'] = pd.to_datetime(df_equity['Date']).dt.date
    df_VIX['Date'] = pd.to_datetime(df_VIX['Date']).dt.date
    df_SPX['Date'] = pd.to_datetime(df_SPX['Date']).dt.date
    df_OEX['Date'] = pd.to_datetime(df_OEX['Date']).dt.date
    df_RUT['Date'] = pd.to_datetime(df_RUT['Date']).dt.date

    # AFEGIR NOVA DATA ALS CVS 'PCR'
    df_total.to_csv('PCR_total.csv', index=False, mode='a', header=False)
    df_index.to_csv('PCR_index.csv', index=False, mode='a', header=False)
    df_etp.to_csv('PCR_etp.csv', index=False, mode='a', header=False)
    df_equity.to_csv('PCR_equity.csv', index=False, mode='a', header=False)
    df_VIX.to_csv('PCR_VIX.csv', index=False, mode='a', header=False)
    df_SPX.to_csv('PCR_SPX.csv', index=False, mode='a', header=False)
    df_OEX.to_csv('PCR_OEX.csv', index=False, mode='a', header=False)
    df_RUT.to_csv('PCR_RUT.csv', index=False, mode='a', header=False)
    

def load_PCR_data(current_path = ''):

    current_path = current_path
    os.chdir(current_path + '\\PC_RATIOS_DATA') 

    df_total = pd.read_csv('PCR_total.csv')
    df_index = pd.read_csv('PCR_index.csv')
    df_etp = pd.read_csv('PCR_etp.csv')
    df_equity = pd.read_csv('PCR_equity.csv')
    df_VIX = pd.read_csv('PCR_VIX.csv')
    df_SPX = pd.read_csv('PCR_SPX.csv')
    df_OEX = pd.read_csv('PCR_OEX.csv')
    df_RUT = pd.read_csv('PCR_RUT.csv')
    
    
def process_PCR_data():  
    pass


def graph_PCR_data():
    
    date_threshold = datetime.datetime.strptime('2022-06-01', '%Y-%m-%d').date()
    df_total['Date'] = pd.to_datetime(df_total['Date']).dt.date
    df_index['Date'] = pd.to_datetime(df_index['Date']).dt.date
    df_etp['Date'] = pd.to_datetime(df_etp['Date']).dt.date
    df_equity['Date'] = pd.to_datetime(df_equity['Date']).dt.date
    df_VIX['Date'] = pd.to_datetime(df_VIX['Date']).dt.date
    df_SPX['Date'] = pd.to_datetime(df_SPX['Date']).dt.date
    df_OEX['Date'] = pd.to_datetime(df_OEX['Date']).dt.date
    df_RUT['Date'] = pd.to_datetime(df_RUT['Date']).dt.date
    
    data = yf.download(['^SPX', '^VIX'], start = '2003-10-17')['Close']
    data['Date'] = data.index.copy()
    data.columns = ['SPX', 'VIX', 'Date']
    data = data[['Date', 'SPX', 'VIX']]
    
    data['Date'] = pd.to_datetime(data['Date']).dt.date

    df = pd.DataFrame()
    df['Date']= data[data['Date'] > date_threshold]['Date']
    df['SPX']= data[data['Date'] > date_threshold]['SPX']
    df['VIX']= data[data['Date'] > date_threshold]['VIX']
    
    
    df_total.index = df_total['Date']
    df_total.index = pd.to_datetime(df_total.index)
    # df = df.join(df_total['PC_RATIO']).add_suffix('_total')
    df = df.merge(df_total[['PC_RATIO']], left_index=True, right_index=True, how='left', suffixes=('', '_total'))
    
    df_index.index = df_index['Date']
    df_index.index = pd.to_datetime(df_index.index)
    df = df.merge(df_index[['PC_RATIO']], left_index=True, right_index=True, how='left', suffixes=('', '_index'))

    df_equity.index = df_equity['Date']
    df_equity.index = pd.to_datetime(df_equity.index)
    df = df.merge(df_equity[['PC_RATIO']], left_index=True, right_index=True, how='left', suffixes=('', '_equity'))
    
    df_SPX.index = df_SPX['Date']
    df_SPX.index = pd.to_datetime(df_SPX.index)
    df = df.merge(df_SPX[['PC_RATIO']], left_index=True, right_index=True, how='left', suffixes=('', '_SPX'))

    df_VIX.index = df_VIX['Date']
    df_VIX.index = pd.to_datetime(df_VIX.index)
    df = df.merge(df_VIX[['PC_RATIO']], left_index=True, right_index=True, how='left', suffixes=('', '_VIX'))
    
    df_OEX.index = df_OEX['Date']
    df_OEX.index = pd.to_datetime(df_OEX.index)
    df = df.merge(df_OEX[['PC_RATIO']], left_index=True, right_index=True, how='left', suffixes=('', '_OEX'))   
    
    df_etp.index = df_etp['Date']
    df_etp.index = pd.to_datetime(df_etp.index)
    df = df.merge(df_etp[['PC_RATIO']], left_index=True, right_index=True, how='left', suffixes=('', '_etp'))       
    
    df_RUT.index = df_RUT['Date']
    df_RUT.index = pd.to_datetime(df_RUT.index)
    df = df.merge(df_RUT[['PC_RATIO']], left_index=True, right_index=True, how='left', suffixes=('', '_RUT'))   

## Grafic
    plt.figure(figsize=(12, 6))
    
    # Graficar las series de los dataframes del diccionario
    plt.plot(df.index, df['PC_RATIO'], label='PC_RATIO')
    plt.plot(df.index, df['PC_RATIO_index'], label='PC_RATIO_index')
    plt.plot(df.index, df['PC_RATIO_equity'], label='PC_RATIO_equity')
    plt.plot(df.index, df['PC_RATIO_SPX'], label='PC_RATIO_SPX')
    # plt.plot(df.index, df['PC_RATIO_VIX'], label='PC_RATIO_VIX')
    # plt.plot(df.index, df['PC_RATIO_OEX'], label='PC_RATIO_OEX')
    # plt.plot(df.index, df['PC_RATIO_etp'], label='PC_RATIO_etp')
    plt.axhline(1, color='r', linestyle='--') 
    plt.axhline(2, color='r', linestyle='--')  
    
    ax = plt.gca()
    ax2 = ax.twinx()
    ax2.plot(df.index, df['SPX'], color='purple', label='SPX Close')
    ax2.set_ylabel('SPX Close', color='purple')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.title('P/C Ratios and SPX')
    # plt.legend()
    ax.legend()
    
    # multi = MultiCursor(None, (ax, ax2), color='r', lw=1)
    cursor = Cursor(ax2, color='r', lw=1)
    plt.show()
 
    
correl = df.iloc[: ,3:].corr()   
    
    
    
    