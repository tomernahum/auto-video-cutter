import json
from config_data.input_config_data import InputConfigData
from command import Command

class ConfigFileParser():  #this doesnt really need to be a class
    def __init__(self) -> None:
        pass

    def parse_config_file(self, config_file_name): 
        with open(config_file_name, 'r') as file:
            json_data = json.load(file)
        config_data = self.parse_format_1(json_data)
        return config_data
        
        
    def parse_format_0(self, json):
        config_data = InputConfigData()

        config_data.add_trigger("Hotkey", "alt+z", "zoom command (temp)")
        config_data.add_trigger("Hotkey", "alt+x", "flip command (temp)")

        return config_data   
        
    def parse_format_1(self, json):
        config_data = InputConfigData()
        
        triggers = json["triggers"]
        for line in triggers:
            config_data.add_trigger(
                category_name= line["trigger category"],
                trigger_name= line["trigger name"],
                command_info= line["command identifier"]
            )

        return config_data
            