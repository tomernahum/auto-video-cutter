import keyboard



class InputManager:
    
    def __init__(self) -> None:
        
        self.hotkey_commands_lookup = dict()
        
        pass



    def register_hotkey(self, hotkey:str):
        hotkey = keyboard.normalize_name(hotkey)
        keyboard.add_hotkey(hotkey, self.on_hotkey_press, args=[hotkey])


    def on_hotkey_press(self, hotkey):
        current_time = self.get_current_time()
        command = self.find_command(hotkey, self.hotkey_commands_lookup)
        #execute command
        
        pass

    
    
    def find_command(self, lookup_key, lookup:dict):
        return lookup[lookup_key]




    def get_current_time(self):
        pass







"""
Something that holds the proccessing objects
Something that detects when commands are called
Something that sends the commands to the proccessing objects when they are called

Something that keeps track of the current time





Something that holds the proccessing objects
Something that holds the commands
Something that detects when commands are called
Something that sends the commands to the proccessing objects when they are called




Possible System:

Engine Could hold all possible commands
InputManager could ask tell engine to retrieve a command

Engine
    Commands
    Objects
    InputManager

InputManager
    on_input_detected(Engine):
        Engine.run_command(...)

RunningDisplay
    update_updating_display(...):
        ...
    


while true:
    update_updating_display(...)
        



"""