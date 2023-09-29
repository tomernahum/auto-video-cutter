from typing import Callable
from utils import addToListDict


class PluginInterface():
    start_callbacks = []
    events_callbacks = {}

    def __init__(self, name:str) -> None:
        self.name = name

    def on_start(self, callback): 
        self.start_callbacks.append(callback)
    def on_pause(self, callback):
        pass

    # aka register event
    def on_event_triggered(self, name, callback):
        addToListDict(self.events_callbacks, name, callback)



    def write_to_file(self, text:str):
        print("Write to file", text)

    def mark_timestamp(self, timestamp:str, text:str):
        print(f"Writing to file: {self.name}: {timestamp}: text", text)
    def mark_current_timestamp(self, text:str):
        self.mark_timestamp("current time", text)

    def print(self, text:str):
        print(text)
    
    
    # editing phase
    def registerEditFunction(self, func, onesInterestedIn):
        pass
    

    # def requestConfigVariable(self, name):
    #     look up from shared config object whos read the json file

    pass 


# todo put this right
class MainLoop():
    events_callbacks = {}
    start_callbacks = []

    def register_plugin(self, callback:Callable[[PluginInterface],None]):
        _register_plugin(self, callback)


    def startRecordMode(self):
        for i in self.start_callbacks:
            i()

    def triggerEvent(self, eventName:str):
        callbacks = self.events_callbacks.get(eventName, [])
        for e in callbacks:
            e()


def _register_plugin(main_loop:MainLoop, callback:Callable[[PluginInterface],None]):
    #maybe check it's not already registered
        
    interface = PluginInterface("PluginName")
    callback(interface)
    # merge events into mainLoop.events_callbacks
    for k,v in interface.events_callbacks.items():
        # print(">", k, v,interface.events_callbacks)
        addToListDict(main_loop.events_callbacks, k, v)
    main_loop.start_callbacks.extend(interface.start_callbacks)


main_loop = MainLoop()
def register_plugin(callback:Callable[[PluginInterface, dict],None]):
    global main_loop
    main_loop.register_plugin(callback)