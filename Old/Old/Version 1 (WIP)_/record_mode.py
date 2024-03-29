from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from typing import List, OrderedDict
import keyboard
import time

from custom_timer import Timer


"""@dataclass #idk if this is good or bad or what - prob will end up converting it to normal which would be a pain to do if i use getters and setters
class Command(): #todo: make a protocol essentially
    name : str #will probably get rid of name once command inheretence stuff is set up
    type : str #should potentially look into enums - nah
    #id: str #could implement for 2 of the same effect so they dont get confused
    
    #will have more stuff like wants_input (maybe make that dynamic?) actually thats a whole thing I will figure out later 
    
    def __eq__(self, other): #WIP
        return self.name == other.name or self.name == other """


class Command(ABC): #WIP
    @abstractproperty
    def type(self) -> str: #aka which proccessor to send it to
        return "abstract_command"

    def get_type(self) -> str:
        return self.type

    @abstractmethod
    def __init__(self) -> None:
        super().__init__()

    #def run_command(self):
    #    pass



class ProccessingObj(ABC):
    @abstractproperty
    def effect_category(self):
        pass

    @abstractmethod
    def trigger(self, command:"Command", interface:"EngineInterface", time:"float"):
        pass
    
    @abstractmethod
    def finish_up(self, interface:"EngineInterface", time:"float"):
        pass

    #can be overwritten or not - i think this would be the right implementation
    def get_running_display_info(self, current_time:float): #might be inneficient to have everygthing give info all the time even if it doesnt need to. Or is it? #Q/A
        return None
    


class ControlCommand(Command):
    type = "control"    #todo maybe rename type

    def __init__(self, name) -> None:
        self.type = "control"
        self.name = name
    

class ControlProccessing(ProccessingObj):
    effect_category = "control"

    def __init__(self) -> None:
        self.started = False
        self.ended = False
        self.paused = False

        self.timer = None #will be timer

    def trigger(self, command:"ControlCommand", interface:"EngineInterface", time:float): #called on
        if command.name == "start_or_end":      #could use case (it that does require python 3.10 which could be annoying maybe)
            if self.started == False: self.trigger_start()
            else: self.trigger_end()

        elif command.name == "start":
            self.trigger_start()
        elif command.name == "end":
            self.trigger_end()
        
        else:
            pass

    def trigger_start(self):
        #start display, hotkey detection, etc (do this by calling Engine probably)
        pass

    def trigger_end(self):
        pass

    def finish_up(self, interface:"EngineInterface", time:float): #called on
        pass


class ToggleEffectsProccessing_old(ProccessingObj):
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

    def trigger(self, effect:Command, interface:"EngineInterface", time): #will get called when hotkey is pressed #Q/A I can't specify the types of everything since its later in the file and they feed into each other - is them feeding in to each other bad design?
        effect_is_active = self.is_effect_active(effect)
        if effect_is_active:
            self._on_active_effect_triggered(effect, interface)
        else:
            self._on_inactive_effect_triggered(effect, interface)

        #effect.trigger()
        
        pass
            
    def _on_inactive_effect_triggered(self, effect, interface:"EngineInterface"):
        self.add_active_effect(effect)
        interface.print_to_display(f"Activated {effect.name} effect", self.effect_category)
    
    def _on_active_effect_triggered(self, effect, interface:"EngineInterface"):
        self.remove_active_effect(effect)
        interface.print_to_display(f"Deactivated {effect.name} effect", self.effect_category)
        #write to file
        pass

    
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
    hotkey_command_lookup : Lookup  #a lookup is just a dict wrapper idk why
    type_proccessing_objs : dict[str, "ProccessingObj"] #I need consistency ik sorry ig cause this is mutable?

    def __init__(self) -> None:
        self.proccesses_data = dict()  #I do not remember what this is for
        self.hotkey_command_lookup = Lookup()
        self.type_proccessing_objs = dict()

        self.display = Display()
        self.writer : Writer = None # type: ignore #needs to be initialized w filename (todo make cleaner)
        self.timer: Timer = Timer()
        
        self.interface = EngineInterface(self)

    def _register_hotkey_command_lookups(self):
        #control
        self.hotkey_command_lookup.register("ctrl+shift+\\", ControlCommand("start_or_end")) #have to use this if u want start & end to be same hotkey
        #self.hotkey_effects_lookup.register("ctrl+shift+\\", EffectData("start", "control"))
        #self.hotkey_effects_lookup.register("ctrl+shift+\\", EffectData("end", "control"))
        placeholder = "pause"

        #cut_actions
        placeholder = "Accept, Reject, Reject Last Accepted, timelapse last, etc"

        #toggle effects
        from toggle_effect_proccessing import get_commands_to_register_temp
        for i in get_commands_to_register_temp():
            self.hotkey_command_lookup.register(i[0], i[1])
        

        #more effects & possibly proccessing objects will be registered by plugins + custom hotkeys will be implemented somehow
        #possibly should allow duplicate of ProccessingObjects?
    
    def _register_proccessing_objects(self):
        from toggle_effect_proccessing import ToggleEffectsProccessing

        self.type_proccessing_objs["control"] = ControlProccessing()
        self.type_proccessing_objs["toggle_effect"] = ToggleEffectsProccessing()
        self.type_proccessing_objs["cut_action"] = None
  
    def get_display_obj(self) -> "Display":
        return self.display
    def get_writer_obj(self) -> "Writer":
        return self.writer
    def get_timer(self):
        return self.timer
    
    def start_record_mode(self): #main
        #register hotkeys & effect proccesses
        self._register_hotkey_command_lookups()
        self._register_proccessing_objects()

        #get output file name (probably from user) / initialize writer
        filename = "test.txt"
        self.writer = Writer(filename)


        #add hotkey listeners with keyboard module
        for hotkey in self.hotkey_command_lookup.get_keys():
            keyboard.add_hotkey(hotkey, self.on_hotkey_press, args=[hotkey])
        
        #wait for user to indicate start
        "tbd"

        #start timer
        self.timer.start_timer()
        #start display/ui
        x = self.type_proccessing_objs["toggle_effect"]
        print(f"hello!!! {x}")
        self.display.run_updating_display(self.type_proccessing_objs["toggle_effect"], self.timer)
        pass

    def on_hotkey_press(self, hotkey): #todo
        current_time = float(self.timer.get_current_time_truncated())
        effect = self.hotkey_command_lookup.lookup(hotkey)
        proccessing_obj = self.type_proccessing_objs[effect.type]
        proccessing_obj.trigger(effect, self.interface, current_time)
        #idea: could later abstract input so i can have hotkeys + streamdeck/touchportal/etc + hand gesture ai detection + etc

    #brainstorm/draft
    def on_input(self, command):
        pass


    def end_record_mode(self):
        for proccessing_obj in self.type_proccessing_objs:
            proccessing_obj.finish_up()
        
        self.display.stop_display()
        self.writer.close_writer()
    
    def pause_recording(self):
        pass









#todo: make interface know what proccessing obj called it - either put diff ones in each proccessing obj or pass in ones tht know
class EngineInterface(): #still workshopping names - actually that applies to many of the names
    def __init__(self, engine:"Engine") -> None:
        self.engine:"Engine" = engine
        self.display:"Display" = engine.get_display_obj()
        self.writer:"Writer" = engine.get_writer_obj() #todo BUG bad stuff m8ty
        self.timer:"Timer" = engine.get_timer()
    

    def print_to_display(self, to_print, info=None):
        self.display.print(to_print, info)
    

    def write_effect_to_file(self, effect_name, start_time, stop_time, parameters:list):
        to_write_list = [effect_name, start_time, stop_time]
        to_write_list.extend(parameters)
        to_write = str(to_write_list)
        print(f"wants_to_write: {to_write}")
        return #todo BUG bad stuff m8ty wil do l8tr
        self.writer.write_effect_to_file(effect_name, start_time, stop_time, parameters)
        return
        to_write = [effect_name, start_time, stop_time].extend(parameters)
        self.writer.write_effect_to_file_1_str(to_write)
    
    def write_effect_to_file_1_str(self, to_write:str):
        self.writer.write_effect_to_file_1_str(to_write)


    def get_current_time(self): #maybe pass in time seperately
        return None #TBD
        self.timer.get_time()
    
    def ask_for_input_parameters(self, params_requested:List[str]) -> OrderedDict:
        return self.display.ask_for_input_parameters(params_requested)
    
    def end(self):
        self.engine.end_record_mode()
        

class Display: #/ UI (might rename)
    #implementation of the methods here is mostly temporary, eventually updating display will be continuous and eventually there will be a gui
    #also I think methods could be better
    
    def __init__(self) -> None:
        pass


    def _get_toggled_effects(self, toggle_effects_proccessing:"ToggleEffectsProccessing_old"): #may find a better design pattern for this
        return toggle_effects_proccessing.get_toggled_effects()

    def run_updating_display(self, toggle_effects_proccessing:ToggleEffectsProccessing_old, timer:Timer):
        
        self.updating_display_is_ended = False
        #updating display
        while self.updating_display_is_ended == False:
            active_effects = self._get_toggled_effects(toggle_effects_proccessing)
            self.update_updating_display(active_effects, timer.get_current_time_truncated())
            time.sleep(1)
    
    
    def update_updating_display(self, toggled_on_effects, current_time):
        #next: figure out interaction with ToggledEffects should it be done in display or toggleeffectproccessing (or somewhere else in between), if done in display where
        
        active_effects_string = ""
        for effect_name in toggled_on_effects:
            active_effects_string += f"{effect_name}, "


        print(f"{current_time} \tactive effects: {active_effects_string}")

    def print(self, to_print, info=None):
        print(info)

    def ask_for_input_parameters(self, params_requested:List[str]) -> OrderedDict:
        output = OrderedDict({})
        for param in params_requested:
            #output[param] = input(f"Enter: {param}:  ")
            output[param] = 50
        return output
    
    def stop_display(self):
        self.updating_display_is_ended = True
        #self.display_is_ended = True





class Writer:
    file_name : str
    file : object #whatever is returned by open("filename.txt", 'w')
    

    def __init__(self, filename) -> None:
        self.file_name = filename
        self.open_file()
    
    def open_file(self):
        self.file = open(self.file_name, "w")
    
    def close_writer(self):
        pass #close file
    
    def write_effect_to_file(self, effect_name, start_time, stop_time, parameters:list):
        to_write = [effect_name, start_time, stop_time].extend(parameters)
        print(to_write)
        #self.file.write(to_write)
    
    def write_effect_to_file_1_str(self, to_write:str):
        print(to_write)









if __name__ == "__main__":
    file = open("test.txt", 'w')
    print(type(file))
    
    
    engine = Engine()
    engine.start_record_mode()












#quit()

"""



    - Engine + Display + Writer

"""




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


