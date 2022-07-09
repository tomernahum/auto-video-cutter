#WIP
import importlib


def get_plugin_api(name):
    return importlib.import_module(f"plugins.{name}.api")
    pass



def register_proccessing_objects(plugin_apis, register_function):
    for api in plugin_apis:
        proccessors = api.get_added_proccessors() #most plugins will return empty list
        for i in proccessors:
            register_function(i) #pseudocode

def register_commands(plugin_apis, register_function):
    for api in plugin_apis:
        commands = api.get_added_commands()
        for i in commands:
            register_function(i) #pseudocode



#


def update_dict(key, value):



if True:
    test_plugin = get_plugin_api("test_plugin")



