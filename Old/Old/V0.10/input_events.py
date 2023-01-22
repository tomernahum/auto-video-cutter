from abc import ABC, abstractmethod
from typing import Callable, Type
from config_data.input_config_data import InputConfigData, ConfigTuple

#trigger data is really: trigger category name (eg hotkeys), trigger name (eg alt+x), and command info (eg {type:test})
#trigger category name references an input object
#trigger name references a register_trigger(trigger_name) to the input object
#command info is passed along and could be anything

#(input object lookup, trigger_id), command_data


class InputEventsMonitor():

    def __init__(self, config_data, output_call):
        self.input_objects_references:dict[str,Type["Input"]] = {
            "Hotkey" : HotkeyInput,
            "Hotkey2" : HotkeyInput
        }
        self.input_objects : dict[str, Input]

        self.config_data:InputConfigData = config_data
        self.output_call = output_call

    def start_monitoring(self):
        self.input_objects = self._get_instanciated_and_started_input_objects(self.input_objects_references)
        
        trigger_data = self.config_data.get_trigger_data()
        for data_piece in trigger_data:
            self.input_objects[data_piece.trigger_category_name].register_hook(
                data_piece.trigger_name, self.output_call, args=[data_piece.command_info])

    

    def stop_monitoring(self):
        for o in self.input_objects.values():
            o.stop_listening()

        
    def _get_instanciated_and_started_input_objects(self, objs,):
        input_objects: dict[str, Input] = {}
        for name, obj in objs.items():
            input_objects[name] = obj()
            input_objects[name].start_listening()
        return input_objects


    def register_input_object(self, name, object:Type["Input"]):
        self.input_objects_references[name] = object




class Input(ABC):
    @abstractmethod
    def register_hook(self, trigger_name, call_function, args):
        pass

    @abstractmethod
    def stop_listening(self):
        pass
    
    @abstractmethod
    def start_listening(self):
        pass

import keyboard
class HotkeyInput(Input):

    active_hotkeys = []
    started = False
    
    def register_hook(self, trigger_name, call_function, args:list):
        keyboard.add_hotkey(trigger_name, self.on_hotkey_pressed, args=[call_function, args])
        self.active_hotkeys.append(trigger_name)

    def on_hotkey_pressed(self, call_function, args):
        if self.started:
            call_function(args)
    
    def stop_listening(self):
        keyboard.clear_all_hotkeys()
        self.active_hotkeys.clear()
        self.started = False
        #or go through the active hotkeys one by one if keyboardhotkeys are used somewhere else. But ideally they wouldnt be
    
    def start_listening(self):
        self.started = True



class ProgramEventInput(Input):
    pass
    
    




class TestInput(Input):
    active_hotkeys = []
    started = False
    
    def register_hook(self, trigger_name, call_function, args:list):
        keyboard.add_hotkey(trigger_name, self.on_hotkey_pressed, args=[call_function, args])
        self.active_hotkeys.append(trigger_name)

    def on_hotkey_pressed(self, call_function, args):
        if self.started:
            call_function(args)
    
    def stop_listening(self):
        keyboard.clear_all_hotkeys()
        self.active_hotkeys.clear()
        self.started = False
        #or go through the active hotkeys one by one if keyboardhotkeys are used somewhere else. But ideally they wouldnt be
    
    def start_listening(self):
        self.started = True


if __name__ == "__main__":
    x = InputEventsMonitor()
    y = TestInput
    print(type(y))
    x.register_input_object("test", y)