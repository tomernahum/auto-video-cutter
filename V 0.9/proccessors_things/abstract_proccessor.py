from abc import ABC, abstractmethod


class Proccessor(ABC):
    
    @abstractmethod
    def trigger(self, command, current_time, interface):
        pass
    
    
    def get_display_active_effects(self, current_time):
        return []

    def finish_up(self, current_time, interface):
        pass




class EmptyProccessor(Proccessor):
    def trigger(self, command, current_time, interface):
        pass