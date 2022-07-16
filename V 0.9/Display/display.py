
import time
from typing import TYPE_CHECKING
from utils import utils

from Display.displays_inteface import DisplaysInterface


if TYPE_CHECKING:
    from Display.displays_inteface import DisplaysInterface


#I will replace this with a model & display system

class Display():
    def __init__(self) -> None:
        self.display_is_active = True
        self.printing_line_rn = False
        
        self.MIN_PRINT_LEN = 100   #sign of how its not a perfect printing system. Maybe there is a library for this kind of thing
    
    def print(self, to_print): #prints over the updating display that would otherwise mess it up
        
        print_fill = " " * (self.MIN_PRINT_LEN - len(to_print))   #used to override updating display
        
        to_print = replace_tabs_w_spaces_in_str(to_print)
        to_print = "\r" + to_print + print_fill
        
        self.printing_line_rn = True
        print(to_print)
        self.printing_line_rn = False

    def start_updating_display(self, interface:DisplaysInterface):
        self.display_is_active = True
        while self.display_is_active:
            if self.printing_line_rn:
                continue
            
            
            self.update_updating_display(interface)
            time.sleep(0.1)

    def stop_updating_display(self):
        self.display_is_active = False

    
    
    def update_updating_display(self, interface:DisplaysInterface):
        
        to_print = self.get_print_data_for_updating_display(interface)  
        #Q/A: for it to be well-organized, should the display not be calling anything (it is calling the get_active_effects_for_display in each proccessor indirectly) but instead some controller push updates to the state/model of the display? - maybe.
        
        print("\r" + to_print, end="")

    def get_print_data_for_updating_display(self, interface):
        active_effects = interface.get_active_effects()
        
        to_print_active_effects = self.get_active_effects_print_str(active_effects)
        to_print_time = interface.get_formatted_current_time()


        to_print = f"{to_print_time}\t\t Active Effects: {to_print_active_effects}"
        return to_print

    



    def get_active_effects_print_str(self, active_effects):
        to_print_active_effects:str = ""
        for effect_name, effect_runtime in active_effects:
            formatted_effect_runtime = self.format_raw_time(effect_runtime)
            to_print_active_effects += f"[{effect_name}]({formatted_effect_runtime}), "
        
        return to_print_active_effects

    def format_raw_time(self, raw_time):
        return utils.format_time(raw_time)


def replace_tabs_w_spaces_in_str(input_string, tabstop = 8): #taken from old file
    from math import ceil
    def find_next_multiple(x, base):
        return base * ceil(x/base)
    
    result = ""
    split_string = input_string.split('\t')
    for section in split_string: 
        diff = find_next_multiple(len(section), tabstop) - len(section)
        if diff == 0: diff = tabstop
        result += section
        result += " " * diff
    return result




"""
off topic: was just watching a vid about MVC. 
So under that system we would want a controller to call start_updating_display 
and pass in active effects (?), and also call display.print()

ok rn we have proccessor's interface which has a reference to the display in it
we also have display's interface which has the list of proccessors in it + the timer

both these lists are passed in to the interfaces from the main file and created / 
stored in my mind in the Engine class

ok so for mvc:
proccessor objects would call the main controller (instead of their own interface to the engine), 
which would then call the display to update.


Boils down to:
rn the display calls the controllers for some things and the controllers call the display for other things
these are done through their own interface class so its organized but maybe this is still high coupling?

so we could have another middleman between the middlemen

or we could have the display never call anything only get called to update by controller






"""