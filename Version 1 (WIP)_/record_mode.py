from dataclasses import dataclass
from typing import List
import keyboard
import time

@dataclass #idk if this is good or bad or what
class EffectData:
    name : str
    type : str #should potentially look into enums
    #id: str #could implement for 2 of the same effect so they dont get confused
    
    def __eq__(self, other):
        return self.name == other.name


class ToggleEffectsProccessing:

    def __init__(self):
        self.active_effects = []

    def trigger(self, effect:EffectData, display): #will get called when hotkey is pressed
        
        if effect in self.active_effects:
            self.remove_active_effect(effect)
            display.print(f"Deactivated {effect.name} effect")
        else:
            self.add_active_effect(effect)
            display.print(f"Activated {effect.name} effect") #still trying to figure out hierarchy/architecture stuff which relates to display
        
        pass
        
        
        
        
        
    def get_active_effects(self):
        return self.active_effects
    def add_active_effect(self, effect):
        self.active_effects.append(effect)
    def remove_active_effect(self, effect):
        self.active_effects.remove(effect)
    
    def get_active_effect_names(self):
        output = ""
        for effect in self.active_effects:
            output += effect.name
        return output

    
    
        


from lookup import Lookup
class Engine():
    proccesses_data : dict
    hotkey_effects_lookup : Lookup  #a lookup is just a dict wrapper idk why
    type_proccessing_objs : dict #I need consistency ik sorry ig cause this is mutable?

    def __init__(self) -> None:
        self.proccesses_data = dict()
        self.hotkey_effects_lookup = Lookup()
        self.type_proccessing_objs = dict()

        self.display = Display()
        self.main_timer = None

    def _register_hotkeys_and_effects(self):
        self.hotkey_effects_lookup.register("alt+x", EffectData("flip", "toggle_effect"))
        self.hotkey_effects_lookup.register("alt+z", EffectData("bw", "toggle_effect"))
    
    def _register_proccessing_objects(self):
        self.type_proccessing_objs["toggle_effect"] = ToggleEffectsProccessing()
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
        proccessing_obj.trigger(effect, self.display)


class Display:
    def __init__(self) -> None:
        pass
    
    def run_updating_display(self, toggle_effects_proccessing:ToggleEffectsProccessing ):
        for x in range(1000):
            active_effects = toggle_effects_proccessing.get_active_effects()
            self.update_updating_display(active_effects)
            time.sleep(1)
    
    
    def update_updating_display(self, active_effects):
        
        active_effects_string = ""
        for active_effect in active_effects:
            active_effects_string += f"{active_effect.name}(N/A), "


        print(f"active effects: {active_effects_string}")

    def print(self, to_print):
        pass












if True:
    engine = Engine()
    engine.start_record_mode()












quit()

"""
could get:
- effectdata
- effectdata constructor


"""

#Mockups
"""
def on_hotkey_press(hotkey):
    effect = effects_hotkey_dictionary.lookup(hotkey)
    
    ui.notify_new_effect()
    
    if effect.wants_input():
        effect = get_input(effect)
    
    write_effect(effect)
    

def on_toggle_effect(effect):
    if effect.wants_input():
        effect = get_input(effect)
    add_to_active_effects(effect)
        active_effects.append()
    _   notify_ui()




#1 - effect object lookup
#2 - effect constructor lookup

1:
def on_hotkey_press(hotkey):
    effect = effects_hotkey_dictionary.lookup(hotkey)
    if effect.wants_input():
        effect = get_input(effect)

2:
def on_hotkey_press(hotkey):
    pass



effect data
"""
"""effect_data
    effect name
    asks_for_input?
    give_input_function
    effect type (cut_action, toggle)
    
    get_start
    get_stop
    get_args
    aka get_thing_to_write



thing_to_write:
    effect name
    start
    stop
    args
"""
"""




"""


