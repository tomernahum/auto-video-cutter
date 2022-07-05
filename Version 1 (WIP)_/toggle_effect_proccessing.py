from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from graphlib import TopologicalSorter
from typing import TYPE_CHECKING, Callable, OrderedDict
from unicodedata import name

from proccessing_abstract import ProccessingObj, Command

if TYPE_CHECKING:
    from record_mode import EngineInterface





class ToggleCommand(Command): #this structure could  be generalized to other types of commands 
    type = "toggle_effect"  #type checking error here cause it doesn't say return. this is cleaner though!
    
    def __init__(self, effect_name, params_list:OrderedDict):
        self.effect_name = effect_name
        self.params_list = params_list   #
    
    #example params list
    params_list_ex = OrderedDict({
        "param_a" : "55",
        "param_b" : "[[REQUEST ON START]]",
        "param_c" : "[[REQUEST ON END]]"
    })

    REQUEST_ON_START_CODE = "[[REQUEST ON START]]"
    REQUEST_ON_END_CODE = "[[REQUEST ON END]]"

    def get_effect_name(self):
        return self.effect_name
    
    def get_params_list(self):
        return self.params_list

    def get_params_requested_on_start(self):
        return self._get_params_of_type(self.REQUEST_ON_START_CODE)
    
    def get_params_requested_on_end(self):
        return self._get_params_of_type(self.REQUEST_ON_END_CODE)


    def _get_params_of_type(self, type_code):
        output = []
        for key, value in self.params_list.items():
            if value == type_code:
                output.append((key, value))
        return output
            


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


class MutableToggleCommand(ToggleCommand):
    def __init__(self, toggle_command:ToggleCommand):
        self.effect_name = toggle_command.effect_name
        self.params_list = toggle_command.params_list
    
    def request_params_start(self, request_function:Callable[[list], OrderedDict]):
        params_requested = self.get_params_requested_on_start()
        for result_key, result_value in request_function(params_requested):
            self.params_list[result_key] = result_value



class ToggleEffect():
    def __init__(self, command, start_time) -> None:
        self.command = command
        self.start_time = start_time
        


class ToggleEffectsProccessing(ProccessingObj):
    command_type = "toggle_effect"

    def __init__(self):
        self.active_effects:list = []
        

    def trigger(self, command: "ToggleCommand", interface: "EngineInterface", current_time:float):
        #command has effect_name & parameters
        effect_info = MutableToggleCommand(command)
        effect_info.request_params_start(lambda x :interface.ask_for_input_parameters(x))  #lambdad in case ask_for_input_parameters ever wants more than 1 input
        
        
        effect = ToggleEffect(command, current_time)
        
        
        
        pass
        

    def finish_up(self, interface: "EngineInterface"):
        pass

    def get_running_display_info(self, current_time:float):
        pass


    def _set_params_for_input(self, command, interface):












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