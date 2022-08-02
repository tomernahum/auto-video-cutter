
#file will be replaced


from collections import OrderedDict

import json

from record_mode import Command

from toggle_effect_proccessing import ToggleCommand, ParamsList  #temp I will simplify this stuff

#probably will redo command definition system
COMMAND_CONSTRUCTORS = {"ToggleCommand": ToggleCommand}


def parse_config_file(json_file_name):
    
    return {
        "hotkeys":{
            "alt+z" : ToggleCommand("zoom", ParamsList()),
            "alt+x" : ToggleCommand("flip", ParamsList())
        }
    }

