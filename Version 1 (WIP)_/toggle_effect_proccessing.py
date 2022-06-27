from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from typing import TYPE_CHECKING

from proccessing_abstract import ProccessingObj, Command

if TYPE_CHECKING:
    from record_mode import EngineInterface



class ToggleCommand(Command, ABC): 
    type = "toggle_effect"
    
    #@property
    #def type(self)
    #    return "toggle_effect"
    
    @abstractproperty
    def name(self):
        return "toggle command base"

    def __init__(self) -> None:
        self.name = "Base class toggle command"

    def get_effect_name(self):
        return self.name

    def wants_input_on_start(self):
        return False



class ZoomEffectCommand(ToggleCommand): #example toggle command
    name = "zoom"
    parameters = None

    start_parameters_requests = None
    end_parameters_requests = None
    
    default_parameter_values = None


    def __init__(self) -> None:
        pass

#Could make toggle command not abstract but
#just having properties that are created on init
#may still make cutaction commands/etc abstract tho


if True:
    zoom_effect = ZoomEffectCommand()
    x = isinstance(zoom_effect, ToggleCommand)
    print(zoom_effect.get_effect_name())




#----------------

class Effect():
    #def __init__(self, command:"ToggleCommand") -> None:
        

    def __init__(self, name, start_time, parameters) -> None:
        self.name = name
        self.start_time = start_time
        self.end_time = None #yet

        self.parameters = parameters

    def get_running_time(self, current_time):
        #maybe add state check of if its ended probably not though
        return current_time - self.start_time


class ToggleEffectsProccessing(ProccessingObj):

    def __init__(self):
        self.active_effects = []
        self.command_type = "toggle_effect"

    def trigger(self, command: "ToggleCommand", interface: "EngineInterface", current_time:float):
        
        effect_is_active = self._is_effect_active_from_command(command)
        
        if effect_is_active:
            effect = self.deactivate_effect_from_command(command)
            self.on_effect_deactivation(effect)
        
        else: 
            effect = self.build_effect_object(command, interface, current_time)
            self.activate_effect(effect)
            #display that it's activated?


        

        #
        

    def finish_up(self, interface: "EngineInterface"):
        pass

    def get_running_display_info(self, current_time:float):
        pass

    
    active_effects:list
    
    def _is_effect_active_from_command(self, command):
        for i in self.active_effects:
            if i.get_name() == command.get_effect_name():
                return True
        return False

    def deactivate_effect_from_command(self, command) -> Effect:
        pass #TBD

    def activate_effect(self, effect:Effect):
        self.active_effects.append(effect)
    
        


    def build_effect_object(self, command, interface, current_time) -> Effect:
        parameters = get_effect_parameters_start(command, interface) #incl potentially asking for input
        effect = Effect(
            name= command.get_effect_name(),
            start_time= current_time,
            parameters= parameters
        )
        return effect
    
    def on_effect_deactivation(self, effect:Effect):
        #ask for any possible closing inputs
        #write to file
        #display that it's closed?
        pass #TBD

def get_effect_parameters_start(command, interface):
    if command.wants_input_on_start():
        #ask for the input
    #idk










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