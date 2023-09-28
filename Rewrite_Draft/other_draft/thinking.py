from typing import Callable
import time

class PluginInterface():
    callbacks = []
    events = []

    def on_start(self, callback): 
        self.callbacks.append(callback)
    def on_pause(self, callback):
        self.callbacks.append(callback)
    def on_event_triggered(self, name, callback):
        self.callbacks.append(callback)
    def register_event(self, name):
        self.events.append(name)

    def write_to_file(self, text:str):
        print("Write to file", text)
    pass 

class MainLoop():
    events_callbacks = {}

def register_plugin(callback:Callable[[PluginInterface],None]):
    main_loop = MainLoop()

    #maybe check it's not already registered
    interface = PluginInterface()
    callback(interface)


    time.sleep(3)

    for i in interface.callbacks:
        i()

    # merge events into mainLoop.events_callbacks



    for i in interface.callbacks:
        i()

    print(interface.events)

    #now we can keep track of interface and call it from main mode




#----Plugin Writer's File. ----
# Using an interface object and callbacks instead of inheriting from class
# Kind of JavaScript style / """Functional""". In honesty I think "functional" is better cause it's slightly less concepts, more accessable peraps

class Timer():
    def start_timer(self):
        print("started")
    pass

timer = Timer()


def reg_Cut_Action(interface:PluginInterface):
    interface.on_start(lambda : timer.start_timer())

    def do_action():
        interface.write_to_file("Hello")

    interface.register_event("myEvent")
    interface.on_event_triggered("myEvent", do_action)


    pass


# only thing required from plugin writer. Hopefully typing will work 
register_plugin(reg_Cut_Action)