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
    main_vfc = get_video_file()
    print("got plugins & video file")

    segment_blueprints_list = get_segment_blueprints_from_plugins(plugins) #file = get_open_file()
    print("got segment bps")
    segment_blueprints_list = combine_segment_blueprints(segment_blueprints_list)
    
    print("combined segment bps")

    #convert segment blueprints to segments with VFC clips & effects_to_be_applied
    segments_list = get_segments_list_from_blueprints(segment_blueprints_list, main_vfc)
    print("converted bps to real segments")
    #_print_list(segments_list, "segments")
    #return
    apply_effects_to_segments(segments_list) #bug reported here - segment is showing up as a list (some of the time)
    print("applied all effects")

    output_clips = []
    for i in segments_list:
        output_clips.append(i.get_vfc)
    _print_list(output_clips)
    output_vfc = moviepy.concatenate_videoclips(output_clips)
    output_vfc.write_videofile("output.mp4")

def apply_effects_to_segments(segments_list: list[Segment]):
    #WIP
    #segments_list = segments_list.copy()
    
    """_print_list(segments_list, "segments_list", mode="type")
    
    print("/n----index in segments_list------")
    for index in range(len(segments_list)):
        segment = segments_list[index]
        print(f"type: {type(segment)},   repr: {segment}")
        print(f"|--    effects_list: {segment.get_effects_to_be_applied()}")
    print("done!")"""


    from helper_functions import apply_effects_to_segments as aets
    return aets.main(segments_list)
           


    pass




def get_segments_list_from_blueprints(segment_blueprints_list, main_vfc):
    _print_list(segment_blueprints_list, "input bps")
    output_list = []
    for blueprint in segment_blueprints_list:
        output_list.append(Segment(blueprint, main_vfc))
    _print_list(output_list, "output segments")

    for i in output_list:
        print(type(i))

    return output_list


def combine_segment_blueprints(segment_blueprints):
    import helper_functions.combine_segment_blueprints as csb
    return csb.combine_segment_blueprints(segment_blueprints)

def get_segment_blueprints_from_plugins(plugins, file=None):
    segment_blueprints_extended_list = []
    for plugin in plugins:
        x = get_segment_blueprints_list_from_plugin(plugin, file=get_open_file(plugin))
        segment_blueprints_extended_list.extend(x)
    return segment_blueprints_extended_list


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


def get_video_file():
    #return None
    main_video_file_name = "new_test.mkv"
    #main_video_file_name = input("Enter the video file name: ")
    main_vfc = moviepy.VideoFileClip(main_video_file_name)
    return main_vfc





def testing():
    plugins = get_list_of_plugin_apis("effect_modules")
    plugin = plugins[0]
    realtest = get_segment_blueprints_list_from_plugin(plugin, file="realtest.txt")
    #_print_list(realtest)


def _print_list(list, title=None, mode=None):
    #return
    if __name__ != "__main__":
        return
    
    if title != None:
        print(f"\n-----{title}-----")
    
    if mode == None or mode in {"normal","default"}:
        for i in list:
            print(i)
    
    elif mode == "type":
        for i in list:
            print(type(i))
    
    print(f"\n")

if __name__ == "__main__":
    main()

    

