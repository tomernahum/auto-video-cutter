

from plugin_apis_template import PluginApi   #todo see below (not really a todo)
# I notice that this is hard coded, so if I moved the template I'd have to change each file. 
# Not sure if this is bad or how best to fix it. Maybe there should be 1 file (would have to
# still have a fixed path) with importlib in it that you import and make requests to.

# of course we could pass in the PluginApi / all the imports somehow, I guess it would have 
# to be a class with the main class in it so it can import it. I don't want to confuse any
# potential plugin developers. I bet stackoverflow has an opinion actually

class API(PluginApi):
    def __init__(self) -> None:
        super().__init__()

    def print_plugin_name(self):
        print("test plugin name printing bbby")
    
    def get_added_proccessors(self):
        from .test import ExampleProccessingObj
        return [ExampleProccessingObj]



def print_plugin_name():
    print("test plugin name printing bbby")
    #print(get_string())
    return "test plugin"


def get_added_proccessors():
    return [] #most plugins won't add proccessors