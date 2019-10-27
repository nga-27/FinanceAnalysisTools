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
    tabular = data.get('tabular', {})
    for key in T_KEYS:
        if T_KEYS[key] not in tabular.keys():
            print(f"WARNING (Tabular_Stats): Key {key} not found in data. Exiting...")
            return tabular
    
    tabular = update_data_realtime(tabular, data)
    gl_period = get_gain_loss_period(tabular)
    tabular['Gain_Loss_Period'] = gl_period[0]
    tabular['Gain_Loss_Period_Percent'] = gl_period[1]

    tabular['Total_Return'] = total_return(tabular)
    tabular['YTD_Return'] = ytd_return(tabular)

    save_tabular_file(tabular, filename='finances_output.xlsx')
    return tabular


def update_data_realtime(tabular: dict, data: dict=None) -> dict:
    download_data = data.get('download_data')
    api_data = data.get('api')

    if download_data is not None:
        amt_data = tabular.get(T_KEYS['amount']).copy()
        qty_data = tabular.get(T_KEYS['qty']).copy()

        if (amt_data is not None) and (qty_data is not None):
            num_rows = len(amt_data)
            for fund in download_data.keys():
                if fund in amt_data.columns:
                    # print(f"col: {fund}")
                    qty = qty_data[fund][num_rows-1]
                    price = download_data[fund]['Close'][len(download_data[fund]['Close'])-1]
                    total = np.round(qty * price, 2)
                    amt_data[fund][num_rows-1] = total
                    # print(f"{qty} at {price} = {total}")
                else: 
                    # Keys are speciality (e.g. `HSA`)
                    special = api_data['details'][fund]['type']
                    special += f"-{fund}"

                    if special in amt_data.columns:
                        # print(f"col: {special}")
                        qty = qty_data[special][num_rows-1]
                        price = download_data[fund]['Close'][len(download_data[fund]['Close'])-1]
                        total = np.round(qty * price, 2)
                        amt_data[special][num_rows-1] = total
                        # print(f"{qty} at {price} = {total}")

            tabular[T_KEYS['amount']] = amt_data.copy()

    return tabular
    


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