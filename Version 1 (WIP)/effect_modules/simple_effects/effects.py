from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx 
#todo make above imports only import whats needed / etc. Also this could be more functional if it wants

from objects.segments_and_effects import Effect

def get_effect(effect_name):
    if effect_name in {"Flip", "flip"}:
        return get_flip_effect()
    elif effect_name in {"BlackWhite", "black-white", "blackwhite"}:
        return get_blackwhite_effect()
    return f"effect name error; name: {effect_name}"

def get_flip_effect():
    effect = Effect("flip", flip_function, is_homogenius=False)
    return effect

def get_blackwhite_effect():
    effect = Effect("black-white", bw_function, is_homogenius=True)
    return effect

def flip_function(segments_list):
    output = []
    for i in segments_list:
        new_clip = i.fx(vfx.mirror_y)
        output.append(new_clip)
    return output

def bw_function(segments_list):
    output = []
    for i in segments_list:
        new_clip = i.fx(vfx.black_white)
        output.append(new_clip)
    return output

#could this be made into functions that take & return functions? (yes obviously)