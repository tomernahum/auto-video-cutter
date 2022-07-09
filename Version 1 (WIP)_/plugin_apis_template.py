

from abc import ABC, abstractmethod

from record_mode import ProccessingObj, Command #temp place

class PluginApi(ABC):
    
    def __init__(self) -> None:
        # this is only in a class because of using ABC (it will never be instanciated more than once) 
        # So I don't know if I should make everything class methods or no
        # also I do know about interfaces but I think they arn't good for working with inheretance
        pass


    @abstractmethod
    def print_plugin_name(self):
        print("This statement is in the abc!")

    
    def get_added_proccessors(self) -> list["ProccessingObj"]:
        return []

    
    def get_default_commands(self) -> list["Command"]:    #maybe replace with hotkey:command tuple or dict
        #the idea is for plugins to provide default commands for the user to pick from
        #to actually use by assigning hotkeys to
        return []