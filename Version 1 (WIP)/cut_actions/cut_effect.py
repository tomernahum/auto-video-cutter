from objects.segments_and_effects import Effect

def get_cut_effect():
    cut_effect = Effect(cut_function, is_breakable=True)
    return cut_effect

def cut_function(clips_list): #Need to think on this
    for clip in clips_list:
        #clip.set_end_time(clip.get_start_time())   #<- currently pseduocode
        
        print(clip)
        pass
        
