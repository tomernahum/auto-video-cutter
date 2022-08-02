from collections import OrderedDict
import json


def get_config_data(config_file_name):
    with open(config_file_name) as file:
        json_data = json.load(file, object_pairs_hook=OrderedDict)
    
    print(json_data)
    
    
    
    
    
    
    
    return


"""
Config Data:

"Hotkeys" "Commands"


"""