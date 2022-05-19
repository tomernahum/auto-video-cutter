from moviepy.editor import *
from moviepy.video import fx

#from (someone's custom functions file) import class


class example_effects_pack: #may be a package instead of a class
    @staticmethod
    def get_names_to_functions_dict(): #required
        names_to_functions_dict = {"greyflip": example_effects_pack.custom_func_example}
        return names_funcs_dict
    
    @staticmethod
    def custom_func_example(VFC):
        #blah
        #blah
        #blah
        result = VFC
        result = result.fx(vfx.blackwhite)
        result = result.fx(vfx.mirror_y)
        return result


names_to_functions_dict = {}
for effects_pack in [example_effects_pack]:
    names_to_functions_dict = {**names_to_functions_dict, **effects_pack.get_names_to_functions_dict()}

    



def flip(VFC:VideoFileClip):
    return VFC.fx(vfx.mirror_y)

def blackwhite(VFC:VideoFileClip):
    return VFC.fx(vfx.blackwhite)

def test(str):
    print(str)












def dynamic_effect_function(effect_name, VFC:VideoFileClip): #needs option for inputs...
    names_funcs_dict[effect_name](VFC)

names_funcs_dict = {"blackwhite": blackwhite,
                    "flip": flip
                    }
#still no way to add functions from a config file












