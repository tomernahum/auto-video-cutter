

class SegmentBlueprint:
    #Clip coordinates
    #List of Effects
    def __repr__(self) -> str:
        return f"({self.start_time}, {self.end_time}):{self.effects_list}"


    def __init__(self, start_time, end_time, effects_list) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.effects_list = effects_list
    
    def add_effect(self, effect):
        self.effects_list.append(effect)

    def get_start_time(self): return self.start_time
    def get_end_time(self): return self.end_time
    def get_effects_list(self): return self.effects_list

    def has_effect(self):
        if self.effects_list == []:
            return False
        return True


class Effect:
    #concrete function
    #breakability

    def __init__(self, function, is_breakable) -> None:
        self.function = function