import pandas as pd 
import numpy as np 
import os 
from datetime import datetime

T_KEYS = {
    'contrib': 'Contributions',
    'amount': 'Amount',
    'qty': 'Qty'
}

SKIP_KEYS = [
    'Index',
    'Month'
]


def tabular_stats(data: dict): 
    for key in T_KEYS:
        if T_KEYS[key] not in data.keys():
            print(f"WARNING (Tabular_Stats): Key {key} not found in data. Exiting...")
            return data
    
    gl_period = get_gain_loss_period(data)
    data['Gain_Loss_Period'] = gl_period[0]
    data['Gain_Loss_Period_Percent'] = gl_period[1]

    data['Total_Return'] = total_return(data)
    data['YTD_Return'] = ytd_return(data)

    save_tabular_file(data, filename='finances_output.xlsx')
    return data
    


def get_gain_loss_period(data: dict) -> list:
    """ returns both pd.DataFrame of actual GL amounts and GL percentages """
    gl_percent = {}
    gl_actual = {}

    columns = list(data[T_KEYS['amount']].columns)
    for skip in SKIP_KEYS:
        if skip in columns:
            gl_actual[skip] = data[T_KEYS['amount']][skip]
            gl_percent[skip] = data[T_KEYS['amount']][skip]
            columns.remove(skip)
    for column in columns:
        value = []
        value.append(0.0)
        percent = []
        percent.append(0.0)
        for i in range(1, len(data[T_KEYS['amount']][column])):
            amt = data[T_KEYS['amount']][column][i] - data[T_KEYS['amount']][column][i-1]
            con = data[T_KEYS['contrib']][column][i] - data[T_KEYS['contrib']][column][i-1]
            value.append(amt - con)
            if data[T_KEYS['contrib']][column][i] == 0.0:
                percent.append(0.0)
            else:
                percent.append(np.round(((amt - con) / data[T_KEYS['contrib']][column][i] * 100.0), 3))
        gl_actual[column] = value.copy()
        gl_percent[column] = percent.copy()


    gl_actual_df = pd.DataFrame.from_dict(gl_actual)
    gl_percent_df = pd.DataFrame.from_dict(gl_percent)
    return gl_actual_df, gl_percent_df


def total_return(data:dict) -> pd.DataFrame: 
    tot_ret = {}

    columns = list(data[T_KEYS['amount']].columns)
    for skip in SKIP_KEYS:
        if skip in columns:
            tot_ret[skip] = data[T_KEYS['amount']][skip]
            columns.remove(skip)
    for column in columns:
        percent = []
        for i in range(len(data[T_KEYS['amount']][column])):
            amt = data[T_KEYS['amount']][column][i]
            con = data[T_KEYS['contrib']][column][i]
            if con == 0.0:
                percent.append(0.0)
            else:
                percent.append(np.round(((amt - con) / con * 100.0), 3))
        tot_ret[column] = percent.copy()

    tot_ret_df = pd.DataFrame.from_dict(tot_ret)
    return tot_ret_df


def ytd_return(data: dict) -> pd.DataFrame:
    tot_ret = {}

    columns = list(data[T_KEYS['amount']].columns)
    for skip in SKIP_KEYS:
        if skip in columns:
            tot_ret[skip] = data[T_KEYS['amount']][skip]
            columns.remove(skip)
    for column in columns:
        percent = []
        start_year = pd.to_datetime(tot_ret['Month'][0]).year
        start_amt = data[T_KEYS['amount']][column][0]
        start_con = data[T_KEYS['contrib']][column][0]
        percent.append(0.0)
        for i in range(1, len(data[T_KEYS['amount']][column])):
            yr = pd.to_datetime(tot_ret['Month'][i]).year
            if yr != start_year:
                if i == 0:
                    y = 0
                else:
                    y = i-1
                start_year = yr
                start_amt = data[T_KEYS['amount']][column][y]
                start_con = data[T_KEYS['contrib']][column][y]
                # percent.append(0.0)
            
            amt = data[T_KEYS['amount']][column][i]
            con = data[T_KEYS['contrib']][column][i]
            if con == 0.0:
                percent.append(0.0)
            else:
                c1 = (start_amt + con - start_con)
                a1 = (amt - c1) / c1
                percent.append(np.round(a1 * 100.0, 3))
        tot_ret[column] = percent.copy()

    tot_ret_df = pd.DataFrame.from_dict(tot_ret)
    return tot_ret_df



def save_tabular_file(data: dict, filename='tabular.xlsx'):
    if not os.path.exists('output/'):
        os.mkdir('output')
    filename = 'output/' + filename 
    with pd.ExcelWriter(filename) as writer:
        for key in data.keys():
            data[key].to_excel(writer, sheet_name=key)

    return 