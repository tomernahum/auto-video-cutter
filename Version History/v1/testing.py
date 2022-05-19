from tracemalloc import start
from moviepy.editor import *
#import effect_functions as e_funcs



def test1():
    def get_effect_function(effect_name):
        if effect_name == "flip":
            return e_funcs.flip
        else:
            return e_funcs.effect_name #does not work (I want it to be the effect_name passed into the function - Likely have to make a new function in e_funcs that takes a string as input. So these things arn')

    class Effect:
        def __init__(self, name) -> None:
            self.name = name
            self.function = get_effect_function(name)

        def run_function(self, VFC):
            return self.function(VFC)


    class Segment:
        def __init__(self, main_vfc, start, end, effects_list=[]) -> None:
            self.parent_vfc = main_vfc
            self.start = start
            self.end = end
            self.subclip_vfc = None
            self.effects_list = effects_list

        def add_effect(self, effect:Effect):
            self.effects_list.append(effect)

        def _create_subclip_vfc_if_not_created(self):  #can be done not at the same time as initialized 
            if self.subclip_vfc == None:
                self.subclip_vfc = self.parent_vfc.subclip(self.start, self.end)

        def get_clip(self):
            self._create_subclip_vfc_if_not_created()
            return self.subclip_vfc

        def apply_all_effects(self) -> VideoFileClip:
            self._create_subclip_vfc_if_not_created()
            for i in self.effects_list:
                self.apply_effect(i)
            return self.subclip_vfc
        
        def apply_effect(self, effect:Effect):
            self._create_subclip_vfc_if_not_created()
            self.subclip_vfc = effect.run_function(self.subclip_vfc)



    main_clip = VideoFileClip("trimmed_vid_for_testing.mp4")

    flip_effect = Effect("blackwhite")


    segment = Segment(main_clip, 8, 10)
    segment.add_effect(flip_effect)


    #segment.get_clip().resize(0.5).preview()

    flipped = segment.apply_all_effects()
    flipped.resize(0.5).preview()

def test2():
    import testing_b
    
    class Test:
        class_var = 1
        def __init__(self, var) -> None:
            self.class_var = var

    for name, val in testing_b.__dict__.items():
        if callable(val):
            print(name, val)
            new_func_name = testing_b.__name__ + name
            setattr(Test, testing_b.__name__)

    for key, value in testing_b.functions.items():
        new_function_name = 

    
    




test2()