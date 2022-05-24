

class SegmentBlueprint:
    #Clip coordinates (start&stop time)
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
        self.is_breakable = is_breakable
        self.is_dumb_unbreakable = None
        #if unbreakable:
        #   Function takes in a list of Segments & returns a list of Segments
        #if breakable:
        #   Function takes in a single Segment & returns a single Segment
        #if bad:
        #   Function takes in a list of segments & returns a single segment
    
    def is_breakable(self): return self.is_breakable
    def get_function(self): return self.function





class Segment:
    # Clip/ VFC
    # Effects_to_be_applied
    pass