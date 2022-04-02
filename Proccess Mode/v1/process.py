from moviepy.editor import *
from moviepy.video import fx


class Constants: 
    accept_ca_label = "Accepted"         #ca means cut action, which itself might be confusing for all i know, good thing about constants though is I can Rename Refactor them easily
    reject_ca_label = "Rejected"
    retake_accepted_ca_label = "Retake A."
    end_ca_label = "Ended"
    ca_set = {accept_ca_label, reject_ca_label, retake_accepted_ca_label, end_ca_label}



class Segment:
    def __init__(self, t_start, t_end, parent_VFC, effects_list):  #Q/N, optimization: parent_VFC ideally would just be a pointer to main VFC, not a copy, so i guess it should be a global variable
        self.raw_end = t_end
        self.raw_start = t_start
        self.VFC = parent_VFC.subclip(t_start, t_end)
        self.effects_list = effects_list  #effects will be their own objects

    def get_effects_list(self):
        return self.effects_list
    def get_VFC(self):
        return self.VFC
    
    def add_effect(self, effect):
        self.effects_list.append(effect)
    def remove_effect(self, effect_to_remove):      #need to test if this works, if not can do isinstance
        for active_effect in self.get_effects_list():
            if isinstance(active_effect, effect_to_remove):
                self.effects_list.remove(active_effect)
    
    def is_cut(self):   
        for effect in self.get_effects_list():
            if isinstance(effect, Cut):
                return True
        return False

    def apply_effect_to_own_VFC(self, effect_object): #apply effects on to VFC
        output = effect_object.apply_effect(self.VFC)
        self.VFC = output
    
    def apply_all_effects(self):    #Q/N: is this the best way of doing this?
        #WIP: may have to add priorities or something
        for effect_object in self.effects_list:
            self.apply_effect_to_own_VFC(effect_object)

    
class Effect:
    def __init__(self):
        pass
    
    def apply_effect(self, VFC:VideoFileClip) -> VideoFileClip:
        return VFC.fx(vfx.blackwhite)

class Cut(Effect):
    def apply_effect(self, VFC:VideoFileClip):
        #return None
        return VFC.subclip(0,0)

class Accepted(Effect):
    def apply_effect(self, VFC: VideoFileClip) -> VideoFileClip:
        return VFC
    #doesn't do anything

class Greyscale(Effect):
    def __init__(self, intensity):
        self.intensity = intensity #example
    
    def apply_effect(self, VFC:VideoFileClip) -> VideoFileClip:
        return VFC.fx(vfx.blackwhite) #intensity was just an example

#...

class DynamicVfxEffect(Effect):  #WIP 4 later
    #WIP: I want it to let you put in ur own effect string and it will do it if it's in the vfx library, end users could ad these in a config file based on movypie docs
    def __init__(self, vfx_effect):
        self.vfx_effect = vfx_effect
        #test if this is a real effect and do something if it isnt
    def apply_effect(self, VFC: VideoFileClip) -> VideoFileClip:
        #return VFC.fx(vfx.)
        pass









def start_process_mode(): #main
    #open timestamps file reader & Master Video File Clip
    video_file_name, timestamps_file = get_file_names_from_user()
    main_VFC = VideoFileClip(video_file_name)
    timestamps_file = open(timestamps_file, 'r')
    
    segments_list = get_segments_list(timestamps_file, main_VFC)
    VFC_list = []
    for segment in segments_list:
        segment.apply_all_effects()
        vfc = segment.get_VFC()
        
        VFC_list.append(vfc)
        #maybe delete the segment todo, also could make it so that it finds & effect-applies segments in chunks not seperatly

    output = concatenate_videoclips(VFC_list)
    
    output.write_videofile("test2.mp4")

    main_VFC.close()

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
    
    segments_list = get_cut_and_keep_segments_list(timestamps_file, main_VFC)
    #get start_stop action effects & mesh all the effects
    


    return segments_list
    

def get_cut_and_keep_segments_list(timestamps_file, main_VFC):
    segments_list = []

    #make a .split tuples list of just cut action timestamps (accept/reject/retake/maybe end)
    cut_action_timestamps_list = []  #[0] is timestamp [1] is label
    for line in timestamps_file.readlines()[1:-1]:  #last bit makes it skip 1st & last lines
        split_line = line.strip().split("\t")
        if split_line[1] in Constants.ca_set:
            cut_action_timestamps_list.append(split_line)
    
    #put cut & none segments in segments_list
    last_timestamp = 0
    for timestamp, label in cut_action_timestamps_list: 
        #print(index, timestamp, label)
        segment = Segment(last_timestamp, timestamp, main_VFC, [])
        
        if label == Constants.reject_ca_label or label == Constants.end_ca_label:
            segment.add_effect(Cut())
        elif label == Constants.accept_ca_label:
            segment.add_effect(Accepted())   #this effect doesn't do anything now
        
        elif label == Constants.retake_accepted_ca_label:
            segment.add_effect(Cut())  #cut out the segment leading up to retake a
            for segment2 in reversed(segments_list): #find the last accepted segment and change it to cut
                if not segment2.is_cut():
                    segment2.remove_effect(Accepted)     #could be hashtagged out if i get rid of accepted effect
                    segment2.add_effect(Cut())
                    break
        
        segments_list.append(segment)
        last_timestamp = timestamp

    
    #for segment in segments_list:
    #    x = ""
    #    if segment.is_cut(): x = "cut"
    #    else: x = "kept"
    #    print (segment.raw_start,"-",segment.raw_end,":",x)

    return segments_list
    
    

    


if __name__ == "__main__":
    start_process_mode()

#possible bug: seems to wait 2 frames after the reject or retake accepted
# command shows up in the recording of the terminal after pressing accepted before cutting