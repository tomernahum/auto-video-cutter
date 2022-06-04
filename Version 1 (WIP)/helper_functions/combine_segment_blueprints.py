from cgi import print_directory
from time import time
from objects.segments_and_effects import *

class effect_toggle:
    #effect
    #id

    def __init__(self, i_d, effect:Effect, time) -> None:
        if effect == None:
            self.effect = None
        else:
            if effect.get_is_homogenius():
                self.effect = effect
            else:
                self.effect = EffectPart(effect, None)
        
        self.id = i_d
        self.time = time
        self.total_part_num = None

    def __repr__(self) -> str:
        return f"Toggle {self.id}: {self.time}, {self.effect}"
    
    def __eq__(self, other) -> bool:
        return self.get_id() == other.get_id()
    
    def get_time(self):
        return self.time
    
    def get_id(self):
        return self.id
    
    def get_effect(self):
        return self.effect

    def increment(self): 
        try:
            self.effect.increment_part_num()
            #self.total_part_num += 1
        except:
            pass
    
    
    def set_part_num(self, n):
        if not self.get_effect().get_is_homogenius():
            self.effect.set_part_num(n)
    
    def set_total_part_num(self, n):
        self.total_part_num = n

    def has_no_effect(self):
        if self.effect == None:
            return True
        return False
    
    def is_final_toggle(self):
        return self.has_no_effect()
    
    pass



#main
def combine_segment_blueprints(segment_blueprints_list: list[SegmentBlueprint]):
    segment_blueprints_list.sort(key=lambda x: x.get_start_time())
    #_print_list(segment_blueprints_list, "sbl!")
    
    effect_toggles = get_effect_toggles(segment_blueprints_list)
    output_sbps = convert_toggles_to_sbp_list_alt(effect_toggles)
    
    #_print_list(effect_toggles, "toggles")
    #_print_list(output_sbps, "dirty output")

    for index, sbp in enumerate(output_sbps[0:1]):  #reorginize
        if sbp.get_start_time() == sbp.get_end_time():
            del output_sbps[index]
    
    #_print_list(output_sbps, "cleaned output")
    return output_sbps

def convert_toggles_to_sbp_list(effect_toggles) -> list[SegmentBlueprint]:
    output_sbps = []
    
    active_effect_toggles = []
    last_timestamp = 0
    for toggle in effect_toggles:
        #print(f"{toggle}, \n\t{active_effect_toggles}")
        
        segment_is_of_length_zero = toggle.get_time() == last_timestamp

        #create the segment ending at this timestamp
        if True:
            effects_list = []
            for active_effect in active_effect_toggles:
                effects_list.append(active_effect.get_effect().get_new_obj())
            output_sbps.append(SegmentBlueprint(last_timestamp, toggle.get_time(), effects_list))


        #add/remove the toggle from active_effects (affects the segment starting at this toggle)
        if toggle.has_no_effect(): 
            break #only the final toggle has no effects
        
        if toggle in active_effect_toggles:
            active_effect_toggles.remove(toggle)
        else:
            toggle.set_part_num(0) #zero cause incremented next
            toggle.set_total_part_num(0)
            active_effect_toggles.append(toggle)
        

        #increment the part numbers of all the active_effects
        if True:
            for active_effect in active_effect_toggles:
                i_is_heterogenius = not active_effect.get_effect().get_is_homogenius()
                if i_is_heterogenius:
                    active_effect.increment()
        else:
            pass
        
        last_timestamp = toggle.get_time()
        pass
    return output_sbps



def convert_toggles_to_sbp_list_alt(toggles_list) -> list[SegmentBlueprint]:
    output_sbps = []

    active_effect_toggles = []
    last_timestamp = 0
    iterator = 0
    while iterator < len(toggles_list):
        
        #build the segment ending at this toggle
        output_sbps.append(build_segment_bp(active_effect_toggles, last_timestamp, current_timestamp=toggles_list[iterator].get_time()))

        #get the current toggles (all toggles with the same time as next unproccessed toggle) & move the iterator past them
        iterator, current_toggles = get_current_toggles_and_iterate(toggles_list, iterator) 
        

        #add/remove toggles from active effects
        for current_toggle in current_toggles:
            add_or_remove_toggle_from_active_toggles(active_effect_toggles, current_toggle)
    
        #increment the part number of all active effects
        for active_toggle in active_effect_toggles:
            active_toggle.increment()

        
        last_timestamp = current_toggles[-1].get_time()
        iterator += 1
    
    return output_sbps

def build_segment_bp(active_effect_toggles, last_timestamp, current_timestamp):
    effects_list = []
    for active_toggle in active_effect_toggles:
        effects_list.append(active_toggle.get_effect().get_new_obj()) #if no get new obj part num continues to update
    return SegmentBlueprint(last_timestamp, current_timestamp, effects_list)

def get_current_toggles_and_iterate(toggles_list, iterator) -> tuple[list[effect_toggle], int]: 
    current_toggles = [toggles_list[iterator]]
    while True:
        if iterator == len(toggles_list) - 1:
            break
            
        if toggles_list[iterator+1].get_time() == current_toggles[0].get_time():
            current_toggles.append(toggles_list[iterator+1])
        else:
            break
        iterator += 1
    return iterator, current_toggles

def add_or_remove_toggle_from_active_toggles(active_toggles: list[effect_toggle], toggle: effect_toggle):
    if toggle.has_no_effect():
        return
    
    if toggle in active_toggles:
        active_toggles.remove(toggle)
    else:
        toggle.set_part_num(0)
        active_toggles.append(toggle)






def get_empty_bps_from_toggles(effect_toggles_list):
    new_segment_bps = []
    last_timestamp = 0
    for toggle in effect_toggles_list:
        new_segment_bps.append(SegmentBlueprint(last_timestamp, toggle.get_time(), []))
    return new_segment_bps






def get_effect_toggles(segment_blueprints_list: list[SegmentBlueprint]) -> list[effect_toggle]:
    effect_toggles = []
    for index, segment_bp in enumerate(segment_blueprints_list):
        start_time = segment_bp.get_start_time()
        end_time = segment_bp.get_end_time()
        for effect_index, effect in enumerate(segment_bp.get_effects_list()):
            toggle_id = index + float("0." + str(effect_index))  #probably bad
            effect_toggles.append(effect_toggle(toggle_id, effect, start_time)) #start
            effect_toggles.append(effect_toggle(toggle_id, effect, end_time)) #end
    
    effect_toggles.sort(key=lambda x: x.get_time())
    
    #add last toggle if previous loop missed it due to it not having effects
    segment_bp = segment_blueprints_list[-1]
    if not segment_bp.has_effects(): 
        start_time = segment_bp.get_start_time()
        end_time = segment_bp.get_end_time()
        effect_toggles.append(effect_toggle(toggle_id, None, start_time)) #start
        effect_toggles.append(effect_toggle(toggle_id, None, end_time)) #end
    

    return effect_toggles





def combine_segment_blueprints_alt(segment_blueprints_list: list[SegmentBlueprint]):
    effect_toggles = get_effect_toggles(segment_blueprints_list)
    
    new_segment_bps = get_empty_bps_from_toggles(effect_toggles)

    active_toggles = []
    for toggle in effect_toggles:
        
        if toggle in active_toggles:
            active_toggles.remove(toggle)
        else:
            active_toggles.append(toggle)
        



    pass




"""
(1,3 A) (2,4 A)



1As 3A 2A 4A 
1As 2Ae 3As 4Ae
(1,2 A) (3,4 A)
(1,2 A) (2,3 AA) (3,44 A)



I: (1,8 A1)  (2,3 A)  (2,5 A)  (4,5 A)  (7,9 A)


"""




if __name__ == "__main__":
    pass





def _print_list(list, title=None):
    if False:
        return
    
    if title != None:
        print(f"\n-----{title}-----")
    try:
        for i in list:
            print(i)
    except:
        print(list)