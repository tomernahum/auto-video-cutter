
import time
from typing import TYPE_CHECKING
from utils import utils

from Display.displays_inteface import DisplaysInterface


if TYPE_CHECKING:
    from Display.displays_inteface import DisplaysInterface


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
        return utils.time_formatter(raw_time)


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