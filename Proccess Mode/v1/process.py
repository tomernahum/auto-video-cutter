from moviepy.editor import *
from moviepy.video import fx

class Segment:
    def __init__(self, t_start, t_end, parent_VFC, effects_list):  #Q/N, optimization: parent_VFC ideally would just be a pointer to main VFC, not a copy, so i guess it should be a global variable
        self.raw_end = t_end
        self.VFC = parent_VFC.subclip(t_start, t_end)
        self.effects_list = effects_list  #effects will be their own objects

    def get_effects_list(self):
        return self.effects_list
    def get_VFC(self):
        return self.VFC
    
    def add_effect(self, effect):
        self.effects_list.append(effect)
    def remove_effect(self, effect):
        self.effects_list.remove(effect)

    def apply_effect_to_own_VFC(self, effect_object): #apply effects on to VFC
        output = effect_object.apply_effect(self.VFC)
        self.VFC = output
    
    def apply_all_effects(self):
        #WIP: may have to add priorities or something
        for effect_object in self.effects_list:
            self.apply_effect_to_own_VFC(effect_object)

    
class Effect:
    def __init__(self):
        pass
    
    def apply_effect(self, VFC:VideoFileClip) -> VideoFileClip:
        return VFC.fx(vfx.blackwhite)

class Greyscale(Effect):
    def __init__(self, intensity):
        self.intensity = intensity #example
    
    def apply_effect(self, VFC:VideoFileClip) -> VideoFileClip:
        return VFC.fx(vfx.blackwhite) #intensity was just an example




def start_process_mode():
    #open timestamps file reader & Master Video File Clip
    video_file_name, timestamps_file = get_file_names_from_user()
    main_VFC = VideoFileClip(video_file_name)
    timestamps_file = open(timestamps_file, 'r')
    
    segments_list = get_segments_list(timestamps_file, main_VFC)

"""
    segment = Segment( 10, 20, main_VFC, effects_list=[Greyscale(100)])
    segment.apply_all_effects()
    #segment.get_VFC().resize(width=500).preview()
    
    output = segment.get_VFC()
    output.write_videofile("test.mp4")

    print("Done!")
"""


def get_file_names_from_user():
    return "test_vid.mkv", "realtest.txt"

def get_segments_list(timestamps_file, main_VFC):
    segments_list = []
    
    #make a .split tuples list of just cut action timestamps (accept/reject/retake/maybe end)
    cut_action_timestamps_list = []  #[0] is timestamp [1] is label
    for line in timestamps_file.readlines()[1:-1]:  #last bit makes it skip 1st & last lines
        split_line = line.strip().split("\t")
        if split_line[1] in {"Accepted","Rejected","Retake A.", "Ended"}:
            cut_action_timestamps_list.append(split_line)
    
    #put cut & none segments in segments_list
    last_timestamp = 0
    for timestamp, label in cut_action_timestamps_list:
        print(timestamp, label)
        #to be continued
        pass

    
    
    
    


if __name__ == "__main__":
    start_process_mode()