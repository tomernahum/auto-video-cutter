from collections import OrderedDict
import json
from typing import Callable, Dict
import record_mode

class EngineInterface():
    def __init__(self, engine) -> None:
        self.engine = engine

class UserInterface():
    def __init__(self, engine_interface) -> None:
        self.engine_interface = engine_interface

class FileWriter():
    pass

#------------------------

class InputSource():
    pass
class HotkeyInput(InputSource):
    def __init__(self, trigger_command:Callable[["ProccessorCommand", "float"], None], timer) -> None:
        self.trigger_command = trigger_command
        self.commands_triggered_by_hotkeys : dict[str, "ProccessorCommand"] = {}
        self.timer = timer
    
    def register_hotkeys(self):
        pass
    
    
    def enable_input(self):
        for hotkey in self.commands_triggered_by_hotkeys.keys():
            pass


    def on_hotkey_press(self, hotkey, timer):
        command= self.commands_triggered_by_hotkeys[hotkey]
        self.trigger_command(command, timer.get_current_time())   #trigger command is a callable passed in when the inputsource was created

def on_blank_input(trigger_command, commands_lookup, input_name, timer):
    command= commands_lookup[input_name]
    trigger_command(command, timer.get_current_time()) 



class Proccessor():
    pass
class ProccessorCommand():
    pass


class ProccessingManager:
    def __init__(self) -> None:
        self.proccessors : dict[str, Proccessor]
        self.proccessor_commands = None

        self.timer = None
        self.get_time_func = self.timer.get_current_time_formatted()

        #todo: will be replaced with input dynamic input sources & eventually will add hand gestures as one of them:
        self.hotkey_command_lookup = {}
        import keyboard
        
        hotkey = "blank"
        keyboard.add_hotkey(hotkey, self.on_hotkey_pressed, args=[
            self.trigger_command, self.hotkey_command_lookup, hotkey, self.get_time_func])
    
    @staticmethod
    def on_hotkey_pressed(trigger_command, commands_lookup, key_name, get_time):
        command= commands_lookup[key_name]
        trigger_command(command, get_time()) 


    def trigger_command(self, command, current_time):
        print(command)
        #get the right proccessor based on info in the command
        #proccessor.trigger(command, current_time, engine_interface)




from ConfigFileParser import ConfigFileParser




if True:
    x = ConfigFileParser("input_config.json")
    x.parse_config_file()


class Engine():
    
    def __init__(self) -> None:
        self.engine_interface = EngineInterface(Engine)
        
        self.ui = UserInterface(EngineInterface)
        self.file_writer = FileWriter()
        
        
        self.proccessing_manager = ProccessingManager()
        
        import plugins_interface
        self.plugins_manager = plugins_interface.PluginsInterface

    def start_record_mode(self):
        proccessors = self.plugins_manager.get_proccessors
        self.input_config = None
        
        pass
    
    def register_processor():
        pass
    def register_command_hotkey_pair():
        pass
    def register_command_blank_pair():
        pass
