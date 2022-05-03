import time
from tokenize import String
from moviepy.editor import *
from moviepy.video import fx


class Constants: 
    accept_ca_label = "Accepted"         #ca means cut action, which itself might be confusing for all i know, good thing about constants though is I can Rename Refactor them easily
    reject_ca_label = "Rejected"
    retake_accepted_ca_label = "Retake A."
    end_ca_label = "Ended"
    ca_set = {accept_ca_label, reject_ca_label, retake_accepted_ca_label, end_ca_label}
    #not all string labels are constants as of now


class Segment:
    def __init__(self, t_start, t_end, parent_VFC, effects_list):  #Q/N, optimization: parent_VFC ideally would just be a pointer to main VFC, not a copy, I think this is what it already is? but I'm not sure. Should it be a class var?
        self.raw_end = t_end
        self.raw_start = t_start
        self.VFC = parent_VFC.subclip(t_start, t_end)     #optimize: could move this to the get function so its not slowed down doing this 
                                                          #Q/N: Question: if I store parent vfc as a class variable will it copy it or store a reference to it
        self.effects_list = effects_list  #effects will be their own objects

    def __repr__(self) -> str:
        result = ""
        for effect in self.get_effects_list():
            result += repr(effect)
            result += "&"
        return result

    def get_effects_list(self):
        return self.effects_list
    def get_VFC(self):
        return self.VFC 
    
    def add_effect(self, effect_name):
        self.effects_list.append(Effect(effect_name))
    
    def remove_effect(self, effect_to_remove):      
        for active_effect in self.get_effects_list():
            if active_effect.get_effect_name() == effect_to_remove.get_effect_name():
                self.effects_list.remove(active_effect)
    
    def is_cut(self):   
        for effect in self.get_effects_list():
            if effect.get_effect_name() == "Cut":
                return True
        return False

    def apply_effect_to_own_VFC(self, effect_object): #apply effects on to VFC
        output = effect_object.apply_effect_function(self.VFC)
        self.VFC = output
    
    def apply_all_effects(self):    #Q/N: is this the best way of doing this?
        #WIP: may have to add priorities or something
        for effect_object in self.effects_list:
            self.apply_effect_to_own_VFC(effect_object)
        
        return self.get_VFC()




class Effect:
    #so an effect is name & function, while a segment is vfc & list of effects
    @staticmethod
    def get_effect_function(name):
        functions_dict = {
            "Cut" : lambda VFC : VFC.subclip(0,0) ,
            "Accepted" : lambda VFC : VFC , #returns itself (does nothing)

            "Flip" : lambda VFC : VFC.fx(vfx.mirror_y),
            "BlackWhite" : lambda VFC : VFC.fx(vfx.blackwhite),

            "CenterZoom" : None,
            "SpeedUp" : lambda VFC, data_list : vfx.speedx(VFC, factor=data_list[1]) ,
            
            #we can also point to other static functions if the function is longer or put all the functions in a seperate file
            #then it could be setup so the user can input somewhere effectname, hotkey, and function (or name of moviepy function and it would be sorted automatically)
        }
        
        return functions_dict[name]

    def __init__(self, name, data=[]):
        self.effect_name = name
        self.effect_function = Effect.get_effect_function(name) #maybe needs some sort of data checking thing
        self.effect_data_list = data
    
    def __repr__(self) -> str:
        return self.get_effect_name()

    def __eq__(self, __o: object) -> bool:
        pass

    def get_effect_name(self): return self.effect_name
    
    def get_effect_function(self): return self.effect_function

    def get_effect_data(self): return self.effect_data_list

    def apply_effect_function(self, VFC:VideoFileClip):
        if self.get_effect_data() == []:
            return self.get_effect_function()(VFC)
        else:
            return self.get_effect_function()(VFC, self.get_effect_data())




#...









def start_process_mode(): #main
    #open timestamps file reader & Master Video File Clip
    video_file_name, timestamps_file_name = get_file_names_from_user()
    main_VFC = VideoFileClip(video_file_name)
    timestamps_file = open(timestamps_file_name, 'r')
    
    #convert timestamps into segments (each segment can have multiple effects)
    print("building segments...")
    segments_list = get_segments_list(timestamps_file, main_VFC)
    
    

    #apply the effects to the video file clips in the segment objects
    print("applying segments...")
    processed_VFCs_list = []
    for segment in segments_list:
        segment.apply_all_effects()
        vfc = segment.get_VFC()   
        
        processed_VFCs_list.append(vfc)
        #todo maybe delete the segment, or seperate the proccessing and the extracting
    
    #todo could make it so that it builds the segments & applies effects to them in chunks of effects with overlapping segments not all at once so that if the file is super long it doesn't take up infinite memory

    output = concatenate_videoclips(processed_VFCs_list)
    
    output.write_videofile("test2.mp4")

    main_VFC.close()



def get_file_names_from_user():  
    return "test_vid.mkv", "realtest.txt"
    vid_file_name = input("Enter the name of the video file to process: ")
    timestamps_file_name = input("Enter the name of the timestamps file with which to process: ")
    return vid_file_name, timestamps_file_name


def get_segments_list(timestamps_file, main_VFC):
    segments_list = []
    
    segments_list = get_cut_and_keep_segments_list(timestamps_file, main_VFC)
    #get start_stop action effects & mesh all the effects
    
    print (segments_list)

    

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
            segment.add_effect("Cut")
        elif label == Constants.accept_ca_label:
            segment.add_effect("Accepted")   #this effect doesn't do anything now
        
        elif label == Constants.retake_accepted_ca_label:
            segment.add_effect("Cut")  #cut out the segment leading up to retake a
            for segment2 in reversed(segments_list): #find the last accepted segment and change it to cut
                if not segment2.is_cut():
                    segment2.remove_effect("Accepted")     #could be hashtagged out if i get rid of accepted effect
                    segment2.add_effect("Cut")
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