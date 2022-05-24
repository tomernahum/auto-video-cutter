
from objects.segments_and_effects import SegmentBlueprint

from ..cut_actions import cut_effect

def get_cut_effect():
    return cut_effect.get_cut_effect()


#main / called on from proccess mode
def get_segment_blueprints_list(timestamps_file):
    timestamps_list = get_list_from_timestamps_file(timestamps_file)
    
    segment_blueprints_list = build_segment_blueprints_list(timestamps_list)
    #for i in segments_list: print(i)
    #print("------------")
    segment_blueprints_list = simplify_segment_blueprints_list(segment_blueprints_list)
    #for i in segments_list: print(i)

    return segment_blueprints_list
    
    
    

def build_segment_blueprints_list(timestamps_list):
    segments_list = []
    last_timestamp = 0
    last_segment_cut = None
    for timestamp, label in timestamps_list: 
        segment = SegmentBlueprint(last_timestamp, timestamp, effects_list=[])
        
        if label == "Rejected" or label == "Ended":
            segment.add_effect(get_cut_effect())
                
            last_segment_cut = True
        elif label == "Accepted":
            last_segment_cut = False
            pass
        elif label == "Retake A.": #reject last accepted
            segment.add_effect(get_cut_effect())
            
            for past_segment in reversed(segments_list):
                if not segment_is_cut(past_segment):
                    past_segment.add_effect(get_cut_effect())
                    break
            
            last_segment_cut = True
        
        segments_list.append(segment)
        last_timestamp = timestamp
    return segments_list

def simplify_segment_blueprints_list(input_segments_list):
    new_segments_list = []
    
    last_input_segment_cut_status = None
    new_segment_start = None
    new_segment_end = None
    new_segment_effects_list = None
    for current_input_segment in input_segments_list:
        current_input_segment_cut_status = segment_is_cut(current_input_segment)

        if last_input_segment_cut_status == current_input_segment_cut_status: #if cut status is the same as the last segment's
            new_segment_end = current_input_segment.get_end_time()
        else:
            if new_segment_start != None:
                new_segment = SegmentBlueprint(new_segment_start, new_segment_end, new_segment_effects_list)
                new_segments_list.append(new_segment)
            
            new_segment_start = current_input_segment.get_start_time()
            new_segment_end = current_input_segment.get_end_time()
            new_segment_effects_list = current_input_segment.get_effects_list()
        
        last_input_segment_cut_status = segment_is_cut(current_input_segment)
        
    
    return new_segments_list

    

def segment_is_cut(segment:SegmentBlueprint):
    if segment.has_effect():
        return True
    return False




def get_list_from_timestamps_file(timestamps_file):
    result = []
    for line in timestamps_file.readlines()[1:-1]:  #last bit makes it skip 1st & last lines
        split_line = line.strip().split("\t")
        result.append(split_line)
    return result



if __name__ == "__main__":
    file = open("realtest.txt", "r")
    x = get_segment_blueprints_list(file)
    file.close()

    for i in x:
        print(i)




