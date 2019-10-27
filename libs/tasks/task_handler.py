import pandas as pd 
import numpy as np 

from libs.tasks.tabular import tabular_stats, fetch_api_data
from libs.tasks.models import growth_investment

def task_handler(config: dict, data: dict):
    tasks = config.get('tasks', [])
    api = config.get('api', None)
    for i, task in enumerate(tasks):
        print(f"task {i} is '{task['task']}', requested is {task['requested']}")

        if task['requested']:
            data = run_task(task['task'], data, api)


def run_task(task: str, data: dict, api: dict) -> dict:
    if task == 'tabular stats':
        data['tabular'] = tabular_stats(data)
    if task == 'growth investment':
        # TODO: add inputs (if future desired)
        growth_investment()
    if task == 'fetch api data':
        data = fetch_api_data(api, data)

    return data