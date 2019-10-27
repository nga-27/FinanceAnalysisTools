import pandas as pd 
import numpy as np 

import yfinance as yf 

def fetch_api_data(api: dict, data_dict: dict) -> dict:
    period = '2y'
    interval = '1d'
    tickers = api['tickers']

    yf_data = yf.download(tickers=tickers, period=period, interval=interval, group_by='ticker')
    # print(f"data keys: {yf_data.keys()}")
    clean_data = {}
    key_list = api['tickers'].split(' ')
    for key in key_list: 
        clean_data[key] = {}
        dat = yf_data.get(key, {}).get('Open')
        if dat is not None:
            clean_data[key]['Date'] = yf_data.get(key).index.copy()
            clean_data[key]['Open'] = yf_data.get(key).get('Open').copy()
            clean_data[key]['Close'] = yf_data.get(key).get('Close').copy()
            clean_data[key]['High'] = yf_data.get(key).get('High').copy()
            clean_data[key]['Low'] = yf_data.get(key).get('Low').copy()
            clean_data[key]['Volume'] = yf_data.get(key).get('Volume').copy()
            clean_data[key]['Adj Close'] = yf_data.get(key).get('Adj Close').copy()
        else:
            clean_data.pop(key)

    data_dict['download_data'] = clean_data

    return data_dict