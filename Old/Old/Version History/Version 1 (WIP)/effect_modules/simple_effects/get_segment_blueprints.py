
from objects.segments_and_effects import SegmentBlueprint
from . import effects

#main / called on from api
def get_segment_blueprints_list(effects_file):
    return scan_toggle_file(effects_file, get_effect)
    #above function could go in general library and parent function could go straight in api

def scan_toggle_file(toggle_file, get_effect_function):  #can be put into general library
    #needs an end timestamp or else it will not work
    file = get_list_from_timestamps_file(toggle_file)
    file = truncate_file_list_to_two(file)

    output = []
    active_effects = set()
    last_timestamp = 0
    for timestamp, effect_name, in file:
        #build the segment ending at this timestamp
        segment_blueprint = SegmentBlueprint(last_timestamp, timestamp, [])
        for i in active_effects:
            segment_blueprint.add_effect(get_effect_function(i))
        output.append(segment_blueprint)

        #update the effects for the next segment
        if effect_name in active_effects:
            active_effects.remove(effect_name)
        else:
            active_effects.add(effect_name)
        
        last_timestamp = timestamp
        

    return output
        

def get_list_from_timestamps_file(timestamps_file):  #todo: copied code, eventually will put these in library
    result = []
    lines = timestamps_file.readlines()[1:-1] #last bit makes it skip 1st & last lines
    for line in lines:  
        split_line = line.strip().split("\t")
        split_line[0] = float(split_line[0])
        result.append(split_line)
    return result

def truncate_file_list_to_two(file):
    new = []
    for i in file:
        n = []
        n.append(i[0])
        n.append(i[1])
        new.append(n)
    return new

def get_effect(effect_name):
    return effects.get_effect(effect_name)




if __name__ == "__main__":
    file = open("effects_test.txt", 'r')
    x = get_segment_blueprints_list(file)
    file.close()
    for i in x:
        print(x)