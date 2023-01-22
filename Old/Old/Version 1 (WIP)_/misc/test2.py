
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from test1 import EffectData
    from test1 import Display
    from test1 import Writer


class ToggleEffectsProccessing:
    effect_category = "toggle_effect"
    
    class ActiveEffect:
        def __init__(self, effect) -> None:
            self.effect = effect
            self.timer = None #will be timer object (or just implement timer directly)
        
        def __eq__(self, other): #used for finding in list to remove
            return self.effect.name == other.effect.name

    def __init__(self):
        self.active_effects = []

    def trigger(self, effect:"EffectData", display:"Display", writer:"Writer"): #will get called when hotkey is pressed #Q/A I can't specify the types of everything since its later in the file and they feed into each other - is them feeding in to each other bad design?
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
    
    def get_active_effects(self):
        output = []
        for i in self.active_effects:
            pass
        return 
   
    def add_active_effect(self, effect):
        self.active_effects.append(self.ActiveEffect(effect))
    
    def remove_active_effect(self, effect):
        self.active_effects.remove(effect)
    def is_effect_active(self, effect):
        return effect in self.active_effects
    

    def get_active_effect_names(self):
        output = ""
        for effect in self.active_effects:
            output += effect.name
        return output
    
    #todo: need stuff to interface with active effect timers 
    # - I think the active_effect class should be a part of this only so its more modular