import pandas as pd 
import numpy as np 
import os 
import json

def get_finance_file_data():
    json_path = 'config.json'
    if os.path.exists(json_path):
        with open(json_path) as json_file:
            core = json.load(json_file)
            finance_filename = core.get('finance file')

            if finance_filename is not None:
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
        print(f"No 'config.json' found. Exiting...")
    return None