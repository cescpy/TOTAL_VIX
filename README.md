# TOTAL_VIX
 VIX futures and indexes. Mass download and process data 

OJO! Definir el directorio en CURRENT_PATH en el archivo Play_Test_VIX_DATA
(o guardar los archivos en C:\Py\00_PROJECTS\TOTAL_VIX) 

### Play_Test_VIX_DATA
Ejemplos de uso de las funciones


### GET_VIX_DATA_CBOE
 Descarga de la web de CBOE:
 - Lista de todas las fechas de vencimientos de los futuros del VIX
 Descarga de la web de CBOE históricos completos de:
 - Futuros vencidos del VIX
 - Futuros activos del VIX
 - VIX
 - VIX9D
 - VVIX
Descarga de YFinance históricos completos de:
 - VIX3M
 - SPX
Datos de velas diarias

### LOAD_VIX_DATA_CBOE
Carga toda la data descargada en diccionarios de dataframes:
- Diccionario con los dataframes de los futuros activos
- Diccionario con los dataframes de los futuros expirados
- Diccionario con los dataframes de los índices

### VIX_RATIOS
Calculo y graficado del VIX ratio y algo más.
