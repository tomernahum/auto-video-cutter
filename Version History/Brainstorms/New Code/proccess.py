"""
1) Get Segments
2) Apply homogenius effects
3) Apply heterogenius effects
4) Apply super_heterogenius effects
) 2/3 can be combined.  that and 4) may be a ble to be combined as well
5) convert segments to output video


1) Convert timestamps file to segments
2) 

"""
from moviepy.editor import *
from moviepy.video import fx


class Segment():
    VFC = None
    effects_to_be_applied = None
    
    def __repr__(self) -> str:
        result = ""
        for effect in self.get_effects_list():
            result += repr(effect)
            result += "&"
        return result

    def __init__(self, VFC_subclip, effects_list) -> None:  
        self.VFC = VFC_subclip
        self.effects_to_be_applied = effects_list  #effects are their own objects

    def get_vfc(self): return self.VFC
    def get_unapplied_effects(self): return self.effects_to_be_applied

    def apply_effect(self, effect_from_list):
        #pseudocode/untested/temp
        self.effects_to_be_applied.pop(effect_from_list)
        self.VFC = effect_from_list.apply_effect_to_vfc(self.VFC)
        return self.VFC



def convert_file_timestamps_to_segments(timestamps_file_lines, parent_VFC:VideoFileClip):
    
    timestamps_data_list = convert_timestamp_file_lines_to_data(timestamps_file_lines)

    return
    segments_list = []
    active_effects = []
    for timestamp, label, data in timestamps_data_list:
        segment_effects = []
        if label in {"Accepted","Rejected","Retaking A.", "Ended"}:
            if label == "Rejected" or label == "Ended":
                segment_effects.append("Cut")
            elif label == "Accepted":
                segment_effects.append("Accepted")
            elif label == "Retake A.":
                pass
            


        else:
            pass




    

def convert_timestamp_file_lines_to_data(timestamps_file_lines):
    #convert lines into data list that is easier to work with
    data = []
    for line in timestamps_file_lines[1:-1]: #skips 1st & last lines
        split_line = line.strip().split("\t")
        if len(split_line) == 2:
            split_line.append("")
        data.append(tuple(split_line))
    
    #convert cut_actions into cuts
    print(data)
    for a in data:
        pass
    
    
    
    
    return data



if __name__ == "__main__":
    with open("1.txt", 'r') as timestamps_file:
        file_lines = timestamps_file.readlines()
        convert_file_timestamps_to_segments(file_lines, None)
    
    
    
