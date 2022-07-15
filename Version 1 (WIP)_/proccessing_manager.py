from abc import ABC
from maint import Proccessor



#something reads the json file
#for each Input Type in the json file, an input component is looked up from a dict
#then the add_input_hook func is called for every name:command pair in that input type's section
-


class InputComponent(ABC):
    
    def __init__(self, trigger_command_func):
        pass

    def add_input_hook(self, hook_id):   #hook id will be that that is in the json file
        #adds an input hook that triggers

        
        pass

    def 


    pass

class HotkeyInputComponent:
    

    def __init__(self) -> None:
        self.hotkey_command_lookup = {}
        
        self.trigger_command_func:
        self.current_time_getter_func:
        pass 
    
    
    def add_hotkey(self, hotkey_name): #aka trigger id
        import keyboard
        
        hotkey = hotkey_name
        keyboard.add_hotkey(hotkey, self.on_hotkey_pressed, args=[
            self.trigger_command_func, self.hotkey_command_lookup, hotkey, self.current_time_getter_func])
        pass
    

    def on_hotkey_pressed(self, key_name):
        current_time = self.current_time_getter_func()
        command = self.hotkey_command_lookup[key_name]
        
        self.trigger_command_func(command, current_time)
        pass
    
    pass



class ProccessingManager:
    #Manages inputs & commands
    
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
    def on_hotkey_pressed(trigger_command, commands_lookup, key_name, get_time_func):
        command= commands_lookup[key_name]
        trigger_command(command, get_time_func()) 


    def trigger_command(self, command, current_time):
        print(command)
        #get the right proccessor based on info in the command
        #proccessor.trigger(command, current_time, engine_interface)