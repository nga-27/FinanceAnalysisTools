import pandas as pd 
import numpy as np 

from libs.tasks.tabular import tabular_stats

def task_handler(config: dict, data: dict):
    tasks = config.get('tasks', [])
    for i, task in enumerate(tasks):
        print(f"task {i} is '{task['task']}', requested is {task['requested']}")

        if task['requested']:
            run_task(task['task'], data)


def run_task(task: str, data: dict):
    if task == 'tabular stats':
        tabular_stats(data)