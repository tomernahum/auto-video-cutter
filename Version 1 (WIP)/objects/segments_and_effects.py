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
        if self.is_homogenius:
            part_num = "N/A"
        else: part_num = self.get_part_num()
        return f"{self.name} Effect: ({part_num}, {self.function})"
    
    def __repr__(self) -> str: return f"({self.name}, {self.get_part_num()})" #comment-out-able

    def __init__(self, name, function, is_homogenius, broken_part_num=None) -> None:
        self.name = name
        self.function = function
        self.is_homogenius = is_homogenius
        self.broken_part_num = broken_part_num #if heterogenius break into parts
        #self.is_dumb_unbreakable = None
        #homogenius: can be broken up into multiple clips and effect will come out the same
        #heterogenius: effect must be applied to entire area at once; breaking it up would make it wrong
        #super-hetrogenius: can't overlap at all (try to avoid this) (not yet implemented)
    
    def __eq__(self, other) -> bool:
        return (self.function == other.function)
            
    
    def get_is_homogenius(self): return self.is_homogenius
    def get_function(self): return self.function
    def get_part_num(self): 
        if self.is_homogenius:
            return ""
        return self.broken_part_num

    def set_part_num(self, new_num): self.broken_part_num = new_num
    def increment_part_num(self): self.broken_part_num += 1





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