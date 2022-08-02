from dataclasses import dataclass
import keyboard
from lookup import Lookup
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import test2

@dataclass #idk if this is good or bad or what - prob will end up converting it to normal which would be a pain to do if i use getters and setters
class EffectData:
    name : str
    type : str #should potentially look into enums - nah
    #id: str #could implement for 2 of the same effect so they dont get confused
    
    #will have more stuff like wants_input (maybe make that dynamic?) actually thats a whole thing I will figure out later
    
    def __eq__(self, other):
        return self.name == other.name or self.name == other



class Engine():
    proccesses_data : dict
    hotkey_effects_lookup : Lookup  #a lookup is just a dict wrapper idk why
    type_proccessing_objs : dict #I need consistency ik sorry ig cause this is mutable?

    def __init__(self) -> None:
        self.proccesses_data = dict()
        self.hotkey_effects_lookup = Lookup()
        self.type_proccessing_objs = dict()

        self.display = Display()
        self.writer = Writer()
        
        self.main_timer = None

    def _register_hotkeys_and_effects(self):
        #control
        self.hotkey_effects_lookup.register("ctrl+shift+\\", EffectData("start_or_end", "control")) #have to use this if u want start & end to be same hotkey
        #self.hotkey_effects_lookup.register("ctrl+shift+\\", EffectData("start", "control"))
        #self.hotkey_effects_lookup.register("ctrl+shift+\\", EffectData("end", "control"))
        placeholder = "pause"

        #cut_actions
        placeholder = "Accept, Reject, Reject Last Accepted, timelapse last, etc"

        #toggle effects
        self.hotkey_effects_lookup.register("alt+x", EffectData("flip", "toggle_effect"))
        self.hotkey_effects_lookup.register("alt+z", EffectData("bw", "toggle_effect"))

        #more effects & possibly proccessing objects will be registered by plugins + custom hotkeys will be implemented somehow
    
    def _register_proccessing_objects(self):
        self.type_proccessing_objs["control"] = None
        self.type_proccessing_objs["toggle_effect"] = test2.ToggleEffectsProccessing()
        self.type_proccessing_objs["cut_action"] = None

    def start_record_mode(self): #main
        #register hotkeys & effect proccesses
        self._register_hotkeys_and_effects()
        self._register_proccessing_objects()

        #add hotkey listeners with keyboard module
        for hotkey in self.hotkey_effects_lookup.get_keys():
            keyboard.add_hotkey(hotkey, self.on_hotkey_press, args=[hotkey])
            

        #start display/ui
        self.display.run_updating_display(self.type_proccessing_objs["toggle_effect"])
        keyboard.wait()
        pass

    def on_hotkey_press(self, hotkey):
        effect = self.hotkey_effects_lookup.lookup(hotkey)
        proccessing_obj : object = self.type_proccessing_objs[effect.type]  #eventually put abstract method instead of :object
        proccessing_obj.trigger(effect, self.display, self.writer)
        #idea: could later abstract input so i can have hotkeys + streamdeck/touchportal/etc + hand gesture ai detection + etc




class Display:
    def __init__(self) -> None:
        self.updating_display_is_ended = False
        pass
    
    def run_updating_display(self, toggle_effects_proccessing:"test2.ToggleEffectsProccessing" ):
        
        #updating display
        while self.updating_display_is_ended == False:
            active_effects = toggle_effects_proccessing.get_active_effects()
            self.update_updating_display(active_effects)
            time.sleep(1)
    
    
    def update_updating_display(self, active_effects):
        
        active_effects_string = ""
        for active_effect in active_effects:
            active_effects_string += f"{active_effect.name}(N/A), "


        print(f"active effects: {active_effects_string}")

    def print(self, to_print, info):
        print(info)


class Writer:
    file_name : str
    file : object #whatever is returned by open("filename.txt", 'w')
    

    def __init__(self) -> None:
        pass
        
    
    def write_effect_to_file(self, effect_name, start_time, stop_time, parameters:list):
        to_write = [effect_name, start_time, stop_time].extend(parameters)
        print(to_write)
        #self.file.write(to_write)
    
    def write_effect_to_file_1_str(self, to_write:str):
        pass



if True:
    engine = Engine()
    
    
    
    engine.start_record_mode()