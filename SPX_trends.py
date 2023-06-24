# -*- coding: utf-8 -*-
"""
Cesc_py
"""
import pandas as pd
import numpy as np
import datetime 
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor 
from matplotlib.widgets import Cursor  


SPX_trends = pd.DataFrame(yf.download('^SPX', start = '1995-01-01')).add_suffix('_SPX')
SPX_trends.index = pd.to_datetime(SPX_trends.index)

SPX_trends['Primary'] = 0
SPX_trends['Secondary'] = 0


SPX_trends.loc['2022-10-14':'2023-06-20', 'Primary'] = 1
SPX_trends.loc['2023-03-14':'2023-06-16', 'Secondary'] = 1
SPX_trends.loc['2023-02-03':'2023-03-13', 'Secondary'] = -1
SPX_trends.loc['2022-12-28': '2023-02-02', 'Secondary'] = 1
SPX_trends.loc['2022-11-30': '2022-12-27', 'Secondary'] = -1
SPX_trends.loc['2022-10-14': '2022-12-01', 'Secondary'] = 1
SPX_trends.loc['2022-08-17': '2022-10-13', 'Secondary'] = -1
SPX_trends.loc['2022-06-21': '2022-08-16', 'Secondary'] = 1
SPX_trends.loc['2022-06-03': '2022-06-20', 'Secondary'] = -1
SPX_trends.loc['2022-05-23': '2022-06-02', 'Secondary'] = 1
SPX_trends.loc['2022-03-30': '2022-05-22', 'Secondary'] = -1
SPX_trends.loc['2022-03-13': '2022-03-29', 'Secondary'] = 1
SPX_trends.loc['2022-01-05': '2022-03-14', 'Secondary'] = -1
SPX_trends.loc['2021-12-03': '2022-01-04', 'Secondary'] = 1






# Grafico linea colores
t = SPX_trends.index
f = SPX_trends['Secondary']
s = SPX_trends['Close_SPX']

inrange = np.ma.masked_where(f == 0, s)
bullish = np.ma.masked_where(f == 1, s)
bearish = np.ma.masked_where(f == -1, s)

fig, ax = plt.subplots()
ax.plot(t, inrange, color = 'blue', label='In range')
ax.plot(t, bearish, color = 'green', label='Bearish')
ax.plot(t, bullish, color = 'red', label='Bullish')

ax.legend()
plt.show()






# Grafico linea
fig, ax = plt.subplots()

# Configurar el color de la línea en función de SPX_trends['Secondary']
# color = ['green' if val == 1 else 'red' if val == -1 else 'blue' for val in SPX_trends['Secondary']]
# color = np.where(SPX_trends['Secondary'] == 1, 'green', np.where(SPX_trends['Secondary'] == -1, 'red', 'blue'))
# Plot the SPX_trends['Close'] column
ax.plot(SPX_trends.index, SPX_trends['Close_SPX'], color='blue', linewidth=1)


# Configurar los títulos y etiquetas
ax.set_title('Gráfico de SPX_trends')
ax.set_xlabel('Fecha')
ax.set_ylabel('Close')

# Mostrar el gráfico
plt.show()



##############################
# Grafico linea puntos colores
fig, ax = plt.subplots()

ax.plot(SPX_trends.index, SPX_trends['Close_SPX'], color='blue', linewidth=1)
# Iterate over the dataframe rows
for index, row in SPX_trends.iterrows():
    # Determine the color based on SPX_trends['Secondary']
    if row['Secondary'] == 1:
        color = 'green'
    elif row['Secondary'] == -1:
        color = 'red'
    else:
        color = 'blue'
    
    # Plot the data point with the assigned color
    ax.plot(index, row['Close_SPX'], marker = '.', color=color)

# Configure titles and labels
ax.set_title('SPX_trends["Close"] Chart')
ax.set_xlabel('Date')
ax.set_ylabel('Close')

# Show the plot
plt.show()





