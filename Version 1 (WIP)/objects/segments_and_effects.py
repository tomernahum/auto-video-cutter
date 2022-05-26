import moviepy.editor as moviepy

class SegmentBlueprint:
    #Clip coordinates (start&stop time)
    #List of Effects
    def __repr__(self) -> str:
        return f"({self.start_time}, {self.end_time}):{self.effects_list}"


    def __init__(self, start_time, end_time, effects_list=[]) -> None:
        self.start_time = float(start_time)
        self.end_time = float(end_time)
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
    
    def __repr__(self) -> str:
        if self.is_breakable:
            b = "breakable"
        else: b = "unbreakable"
        return f"{self.name} Effect: ({b}, {self.function})"
    
    def __repr__(self) -> str: return f"{self.name}" #comment-out-able

    def __init__(self, name, function, is_breakable) -> None:
        self.name = name
        self.function = function
        self.is_breakable = is_breakable
        self.is_dumb_unbreakable = None
        #if unbreakable:
        #   Function takes in a list of Segments & returns a list of Segments
        #if breakable:
        #   Function takes in a single Segment & returns a single Segment
        #if bad:
        #   Function takes in a list of segments & returns a single segment
    
    def __eq__(self, other) -> bool:
        return (self.function == other.function)
            
    
    def is_breakable(self): return self.is_breakable
    def get_function(self): return self.function





class Segment:
    # Clip/ VFC
    # Effects_to_be_applied
    def __init__(self, segment_bp:SegmentBlueprint, parent_vfc:moviepy.VideoFileClip):
        self.effects_to_be_applied = segment_bp.get_effects_list()
        self.blueprint = segment_bp
        #below could be seperated to act only once its needed if ever needed
        self.vfc = parent_vfc.subclip(segment_bp.get_start(), segment_bp.get_end())

    
    def get_vfc(self):
        return self.vfc
    

    pass