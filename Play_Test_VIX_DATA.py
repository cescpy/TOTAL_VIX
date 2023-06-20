# -*- coding: utf-8 -*-
"""
Cesc_py
"""
# DEFINIR DIRECTORIO DONDE ESTA EL ARCHIVO
CURRENT_PATH = 'C:\\Py\\00_PROJECTS\\TOTAL_VIX'

import os
# CURRENT_PATH = os.getcwd()
os.chdir(CURRENT_PATH)


import GET_VIX_DATA_CBOE as gvd
import LOAD_VIX_DATA_CBOE as pvd


# gvd.del_VIX_Data('C:\\Py\\00_PROJECTS\\TOTAL_VIX\\VIX_DATA')

#DOWNLOAD DATA FUNCTIONS
expiry_list = gvd.get_VIXfut_expiries(expiry_period = 'mo', is_current = True, is_expired = True)
gvd.download_VIXfutures(expiry_list = expiry_list, clean_path = False, current_path = CURRENT_PATH)
gvd.download_VIXindexes(current_path = CURRENT_PATH)

#LOAD AND PROCESS DATA FUNCTIONS
data_current_futures = pvd.load_current_VIXfutures(current_path = CURRENT_PATH)
data_expired_futures = pvd.load_expired_VIXfutures(current_path = CURRENT_PATH)
data_VIX_indexs = pvd.load_VIXindexs(current_path = CURRENT_PATH)



