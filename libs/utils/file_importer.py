import pandas as pd 
import numpy as np 
import os 
import json

def get_finance_file_data(core: dict):
    
    finance_filename = core.get('finance file')

    if finance_filename is not None:
        data = get_data(finance_filename)
        data = cleanse_data(data)
        return data
        
    return None


def cleanse_data(data: dict) -> dict:
    return data


def get_data(finance_filename: str) -> dict:
    finance_filename = os.path.join("input/", finance_filename)
    if os.path.exists(finance_filename):

        data = {}
        if finance_filename.split('.')[1] == 'xlsx':
            try:
                xlsx = pd.ExcelFile(finance_filename)
                for sheet in xlsx.sheet_names:
                    data[sheet] = xlsx.parse(sheet_name=sheet)
                return data 
            except:
                print(f"failed to open {finance_filename}")
                return None 

        elif finance_filename.split('.')[1] == 'csv':
            try:
                data['sheet'] = pd.read_csv(finance_filename)
                return data
            except:
                print(f"failed to open {finance_filename}")
    else:
        return None