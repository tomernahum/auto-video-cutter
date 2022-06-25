from dataclasses import dataclass
from typing import List
import keyboard
import time

@dataclass #idk if this is good or bad or what - prob will end up converting it to normal which would be a pain to do if i use getters and setters
class EffectData:
    name : str
    type : str #should potentially look into enums - nah
    #id: str #could implement for 2 of the same effect so they dont get confused
    
    #will have more stuff like wants_input (maybe make that dynamic?) actually thats a whole thing I will figure out later
    
    def __eq__(self, other):
        return self.name == other.name or self.name == other


class Proccessing():
    #will be an abstract class or interface or whatnot for proccessing
    pass

class ControlProccessing:
    effect_category = "control"

    def __init__(self) -> None:
        self.started = False
        self.ended = False
        self.paused = False

        self.timer = None #will be timer

    def trigger(self, effect:EffectData, display, writer): #called on
        if effect == "start_or_end":      #could use case (it that does require python 3.10 which could be annoying maybe)
            if self.started == False: self.trigger_start()
            else: self.trigger_end()

        elif effect == "start":
            self.trigger_start()
        elif effect == "end":
            self.trigger_end()
        
        else:
            pass

    def trigger_start(self):
        #start display, hotkey detection, etc (do this by calling Engine probably)
        pass

    def trigger_end(self):
        pass

    def finish_up(self, WIP): #called on
        pass


class ToggleEffectsProccessing:
    effect_category = "toggle_effect"
    
    class ToggledEffect:
        def __init__(self, effect) -> None:
            self.effect = effect
            self.timer = None #will be timer object (or just implement timer directly)
        
        def __eq__(self, other): #used for finding in list to remove
            self_name = self.effect.name
            try:
                other_name = other.effect.name
            except AttributeError:
                other_name = other.name
            
            return self_name == other_name

    def __init__(self):
        self.active_effects = []

    def trigger(self, effect:EffectData, display:"Display", writer): #will get called when hotkey is pressed #Q/A I can't specify the types of everything since its later in the file and they feed into each other - is them feeding in to each other bad design?
        effect_is_active = self.is_effect_active(effect)
        if effect_is_active:
            self._on_active_effect_triggered(effect, display, writer)
        else:
            self._on_inactive_effect_triggered(effect, display, writer)
        #may have to ask user for input - i guess we should pass in engine for that right? thats kosher right?
        pass
            
    def _on_inactive_effect_triggered(self, effect, display, writer):
        self.add_active_effect(effect)
        display.print(f"Activated {effect.name} effect", self.effect_category)
    
    def _on_active_effect_triggered(self, effect, display, writer):
        self.remove_active_effect(effect)
        display.print(f"Deactivated {effect.name} effect", self.effect_category)
        #write to file
        pass

    #todo idea: maybe needs in-between thing for converting events into display requests?
    
    def get_toggled_effects(self):
        return self.active_effects
   
    def add_active_effect(self, effect):
        self.active_effects.append(self.ToggledEffect(effect))
    
    def remove_active_effect(self, effect):
        self.active_effects.remove(effect)
    def is_effect_active(self, effect):
        
        return effect in self.active_effects
    

    def get_active_effect_names(self):
        output = ""
        for effect in self.active_effects:
            output += effect.name
        return output

    def finish_up(self, WIP): #called on at the end of the program
        pass
    
    #todo: need stuff to interface with active effect timers 
    # - I think the active_effect class should be a part of this only so its more modular


    
    
        


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
        self.writer : Writer = None #needs to be initialized w filename

        #self.display_interface = DisplayInterfaceConcept()
        
        self.main_timer = None

    def get_display_obj(self) -> "Display":
        return self.dispaly
    def get_writer_obj(self) -> "Writer":
        return self.writer

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
        #possibly should allow duplicate of ProccessingObjects?
    
    def _register_proccessing_objects(self):
        self.type_proccessing_objs["control"] = ControlProccessing
        self.type_proccessing_objs["toggle_effect"] = ToggleEffectsProccessing()
        self.type_proccessing_objs["cut_action"] = None

    def start_record_mode(self): #main
        #register hotkeys & effect proccesses
        self._register_hotkeys_and_effects()
        self._register_proccessing_objects()

        #get output file name (probably from user) / initialize writer
        filename = "test.txt"
        self.writer = Writer(filename)

        #add hotkey listeners with keyboard module
        for hotkey in self.hotkey_effects_lookup.get_keys():
            keyboard.add_hotkey(hotkey, self.on_hotkey_press, args=[hotkey])
        
        #wait for user to indicate start
        "tbd"

        #start display/ui
        self.display.run_updating_display(self.type_proccessing_objs["toggle_effect"])
        keyboard.wait()
        pass

    def on_hotkey_press(self, hotkey):
        effect = self.hotkey_effects_lookup.lookup(hotkey)
        proccessing_obj : object = self.type_proccessing_objs[effect.type]  #eventually put abstract method instead of :object
        proccessing_obj.trigger(effect, self.display, self.writer)
        #idea: could later abstract input so i can have hotkeys + streamdeck/touchportal/etc + hand gesture ai detection + etc

    def end_record_mode(self):
        for proccessing_obj in self.type_proccessing_objs:
            proccessing_obj.finish_up()
        
        self.display.stop_display()
        self.writer.close_writer()
    
    def pause_recording(self):
        pass

#next: pass VV object into proccessing_objs instead of whats there + implement control proccessing obj (then implement abstract class)
class ProccessingObjInterfaceConcept():
    def __init__(self, engine:"Engine") -> None:
        self.engine = engine
        self.display = engine.get_display_obj()
        self.writer = engine.get_writer_obj()
    
    def print_to_display(self, to_print, info=None):
        self.display.print(to_print, info)
    

    def write_effect_to_file(self, effect_name, start_time, stop_time, parameters:list):
        self.writer.write_effect_to_file(effect_name, start_time, stop_time, parameters)
        return
        to_write = [effect_name, start_time, stop_time].extend(parameters)
        self.writer.write_effect_to_file_1_str(to_write)
    
    def write_effect_to_file_1_str(self, to_write:str):
        self.writer.write_effect_to_file_1_str(to_write)
    

    def end(self):
        self.engine.end_record_mode()
        

class Display:
    def __init__(self) -> None:
        pass
    

    def _get_toggled_effects(self, toggle_effects_proccessing): #may find a better design pattern for this
        toggle_effects_proccessing.get_toggled_effects()

    def run_updating_display(self, toggle_effects_proccessing:ToggleEffectsProccessing):
        
        self.updating_display_is_ended = False
        #updating display
        while self.updating_display_is_ended == False:
            active_effects = self._get_toggled_effects(toggle_effects_proccessing)
            self.update_updating_display(active_effects)
            time.sleep(1)
    
    
    def update_updating_display(self, toggled_on_effects):
        #next: figure out interaction with ToggledEffects should it be done in display or toggleeffectproccessing (or somewhere else in between), if done in display where
        
        active_effects_string = ""
        for effect in toggled_on_effects:
            active_effects_string += f"{effect.effect.name}(N/A), "


        print(f"active effects: {active_effects_string}")

    def print(self, to_print, info=None):
        print(info)
    
    def stop_display(self):
        self.updating_display_is_ended = True
        #self.display_is_ended = True





class Writer:
    file_name : str
    file : object #whatever is returned by open("filename.txt", 'w')
    

    def __init__(self) -> None:
        pass #probably open file here
    
    
    def close_writer(self):
        pass #close file
    
    def write_effect_to_file(self, effect_name, start_time, stop_time, parameters:list):
        to_write = [effect_name, start_time, stop_time].extend(parameters)
        print(to_write)
        #self.file.write(to_write)
    
    def write_effect_to_file_1_str(self, to_write:str):
        print(to_write)








if True:
    file = open("test.txt", 'w')
    print(type(file))
    
    
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


