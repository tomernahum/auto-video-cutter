
from collections import OrderedDict

import json

from record_mode import Command

from toggle_effect_proccessing import ToggleCommand, ParamsList  #temp I will simplify this stuff




#maybe each command should just have the same number of inputs and one of them is a list
#infact maybe we don't even need command subclasses.
#the only thing they provide is types + # of parameters 



#probably will redo command definition system
COMMAND_CONSTRUCTORS = {"ToggleCommand": ToggleCommand}


def parse_config_file(json_file_name):
    
    return {
        "hotkeys":{
            "alt+z" : ToggleCommand("zoom", ParamsList()),
            "alt+x" : ToggleCommand("flip", ParamsList())
        }
    }
    
    #todo WIP 
    with open(json_file_name, 'r') as file:
        json_data = json.load(file, object_pairs_hook=OrderedDict)


    output = {}   #trigger type : {trigger id : command}
    for trigger_type, data in json_data.items():         #at time of writing the only developed trigger type is hotkey (implemented with keyboard module from pypi)
        
        output2 = {}
        for command_type, id_constructor_pairs in data.items():
            command_constructor = COMMAND_CONSTRUCTORS[command_type]
            for event_id, constuctor_info in id_constructor_pairs.items():
                command = command_constructor()
                
                
                output2[event_id] = None

        
        x = None
        output[trigger_type] = x










class ConfigFileParser():
    #reads the input config file to tell what commands correspond to what hotkey/other input method
    #file format and stuff may be revised

    def __init__(self, json_file_name) -> None:
        import json
        self.json_file_name = json_file_name
        #self.json_data_dict = None

        #I was am a bit tired when I write this
        self.TRIGGER_TYPE_TO_FUNCTION = {"Hotkey-Commands": self.parse_hotkeys}
        self.COMMAND_CONSTRUCTORS = {"ToggleCommand" : ""}


    # -> hotkey:command   ___:command

    def parse_config_file(self) :
        #get the configs from the file
        with open(self.json_file_name, 'r') as file:
            json_data = json.load(file, object_pairs_hook=OrderedDict)
        
        output = {}
        for trigger_type, data in json_data.items():
            if trigger_type not in self.TRIGGER_TYPE_TO_FUNCTION:
                continue
            output[trigger_type] = self.TRIGGER_TYPE_TO_FUNCTION[trigger_type](data)
        
        return output
        pass

    def parse_hotkeys(self, data) -> Dict[str, "Command"]:
        for command_type_name in data:
            pass