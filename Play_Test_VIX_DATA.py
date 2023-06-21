# -*- coding: utf-8 -*-
"""
cesc_py
"""
# DEFINIR DIRECTORIO DONDE ESTA EL ARCHIVO
CURRENT_PATH = 'C:\\Py\\00_PROJECTS\\TOTAL_VIX'

import os
# CURRENT_PATH = os.getcwd()
os.chdir(CURRENT_PATH)

import GET_VIX_DATA_CBOE as gvd
import LOAD_VIX_DATA_CBOE as lvd
import PROCESS_VIX_DATA as pvd
import VIX_RATIOS as vr

#DOWNLOADS DATA. GET DATA FUNCTIONS
# gvd.del_VIX_Data('C:\\Py\\00_PROJECTS\\TOTAL_VIX\\VIX_DATA')
expiry_list = gvd.get_VIXfut_expiries(expiry_period = 'mo', is_current = True, is_expired = True)
gvd.download_VIXfutures(expiry_list = expiry_list, clean_path = False, current_path = CURRENT_PATH)
gvd.download_VIXindexes(current_path = CURRENT_PATH)

#LOADS AND PREPROCESSEDS DATA. LOAD DATA FUNCTIONS
data_current_futures = lvd.load_current_VIXfutures(current_path = CURRENT_PATH)
data_expired_futures = lvd.load_expired_VIXfutures(current_path = CURRENT_PATH)
data_VIX_indexs = lvd.load_VIXindexs(current_path = CURRENT_PATH)

'''
#PROCESSES DATA. PROCESS DATA FUNCTIONS
# Examples combine datas
data_combined_futures = pvd.combine_dictDB(dicts = [data_current_futures, data_expired_futures])
data_combined_total = pvd.combine_dictDB(dicts = [data_current_futures, data_expired_futures, data_VIX_indexs])
data_combined_current = pvd.combine_dictDB(dicts = [data_current_futures, data_VIX_indexs])
data_combined_expired = pvd.combine_dictDB(dicts = [data_expired_futures, data_VIX_indexs])
'''

# CALCULATE VIX RATIOS
VIX_ratios = vr.calculate_VIX_ratios(data = data_VIX_indexs)
data_combined_ratios = pvd.combine_dictDB(dicts = [data_VIX_indexs, VIX_ratios])
vr.graph_vixratios(data = data_combined_ratios)

