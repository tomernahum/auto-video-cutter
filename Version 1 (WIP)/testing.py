
from objects.segments_and_effects import *


def combine_segment_blueprints_test():
    from helper_functions import combine_segment_blueprints as csb
    
    cut_effect = Effect("cut", print("cut_t"), False)
    flip_effect = Effect("flip", print("flip_t"), False)
    bw_effect = Effect("bw", print("bw_t"), False)
    zoom_effect = Effect("zoom", print("zoom_t"), False)
    

    sb_list = get_sb_list_2(cut_effect, flip_effect, bw_effect, zoom_effect)
    
    csb.combine_segment_blueprints(sb_list)

def get_sb_list_1(cut_effect, flip_effect, bw_effect, zoom_effect):
    sb_list = []
    sb_list.append(SegmentBlueprint(0, 3, effects_list=[cut_effect]))
    sb_list.append(SegmentBlueprint(2, 4, effects_list=[flip_effect, bw_effect]))
    #sb_list.append(SegmentBlueprint(1, 2.5, effects_list=[zoom_effect]))
    return sb_list
    #passes

def get_sb_list_2(cut_effect, flip_effect, bw_effect, zoom_effect):
    sb_list = []
    sb_list.append(SegmentBlueprint(0, 3, effects_list=[cut_effect]))
    sb_list.append(SegmentBlueprint(2, 4, effects_list=[flip_effect, bw_effect]))


    sb_list.append(SegmentBlueprint(6, 10, effects_list=[flip_effect]))
    return sb_list







combine_segment_blueprints_test()