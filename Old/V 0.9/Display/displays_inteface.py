
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from utils.custom_timer import Timer
    from proccessors_things.abstract_proccessor import Proccessor

class DisplaysInterface(): #Display's Interface  #todo better name perhaps
    def __init__(self, timer, proccessors:dict[str, "Proccessor"]):
        self.timer: Timer = timer
        self.proccessors = proccessors #command_type_proccessor_pairs

    def get_active_effects(self):
        current_time = self.timer.get_current_time() #should this be passed in?
        
        active_effects = []
        for name, proccessor in self.proccessors.items():
            active_effects.extend(proccessor.get_display_active_effects(current_time))
        return active_effects

    def get_formatted_current_time(self):
        return self.timer.get_current_time_formatted()