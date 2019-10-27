import pandas as pd 
import numpy as np 
import os 
import json
import pprint

DROP_COLUMNS = [
    'Unnamed'
]

def get_finance_file_data(core: dict):
    
    finance_filename = core.get('finance file')

    if finance_filename is not None:
        data = get_data(finance_filename)
        data = cleanse_data(data)
        core['api'] = get_tickers(data)
        return data, core
        
    return None, core


def get_data(finance_filename: str) -> dict:
    finance_filename = os.path.join("input/", finance_filename)
    if os.path.exists(finance_filename):

        data = {}
        data['tabular'] = {}
        if finance_filename.split('.')[1] == 'xlsx':
            try:
                xlsx = pd.ExcelFile(finance_filename)
                for sheet in xlsx.sheet_names:
                    data['tabular'][sheet] = xlsx.parse(sheet_name=sheet, index_col='Index')
                return data 
            except:
                print(f"failed to open {finance_filename}")
                return None 

        elif finance_filename.split('.')[1] == 'csv':
            try:
                data['tabular']['sheet'] = pd.read_csv(finance_filename, index_col='Index')
                return data
            except:
                print(f"failed to open {finance_filename}")
    else:
        return None



def cleanse_data(data: dict) -> dict:
    if data is None:
        return None
        
    for tab in data['tabular'].keys():
        drop_cols = []
        for column in data['tabular'][tab].columns:
            for drop in DROP_COLUMNS:
                if drop in column:
                    drop_cols.append(column)
        data['tabular'][tab].drop(columns=drop_cols, inplace=True)
        data['tabular'][tab].dropna(axis='columns', how='all', inplace=True)
    
    return data


def get_tickers(data: dict) -> dict:
    tickers = {}
    potential_tickers = []
    amt_tab = data['tabular'].get('Amount')
    if amt_tab is not None:
        potential_tickers = ticker_filter_totals(amt_tab, potential_tickers) 
        potential_tickers = ticker_filter_dashes(potential_tickers)
        tickers = cluster_tickers(potential_tickers)
    return tickers


############################################
# Ticker filters
############################################

def ticker_filter_totals(tab: pd.DataFrame, ticker_list: list) -> list:
    for col in tab.columns:
        if "Total" in col:
            continue
        elif "Month" in col:
            continue
        elif "total" in col:
            continue
        elif "Cash" in col:
            continue 
        elif "Core" in col:
            continue
        elif "401k" in col:
            # Support only if ticker symbol (likely not)
            continue 
        else:
            ticker_list.append(col)
    
    return ticker_list


def ticker_filter_dashes(ticker_list: list) -> list:
    filtered_list = []
    for col in ticker_list:
        if '-' in col:
            if 'CD' in col:
                continue
            elif 'HSA' in col:
                filtered_list.append(col)
            elif 'IRA' in col:
                filtered_list.append(col)
            else:
                continue
        else:
            filtered_list.append(col)
    return filtered_list


def cluster_tickers(ticker_list: list) -> list:
    clusters = {}
    clusters['tickers'] = ''
    clusters['details'] = []
    for ticker in ticker_list:
        if "-" in ticker:
            tick = ticker.split('-')[1]
            if "HSA" in ticker:
                clusters['tickers'] += tick + " "
                clusters['details'].append({"ticker": tick, "type": "HSA"})
            elif "IRA" in ticker: 
                clusters['tickers'] += tick + " "
                clusters['details'].append({"ticker": tick, "type": "IRA"})
            else:
                continue
        else:
            clusters['tickers'] += ticker + ' '
            clusters['details'].append({"ticker": ticker, "type": "fund"})

    return clusters