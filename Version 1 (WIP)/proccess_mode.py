"""
Input:
- Main Video
- output video file name
- record mode data
    - each mod creates its own record mode data file
    - these are zipped into one file
"""

"""
Code:
- Unzip data files
- Call proccess mode functions in each mod passing in their corresponding data file
- Get lists of segments (clip & effects_list[specific function & info])
    - Segment: Clip & Effects_list
    - Effects List:
        - list of concrete functions (only input is vfc clips)
            - (may just be calling another function & passing in specific inputs)
        - each with data on breakability
            - function Input: VFC clips
            - function output: VFC clips
- Combine lists of segments into one list
    - some effects will get broken up into "parts"
- Apply the effect functions in the segments (to the input video)
    - 
- output the final video
"""


"""
Code:
 - get data from mod
 - get lists of segment_blueprints from each mod (pass in appropriate data)
 - combine all segment blueprints and convert to segments w clips on main video
 - apply all the effects
 - output
"""

import moviepy.editor as moviepy
import importlib
from objects.segments_and_effects import *


def main():
    PLUGINS_DIRECTORY_NAME = "effect_modules" #I will change this to effect_plugins later
    
    plugins = get_list_of_plugin_apis(PLUGINS_DIRECTORY_NAME)

    #get files from user
    #main_video_file_name = input("Enter the video file name: ")
    #main_vfc = moviepy.VideoFileClip(main_video_file_name)

    #combine plugin provided segment_blueprints_list into one segments_list
    segment_blueprints_extended_list = []
    for plugin in plugins:
        x = get_segment_blueprints_list_from_plugin(plugin, file=get_open_file(plugin))
        segment_blueprints_extended_list.extend(x)
    
    segment_blueprints_list = combine_segment_blueprints(segment_blueprints_extended_list)

    #convert segment blueprints to segments with VFC clips & effects_to_be_applied
    #segments_list = []
    #for segment_blueprint in segment_blueprints_list:
    #    segments_list.append(Segment(segment_blueprint, main_vfc))
    
    #apply all effects to each segment
    #concatenate & output resulting video



def combine_segment_blueprints(segment_blueprints):
    #TODO: NEEDS BREAKABLITY
    #optimize: could be more efficient (for all I know) 
    
    #convert segment_blueprints to starts & ends objects (type, timestamp, effect)
    start_effect_obj, end_effect_obj, final_effect_obj = get_start_end_effect_objs()
    starts_and_ends_list = convert_sbp_to_start_end_list(segment_blueprints, start_effect_obj, end_effect_obj, final_effect_obj)
    
    #create new segment_blueprints based on that
    new_segment_blueprints = convert_start_end_objs_to_segment_blueprints(starts_and_ends_list)
    
    return new_segment_blueprints

def get_start_end_effect_objs():
    class start_or_end_effect:
        def __init__(self, time, effect):
            self.time = time
            self.effect = effect
        def __eq__(self, other):
            return self.effect == other.effect #effects = based on function
        def __repr__(self):
            return f"{self.get_type_str()}, {self.time} : {self.effect}"
        def get_time(self): return self.time
        def get_effect(self): return self.effect
        def get_type_str(self):
            if isinstance(self, start_effect_obj): return "start"
            elif isinstance(self, end_effect_obj): return "end"
            else: return "final"
        def is_homogenius(self):
            return self.effect.get_is_homogenius()  
        def is_heterogenius(self):
            return not self.is_homogenius()
        def set_part_num(self, n):
            self.effect.set_part_num(n)
        def increment_part_num(self):
            self.effect.increment_part_num()
    class start_effect_obj(start_or_end_effect): pass
    class end_effect_obj(start_or_end_effect): pass
    class final_effect_obj(start_or_end_effect): pass
    return start_effect_obj, end_effect_obj, final_effect_obj


def convert_sbp_to_start_end_list(segment_blueprints, start_effect_obj, end_effect_obj, final):
    #_print_list(segment_blueprints)
    starts_and_ends_list = []
    for segment_blueprint in segment_blueprints:
        effects_list = segment_blueprint.get_effects_list()
        start_time = segment_blueprint.get_start_time()
        end_time = segment_blueprint.get_end_time()
        
        if effects_list == []:
            continue
        for effect in effects_list:
            starts_and_ends_list.append(start_effect_obj(start_time, effect))
            starts_and_ends_list.append(end_effect_obj(end_time, effect))
    
    starts_and_ends_list.sort(key=lambda x: x.get_time())
    starts_and_ends_list.append(final(segment_blueprints[-1].get_end_time(), "Final"))
    return starts_and_ends_list

def convert_start_end_objs_to_segment_blueprints(starts_and_ends_list): #starts_and_ends_list must be sorted
    #still bugged, kind of tired rn, (hetero effects counts dont reset/work)
    _print_list(starts_and_ends_list)
    output = []

    active_toggles = []
    last_timestamp = 0
    for toggle in starts_and_ends_list:
        timestamp = toggle.get_time()
        effect = toggle.get_effect()
        toggle_type = toggle.get_type_str()
        print(f"{timestamp}\t {type}\t {effect}")
        

        #create the segment_bp ending at this toggle
        output_segment_effects = [x.get_effect() for x in active_toggles] #first time using [] not yet tested
        output_segment = SegmentBlueprint(last_timestamp, timestamp, output_segment_effects)
        output.append(output_segment)

        #update active toggles for next segment_bp based on current toggle
        if toggle_type == "final":
            break
        
        elif toggle_type == "start":
            if toggle.is_heterogenius():
                toggle.set_part_num(0)  #0 because it will be increased next    if bug could be related to this?
            active_toggles.append(toggle)
        elif toggle_type == "end":
            active_toggles.remove(toggle)  #objects are = if their effects are (which are = if their function is)

        #increase any hetero active toggle' part numbers by 1
        for toggle in active_toggles:
            if not toggle.is_homogenius():
                toggle.increment_part_num()

        last_timestamp = timestamp

    _print_list(output)
    
    






def get_segment_blueprints_list_from_plugin(plugin, file=None):
    result = plugin.get_segment_blueprints_list(file)
    file.close()
    return result

def get_open_file(plugin):
    #will eventually have to do with interacting w/ plugin
    file = open(plugin.get_file_name(), 'r')
    return file

def get_list_of_plugin_apis(plugins_folder_name):
    list_of_plugin_names = get_list_of_plugin_names(plugins_folder_name)
    
    list_of_plugin_modules = []
    for plugin_name in list_of_plugin_names:
        plugin_module = importlib.import_module(plugins_folder_name + "." + plugin_name + ".api")
        list_of_plugin_modules.append(plugin_module)
    
    return list_of_plugin_modules


def get_list_of_plugin_names(plugins_folder):  #Q/A what if this was indented in the above function cause thats the only place its used & it clutters the outline (this applies to all functions that are just seperating out code from other functions)
    #code partially stolen from stackoverflow
    import os
    list_dir = os.listdir(plugins_folder)
    
    output = []
    for plugin_directory in list_dir:
        plugin_path = os.path.abspath(plugins_folder) + os.sep + plugin_directory 
        if os.path.isdir(plugin_path) and os.path.exists(plugin_path + os.sep + "__init__.py"):
            output.append(plugin_directory)
    
    return output
    #return ["cut_actions"]








def testing():
    plugins = get_list_of_plugin_apis("effect_modules")
    plugin = plugins[0]
    realtest = get_segment_blueprints_list_from_plugin(plugin, file="realtest.txt")
    #_print_list(realtest)


def _print_list(list):
    for i in list:
        print(i)

if __name__ == "__main__":
    main()

    

