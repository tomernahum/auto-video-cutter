from typing import Callable
import time

class PluginInterface():
    callbacks = []
    events_callbacks = {}

    def on_start(self, callback): 
        self.callbacks.append(callback)
    def on_pause(self, callback):
        self.callbacks.append(callback)
    def on_event_triggered(self, name, callback):
        addToListDict(self.events_callbacks, name, callback)
    # def register_event(self, name):
    #     self.events.append(name)

    def write_to_file(self, text:str):
        print("Write to file", text)
    pass 

class MainLoop():
    events_callbacks = {}

# def addToListDict(dict, key, value):
#     if key not in dict:
#         dict[key] = [value]
#     else:
#         dict[key].append(value)
def addToListDict(dictt, key, value):
    isList = isinstance(value, list)

    if key not in dictt:
        if isList:
            dictt[key] = value
        else:
            dictt[key] = [value]
    else:
        if isList:
            dictt[key].extend(value)
        else:
            dictt[key].append(value)

def register_plugin(callback:Callable[[PluginInterface],None]):
    main_loop = MainLoop()

    #maybe check it's not already registered
    
    interface = PluginInterface()
    callback(interface)

    # merge events into mainLoop.events_callbacks
    for k,v in interface.events_callbacks.items():
        # print(">", k, v,interface.events_callbacks)
        addToListDict(main_loop.events_callbacks, k, v)

    # time.sleep(3)

    
    # call all callbacks
    for i in interface.callbacks:
        i()

    print(main_loop.events_callbacks)
    print(interface.events_callbacks)
    
    def triggerEvent(eventName:str):
        callbacks = main_loop.events_callbacks.get(eventName, [])
        for e in callbacks:
            e()

    triggerEvent("myEvent")
    triggerEvent("nooneslistening")

    triggerEvent("printTime")
    time.sleep(3)
    triggerEvent("printTime")
    # obviously irl to be triggered by shortcuts




#---------  Plugin's File. ------------


# Using an interface object and callbacks instead of inheriting from class
# Kind of JavaScript style / """Functional""". In honesty I think "functional" is better cause it's slightly less concepts, more accessable peraps. but maybe it's less idiomatic or maybe it only seems that way

from utils import Timer

timer = Timer()


def register_CutActions_plugin(interface:PluginInterface):
    interface.on_start(lambda : timer.start_timer())

    def do_action():
        interface.write_to_file("Hello")

    interface.on_event_triggered("myEvent", do_action)
    interface.on_event_triggered("myEvent", lambda: print("Hello2"))

    interface.on_event_triggered("printTime", lambda: print(f"{timer.get_formatted_current_time()} Hi"))


    pass


# only thing required from plugin writer. Hopefully typing will work 
register_plugin(register_CutActions_plugin)