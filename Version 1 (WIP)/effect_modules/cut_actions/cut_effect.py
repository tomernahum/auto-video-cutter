from moviepy.editor import clips_array
from moviepy.editor import ImageClip
from moviepy.editor import VideoFileClip


from objects.segments_and_effects import Effect

def get_cut_effect():
    cut_effect = Effect("cut", cut_function, is_homogenius=True)
    return cut_effect

def cut_function(segments_list): #Need to think on this
    output = []
    for segment in segments_list:
        vfc = segment.get_vfc()
        segment.set_vfc(vfc.subclip(0,0))
        output.append(segment)
    return output
        

"""
image = ImageClip("example_data.jpg")
        output_clip = clips_array([clip, image])
"""
