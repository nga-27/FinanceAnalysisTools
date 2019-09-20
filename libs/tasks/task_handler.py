import pandas as pd 
import numpy as np 

def task_handler(config: dict, data: dict):
    tasks = config.get('tasks', [])
    for i, task in enumerate(tasks):
        print(f"task {i} is '{task['task']}', requested is {task['requested']}")