# -*- coding: utf-8 -*-
"""
cesc_py
"""

def combine_dictDB(dicts = []):
    '''
    AJUNTA LES DOS BD DE FUTURS I INDEXS EN UN SOL DICCIONARI
    '''
    
    data_combined = dicts[0].copy()
    for i, dic in enumerate(dicts[:-1]):
        data_combined.update(dicts[i+1])
     
    return data_combined

