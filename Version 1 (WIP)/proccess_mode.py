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
    main_video_file_name = input("Enter the video file name")
    main_vfc = moviepy.VideoFileClip(main_video_file_name)

    #combine plugin provided segment_blueprints_list into one segments_list
    segment_blueprints_extended_list = []
    for plugin in plugins:
        x = get_segment_blueprints_list_from_plugin(plugin, file=get_open_file(plugin))
        segment_blueprints_extended_list.extend(x)
    
    segment_blueprints_list = combine_segment_blueprints(segment_blueprints_extended_list)

    #convert segment blueprints to segments with VFC clips & effects_to_be_applied
    segments_list = []
    for segment_blueprint in segment_blueprints_list:
        segments_list.append(Segment(segment_blueprint, main_vfc))
    
    #apply all effects to each segment
    #concatenate & output resulting video



def combine_segment_blueprints(segment_blueprints):
    #TODO: NEEDS BREAKABLITY
    #optimize: could be more efficient (for all I know) 
    
    #convert segment_blueprints to starts & ends
    class start_or_end_effect:
        def __init__(self, time, effects_list):
            self.time = time
            self.effects_list = effects_list
        def __eq__(self, other):
            return self.effects_list == other.effects_list #effects = based on function
        def __repr__(self):
            return f"{self.time}, {type(self).__name__}: {self.effects_list}"
        def get_time(self): return self.time
        def get_effects_list(self): return self.effects_list
    class start(start_or_end_effect): pass
    class end(start_or_end_effect): pass
    class final(start_or_end_effect): pass

    starts_and_ends_list = convert_sbp_to_start_end_list(segment_blueprints, start, end, final)
    
    #create new segment_blueprints based on that
    output_segment_blueprints = []
    open_starts = []  #not a set because there could be 2 of the same effect (then it would apply double)
    last_timestamp = 0
    for start_or_end in starts_and_ends_list:
        timestamp = start_or_end.get_time()
        effects_list = start_or_end.get_effects_list()
        is_start = isinstance(start_or_end, start)
        
        
        #create the last segment
        active_effects_list = []
        for open_start in open_starts:
            active_effects_list.extend(open_start.get_effects_list())
        sbp = SegmentBlueprint(last_timestamp, timestamp, active_effects_list)
        output_segment_blueprints.append(sbp)
        
        #update open effects list
        if isinstance(start_or_end, final):
            break
        if is_start:
            open_starts.append(start_or_end)
        else: #if is end
            #remove corresponding start from active_effects
            open_starts.remove(start_or_end) #start_or_ends equal based on effects list regardless of start/end status

        last_timestamp = timestamp
    
    #_print_list(output_segment_blueprints)

    return output_segment_blueprints

def convert_sbp_to_start_end_list(segment_blueprints, start, end, final):
    #_print_list(segment_blueprints)
    starts_and_ends_list = []
    for segment_blueprint in segment_blueprints:
        effects_list = segment_blueprint.get_effects_list()
        start_time = segment_blueprint.get_start_time()
        end_time = segment_blueprint.get_end_time()
        
        if effects_list == []:
            continue
        starts_and_ends_list.append(start(start_time, effects_list))
        starts_and_ends_list.append(end(end_time, effects_list))
    
    starts_and_ends_list.sort(key=lambda x: x.get_time())
    starts_and_ends_list.append(final(segment_blueprints[-1].get_end_time(), []))
    return starts_and_ends_list



def get_segment_blueprints_list_from_plugin(plugin, file=None):
    if file == None: file = get_open_file(plugin)
    else: file = open(file, 'r')
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

    

