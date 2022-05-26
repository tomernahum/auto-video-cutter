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


import importlib


def main():
    PLUGINS_DIRECTORY_NAME = "effect_modules" #I will change this to effect_plugins later
    
    plugins = get_list_of_plugin_apis(PLUGINS_DIRECTORY_NAME)

    #combine plugin provided segment_blueprints_list into one segments_list
    segment_blueprints_list = []
    for plugin in plugins:
        x = get_segment_blueprints_list_from_plugin(plugin)
        segment_blueprints_list.extend(x)
    
    combine_segment_blueprints(segment_blueprints_list)

def combine_segment_blueprints(segment_blueprints):
    #optimize: could be more efficient (for all I know) 
    
    #convert segment_blueprints to starts & ends
    class start_or_end_effect:
        def __init__(self, time, effects_list):
            self.time = time
            self.effects_list = effects_list
        def __repr__(self):
            return f"{self.time}, {type(self).__name__}: {self.effects_list}"
        def get_time(self): return self.time
    class start(start_or_end_effect): pass
    class end(start_or_end_effect): pass

    starts_and_ends_list = []
    for segment_blueprint in segment_blueprints:
        effects_list = segment_blueprint.get_effects_list()
        start_time = segment_blueprint.get_start_time()
        end_time = segment_blueprint.get_end_time()
        
        starts_and_ends_list.append(start(start_time, effects_list))
        starts_and_ends_list.append(end(end_time, effects_list))
    
    starts_and_ends_list.sort(key=lambda x: x.get_time())
    
    _print_list(starts_and_ends_list)


    #create new segment_blueprints based on that
    for start_or_end in starts_and_ends_list:
        timestamp = start_or_end.get_time()
        effects_list = start_or_end.get_effects_list





    #sorted_list = sorted(list_of_segment_blueprint_lists, key=lambda x: x.get_start_time() )

    return


def scan_toggle_file(toggle_file, get_effect_function):  #can be put into general library
    #needs an end timestamp or else it will not work
    file = get_list_from_timestamps_file(toggle_file)
    file = truncate_file_list_to_two(file)

    output = []
    active_effects = set()
    last_timestamp = 0
    for timestamp, effect_name, in file:
        #build the segment ending at this timestamp
        segment_blueprint = SegmentBlueprint(last_timestamp, timestamp, [])
        for i in active_effects:
            segment_blueprint.add_effect(get_effect_function(i))
        output.append(segment_blueprint)

        #update the effects for the next segment
        if effect_name in active_effects:
            active_effects.remove(effect_name)
        else:
            active_effects.add(effect_name)
        
        last_timestamp = timestamp
        

    return output


def get_segment_blueprints_list_from_plugin(plugin, file=None):
    if file == None: file = get_file(plugin)
    else: file = open(file, 'r')
    result = plugin.get_segment_blueprints_list(file)
    file.close()
    return result

def get_file(plugin):
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
    _print_list(realtest)


def _print_list(list):
    for i in list:
        print(i)

if __name__ == "__main__":
    main()

    

