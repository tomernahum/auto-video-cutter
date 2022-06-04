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

    def has_effects(self):
        if self.effects_list == []:
            return False
        return True


class Effect:
    #concrete function
    #breakability/homogeneity
    
    def __repr__(self) -> str:
        return f"({self.name} effect: ({self.function}))"
    
    def __repr__(self) -> str: return f"({self.name})" #comment-out-able  #, {self.get_part_num()}

    def __init__(self, name, function, is_homogenius) -> None:
        self.name = name
        self.function = function
        self.is_homogenius = is_homogenius
        #self.is_dumb_unbreakable = None
        #homogenius: can be broken up into multiple clips and effect will come out the same
        #heterogenius: effect must be applied to entire area at once; breaking it up would make it wrong
        #super-hetrogenius: can't overlap at all (try to avoid this) (not yet implemented)
    
    def __eq__(self, other) -> bool:
        try: return (self.function == other.function)
        except: return False
    
    def get_is_homogenius(self): return self.is_homogenius
    def get_function(self): return self.function

    def get_new_obj(self):
        return Effect(self.name, self.function, self.is_homogenius)
    


class EffectPart(Effect): #Q/A is inherentance better (or any different)?
    #effect
    #part_num
    def __init__(self, effect:Effect, part_num) -> None: 
        super().__init__(effect.name, effect.function, effect.is_homogenius) #Q/A I want it to do this automatically in case I ever add attributes but I dont know how
        self.part_num = part_num

    def __repr__(self) -> str:
        return  f"({self.name}, {self.part_num})"

    def get_new_obj(self):
        return EffectPart(Effect(self.name, self.function, self.is_homogenius), self.part_num)

    def get_part_num(self): 
        return self.part_num

    def set_part_num(self, new_num): 
        self.part_num = new_num
    
    def increment_part_num(self): 
        self.part_num += 1
    
    
    



class Segment:
    # Clip/ VFC
    # Effects_to_be_applied
    def __init__(self, segment_bp:SegmentBlueprint, parent_vfc:moviepy.VideoFileClip):
        self.effects_to_be_applied = segment_bp.get_effects_list()
        self.blueprint = segment_bp
        #below could be seperated to act only once its needed if ever needed
        self.vfc = parent_vfc.subclip(segment_bp.get_start_time(), segment_bp.get_end_time())

    def __repr__(self) -> str:
        return F"(effects_tba:{self.effects_to_be_applied})"
    
    def get_vfc(self) -> moviepy.VideoFileClip:
        return self.vfc
    def get_effects_to_be_applied(self) -> list[Effect]:
        return self.effects_to_be_applied
    
    def set_vfc(self, vfc):
        self.vfc = vfc

    def remove_effect_to_be_applied(self, effect):
        self.effects_to_be_applied.remove(effect)
    
    def has_effect(self, effect):
        effect in self.effects_to_be_applied

    @staticmethod
    def apply_effect_to_segment_s(segment_or_segment_list, effect:Effect):
        if type(segment_or_segment_list) == Segment:
            segments_list = [segment_or_segment_list]
        else:
            segments_list = segment_or_segment_list
        
        #V not sure if this modifies the original input so returning it just in case
        function = effect.get_function()
        segments_list = function(segments_list)
        for i in segments_list:
            i.remove_effect_to_be_applied(effect)
        
        return segments_list
        
    
    
    

    pass