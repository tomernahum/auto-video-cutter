from moviepy.editor import clips_array
from moviepy.editor import ImageClip
from moviepy.editor import VideoFileClip


from objects.segments_and_effects import Effect

def get_cut_effect():
    cut_effect = Effect(cut_function, is_breakable=True)
    return cut_effect

def cut_function(segments_list): #Need to think on this
    for clip in segments_list:
        #not tested or correct stuff


        image = ImageClip("example_data.jpg")
        output_clip = clips_array([clip, image])
        pass
        

        
