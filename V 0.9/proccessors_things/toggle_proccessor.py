from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from record_mode import Command
    from proccessors_things.proccessors_interface import ProccessorsInterface

from proccessors_things.abstract_proccessor import Proccessor
import utils.utils

class Effect():  #local    #copied from previous file
    def __init__(self, start_time:float, effect_name) -> None:
        self.effect_id = effect_name
        #self.parameters:ParamsList = parameters
        self.start_time = start_time

        self.write_name = effect_name

    def __eq__(self, other) -> bool:
        if type(other) == type(self):
            return self.effect_id == other.effect_id

    def get_runtime(self, current_time):
        return current_time - self.start_time


class ActiveEffects():
    #keeps track of what effects are active
    active_effects_list = []
    
    def __init__(self) -> None:
        self.active_effects_list: list[Effect] = []
    
    def activate_effect(self, effect:Effect):    #should this also be in terms of effect_name and then effect would only be referejced here?
        self.active_effects_list.append(effect)
    
    def effect_is_active(self, effect_name):
        for i in self.active_effects_list:
            if i.effect_id == effect_name:
                return True
        return False

    def remove_effect(self, effect_name): 
        for i, effect in enumerate(self.active_effects_list):
            if effect.effect_id == effect_name:
                return self.active_effects_list.pop(i)
        raise ValueError(f"No effect found. Active effects:{self.active_effects_list}")

    def get_active_effects_list(self):
        return self.active_effects_list


class ToggleProccessor(Proccessor):
    active_effects = ActiveEffects()

    def trigger(self, command:"Command", current_time, interface):
        effect_name = command.get_data(0) #everything is very temporary
        effect_params = command.get_data(1)
        #interface.print(f"command: {command}.    effect_name: {effect_name}.   effect_is_active:{self.effect_is_active(effect_name)}")
        
        if not self.active_effects.effect_is_active(effect_name):
            self._start_effect(effect_name, current_time, interface)
            
        else:
            self._end_effect(effect_name, current_time, interface)


        #may do instead sooner:
        #tp = TriggerProccessor(command, current_time, interface)
        #tp.proccess_trigger()
        #active_effects would be passed in somewhere?
    

    def get_display_active_effects(self, current_time):
        data = []
        for effect in self.active_effects.get_active_effects_list():
            runtime = effect.get_runtime(current_time)
            runtime = utils.utils.truncate_number(runtime)   #todo reorganize probably
            data.append((effect.effect_id, runtime))
        
        
        return data

    def finish_up(self, current_time, interface):  #something janky here
        pass



    def _start_effect(self, effect_name, current_time, interface, print_enabled=True):
        #build & activate the effect
        effect = Effect(current_time, effect_name)
        self.active_effects.activate_effect(effect)
        
        #print a message that you activated it
        if print_enabled == True:
            interface.print(f"{utils.utils.format_time(current_time)} - Activated [{effect_name}]") 
            #todo fix utils orginization. Also print orginization could be better here I think
        
        

    def _end_effect(self, effect_name, current_time, interface:"ProccessorsInterface", print_enabled=True):
        #remove the effect
        effect = self.active_effects.remove_effect(effect_name)
        
        #print a message that you removed it
        if print_enabled == True:
            interface.print(f"{utils.utils.format_time(current_time)} - Deactivated [{effect.effect_id}] it ran from {effect.start_time} - {current_time}")

        #write the effect to file
        interface.write_effect_to_file(effect.write_name, effect.start_time, current_time)




    def finish_with_effect(self, effect, current_time, interface):
        #write the effect
        interface.print(f"info to write: {effect.start_time} - {current_time}:  {effect.write_name}")



    #this section / file is kind of jank I am tired but I think I can refactor it later if I feel like it (its not too bad)
    printing_enable = True
    def print_effect_start(self, effect_name, current_time, interface): 
        if not self.printing_enable:
            return
            
        to_print = f"{utils.utils.format_time(current_time)} - Activated [{effect_name}]" #todo fix utils orginization
        interface.print(to_print)
    
    def print_effect_end(self, effect_name, effect_start_time, current_time, interface): 
        if not self.printing_enable:
            return
        
        to_print = f"{utils.utils.format_time(current_time)} - Deactivated [{effect_name}] it ran from {effect_start_time} - {current_time}"
        interface.print(to_print)





    