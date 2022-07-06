from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from graphlib import TopologicalSorter
from typing import TYPE_CHECKING, Callable, OrderedDict
from unicodedata import name

from proccessing_abstract import ProccessingObj, Command

if TYPE_CHECKING:
    from record_mode import EngineInterface


class ParamsList():   #todo: put in general file & import
    def __init__(self, default_params: OrderedDict=OrderedDict({})) -> None:
        self.params_list = default_params

    REQUEST_ON_START_CODE = "[[REQUEST ON START]]"
    REQUEST_ON_END_CODE = "[[REQUEST ON END]]"
    
    #example params list
    params_list_ex = OrderedDict({
        "param_a" : "55",
        "param_b" : "[[REQUEST ON START]]",
        "param_c" : "[[REQUEST ON END]]"
    })

    def get_params_list(self):
        return self.params_list

    def get_params_values(self):

        return list(self.params_list.values())
    def get_params_requested_on_start(self):
        return self._get_params_of_type(self.REQUEST_ON_START_CODE)
    
    def get_params_requested_on_end(self):
        return self._get_params_of_type(self.REQUEST_ON_END_CODE)


    def ask_ui_for_start_parameters_and_update_them(self, interface:"EngineInterface"):
        params_requested = self.get_params_requested_on_start()
        if params_requested == []:
            return
        
        result = interface.ask_for_input_parameters(params_requested)  
        for key, value in result.items():
            self.params_list[key] = value
    
    def ask_ui_for_end_parameters_and_update_them(self, interface:"EngineInterface"):
        params_requested = self.get_params_requested_on_end()
        if params_requested == []:
            return
        
        result = interface.ask_for_input_parameters(params_requested)  
        for key, value in result.items():
            self.params_list[key] = value


    def _get_params_of_type(self, type_code):
        output = []
        for key, value in self.params_list.items():
            if value == type_code:
                output.append(key)
        return output


class ToggleCommand(Command): #this structure could  be generalized to other types of commands 
    type = "toggle_effect"  # type: ignore   #type checking error here cause it doesn't say return. this is cleaner though!
    
    def __init__(self, effect_name:str, params_list:ParamsList):
        self.effect_write_name = effect_name 
        self.params_list = params_list   #

        self.effect_id = effect_name   #would be diff from write_name to have 2 of the same effect
        #self.action = "Toggle" #not going to implement other actions for now but they could be turn on or turn off and then it would be 2 of the same effect or do nothing #todo if u want



    def get_effect_id(self):
        return self.effect_id
    def get_effect_write_name(self):
        return self.effect_write_name
    def get_params_list(self):
        return self.params_list
            


#example toggle command/how the system would work (draft):
if False:
    params_list = OrderedDict({
        "zoom multiplier" : "REQUEST ON START",
        "zoom x" : "middle",
        "zoom y" : "middle",
        "animation" : "true"
    })
    zoom_effect_command = ToggleCommand("defaults.zoom", params_list)
    params_list["animation"] = "false"
    zoom_effect_command_un_animated = ToggleCommand("defaults.zoom", params_list)

    hotkey_lookup.register("alt+z", zoom_effect_command_un_animated)
    hotkey_lookup.register("alt+shift+z", zoom_effect_command)

#-----------------


class ToggledEffect():
    def __init__(self, start_time, effect_name, parameters) -> None:
        self.effect_id = effect_name
        self.parameters:ParamsList = parameters
        self.start_time = start_time

        self.effect_write_name = effect_name

    def __eq__(self, other) -> bool:
        if type(other) == ToggledEffect:
            return self.effect_id == other.effect_id
        else:
            return self.effect_id == other
        

        


class ToggleEffectsProccessing(ProccessingObj):
    command_type = "toggle_effect"

    def __init__(self):
        self.active_effects:list = []
        

    def trigger(self, command: "ToggleCommand", interface: "EngineInterface", current_time:float):
        #command has effect name & parameters object
        
        #!! user input not yet tested

        if not self.is_effect_active(command.effect_id):
            self.start_effect(command, interface, current_time)
        else:
            self.end_effect(command, interface, current_time)


        pass
        

    def finish_up(self, interface: "EngineInterface", current_time:float):
        #toggle off all active effects
        pass

    def get_running_display_info(self, current_time:float):
        pass
    def get_toggled_effects(self): #for old implementation of display
        output = []
        for i in self.active_effects:
            output.append(i.effect_write_name)
        return output



    def start_effect(self, command:ToggleCommand, interface:"EngineInterface", current_time):
        effect = ToggledEffect(current_time, command.get_effect_write_name(), command.get_params_list())
            
        #ask for params start
        #print(f"PARMAMSM!!!: {effect.parameters}")
        effect.parameters.ask_ui_for_start_parameters_and_update_them(interface)
        
        #add to active effects list
        self.activate_effect(effect)
        pass
    
    def end_effect(self, command:ToggleCommand, interface:"EngineInterface", current_time:float):
        effect = self.get_effect(command.effect_id)
        
        #ask for params end
        effect.parameters.ask_ui_for_end_parameters_and_update_them(interface)
        
        #remove from active effects list
        self.deactivate_effect(effect)
        
        #write to file
        interface.write_effect_to_file(
            effect_name= effect.effect_write_name, 
            start_time = effect.start_time,
            stop_time  = current_time,
            parameters = effect.parameters.get_params_values(),
            )

    


    def is_effect_active(self, effect_id):
        return effect_id in self.active_effects
    
    def activate_effect(self, effect:ToggledEffect):
        self.active_effects.append(effect)
    
    def deactivate_effect(self, effect:ToggledEffect):
        self.active_effects.remove(effect)

    def get_effect(self, effect_id) -> ToggledEffect:
        for i in self.active_effects:
            if i.effect_id == effect_id:
                return i
        return None # type: ignore #todo: errors i guess



def get_commands_to_register_temp():  #temp, eventually this will do an official registration function in the plugin
    output = [
        ("alt+x", ToggleCommand("flip", ParamsList())),  #it being a toggle command sets the proccessor/type automatically
        ("alt+z", ToggleCommand("bw", ParamsList()))
    ]

    return output








"""
    parameters requested:
    - parameter name:  zoom amount   ,  parameter value: input request    ,  input message:  "pls input zoom amount", input type: on start
    - parameter name:  zoom x   ,  parameter value: center    ,  input message:  None
    - parameter name:  zoom y   ,  parameter value: function    ,  function: "get_center_y_of_ screen"
    
   
    
"""
    #test










"""
Concept:

ToggleEffect(abstract, effect_data):   # effectdata might be interface or something
    on_toggle_on()
        ask for input or not
        (maybe add active_effect?)
        pass

    on_toggle_off()
        write to file based on input & time elapsed


ToggleEffectsProccessing(ProccessingObj):
    active_effects
    
    trigger(toggle_effect, interface):
        if effect is active:
            toggle_effect.on_start
        else:
            toggle_effect.on_end
    
    finish_up():

    get_active_effects_w_start_times/timers():


either:
 - pass in toggle_proccessing interface to toggle effects so they can 
    - ask for input
    - write effect w parameters from stored input (.or settings)
 - get specific info from toggle effects such as:
    - list of parameters
    - ask_for_input message for each parameter


cut actions:
either:
- pass in cut_action interface to cutaction effects so they can:
    - ask for input
    - move the segment (reject/accept it)
    - write effect / apply effect to segment w parameters from input stored (.or settings)
- get specific info from cutaction effects such as:
    - list of paramaters & input_request messages
    - whether it wants to move the segment??






"""