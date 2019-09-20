import pandas as pd 
import numpy as np 
import json
import os
import time

def startup_script(version='0.0.1', update_release='2019-09-19') -> dict:
    print(" ")
    print("----------------------------------")
    print("-    Finance Analysis Tools      -")
    print("-                                -")
    print("-            nga-27              -")
    print("-                                -")
    print(f"-       version: {version}          -")
    print(f"-       updated: {update_release}      -")
    print("----------------------------------")
    print(" ")
    
    time.sleep(1)

    return get_configuration()


def get_configuration() -> dict:
    json_path = 'config.json'
    if os.path.exists(json_path):
        with open(json_path) as json_file:
            core = json.load(json_file)
            return core

    print(f"No 'config.json' found. Exiting...")
    return None
        