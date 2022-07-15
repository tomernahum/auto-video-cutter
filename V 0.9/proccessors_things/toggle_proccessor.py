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
        else:
            return self.effect_id == other

    def get_runtime(self, current_time):
        return current_time - self.start_time



class ToggleProccessor():
    active_effects = []

    def trigger(self, command, current_time, interface):
        effect_name = command.data[0] #everything is very temporary
        #interface.print(f"command: {command}.    effect_name: {effect_name}.   effect_is_active:{self.effect_is_active(effect_name)}")
        
        if not self.effect_is_active(effect_name):
            self.active_effects.append(Effect(current_time, effect_name))
            self.print_effect_start(command, current_time, interface) #shouldnt some of these just be class variables or in a seperate class yesss #todo - seperate class that just returns something or other 4 this class
        else:
            effect = self.remove_effect(effect_name)
            self.print_effect_end(command, current_time, interface)
            
            self.finish_with_effect(effect, current_time, interface)


        #may do instead sooner:
        #tp = TriggerProccessor(command, current_time, interface)
        #tp.proccess_trigger()
        #active_effects would be passed in somewhere?
    

    def get_display_active_effects(self, current_time):
        data = []
        for i in self.active_effects:
            runtime = i.get_runtime(current_time)
            runtime = utils.utils.truncate_number(runtime)   #todo reorganize probably
            data.append((i.effect_id, runtime))
        
        
        return data



    def effect_is_active(self, effect_name):
        for i in self.active_effects:
            if i.effect_id == effect_name:
                return True
        return False

    def remove_effect(self, effect_name):
        for i, effect in enumerate(self.active_effects):
            if effect.effect_id == effect_name:
                return self.active_effects.pop(i)
        raise ValueError(f"No effect found. Active effects:{self.active_effects}")


    def finish_with_effect(self, effect, current_time, interface):
        interface.print(f"info to write: {effect.start_time} - {current_time}:  {effect.write_name}")



    #this section / file is kind of jank I am tired but I think I can refactor it later if I feel like it (its not too bad)
    printing_enable = True
    def print_effect_start(self, command, current_time, interface): 
        if not self.printing_enable:
            return

        effect_name = command.data[0]
        to_print = f"{current_time} - Activated [{effect_name}]"
        interface.print(to_print)
    
    def print_effect_end(self, effect, current_time, interface): 
        if not self.printing_enable:
            return
        
        effect_name = effect.effect_id
        to_print = f"Deactivated Effect: [{effect_name}] it ran from{effect.start_time} - {current_time}"
        interface.print(to_print)
