#WIP
import importlib
from typing import Dict

from record_mode import Command #temp location probably

from plugin_apis_template import PluginApi #might put in this same file



class PluginsInterface:
    def __init__(self, active_plugin_names, plugins_folder_directory="plugins") -> None:
        self.plugin_apis: list[PluginApi] = get_plugin_apis(active_plugin_names, plugins_folder_directory)

    def get_default_commands_by_type(self) -> Dict[str, list["Command"]]: 
        all_default_commands = self.get_default_commands()
        
        dc_dict = dict()
        for command in all_default_commands:
            command_proccessor_name = command.type
            
            if command_proccessor_name not in dc_dict:
                dc_dict[command_proccessor_name] = []
            
            dc_dict[command_proccessor_name].append(command)

        return dc_dict

    def get_default_commands(self):
        default_commands = []
        for api in self.plugin_apis:
            default_commands.extend( api.get_default_commands() )
        return default_commands


    

    

def get_plugin_apis(plugin_names, dir) :
        output = []
        for name in plugin_names:
            output.append(get_plugin_api(name, dir))
        return output

def get_plugin_api(name, dir) -> PluginApi:
    
    return importlib.import_module(str(f"{dir}.{name}.api")).API()



#



if True:
    test_plugin = get_plugin_api("test_plugin", "plugins")
    pi = PluginsInterface(["test_plugin"])
    pi.get_default_commands_by_type()


