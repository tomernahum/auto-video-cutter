from moviepy.editor import *
from moviepy.video import fx

class Segment:
    def __init__(self, t_start, t_end, parent_VFC, effects_list):
        self.raw_start = t_start
        self.raw_end = t_end
        self.VFC = parent_VFC.subclip(t_start, t_end)
        self.effects_list = effects_list  #effects will be their own objects

    def get_effects_list(self):
        return self.effects_list
    def get_VFC(self):
        return self.VFC
    
    def apply_effect_to_self(self, effect_object): #apply effects on to VFC
        output = effect_object.apply_effect(self.VFC)
        self.VFC = output
    
    def apply_all_effects(self):
        #WIP: may have to add priorities or something
        for effect_object in self.effects_list:
            self.apply_effect_to_self(effect_object)

    
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
    video_file_name = "test_vid.mkv"
    main_VFC = VideoFileClip(video_file_name)
    
    
    segment = Segment( 10, 20, main_VFC, effects_list=[Greyscale(100)])
    segment.apply_all_effects()
    #segment.get_VFC().resize(width=500).preview()
    
    output = segment.get_VFC()
    output.write_videofile("test.mp4")

    print("Done!")

if __name__ == "__main__":
    start_process_mode()