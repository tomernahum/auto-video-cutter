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
    list_of_segment_blueprints_lists = []
    for plugin in plugins:
        x = get_segment_blueprints_list_from_plugin(plugin)
        list_of_segment_blueprints_lists.append(x)
    
    combine_segment_blueprints(list_of_segment_blueprints_lists)

def combine_segment_blueprints(list_of_segment_blueprints_lists):
    #x = 
    for i in list_of_segment_blueprints_lists:
        print(i)
    return


def get_segment_blueprints_list_from_plugin(plugin, file=None):
    if file == None: file = get_file(plugin)
    else: file = open(file, 'r')
    result = plugin.get_segment_blueprints_list(file)
    file.close()
    return result

def get_file(plugin):
    #will eventually have to do with interacting w/ plugin
    return open("realtest.txt", 'r')

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
    print_list(realtest)


def print_list(list):
    for i in list:
        print(i)

if __name__ == "__main__":
    testing()

    

