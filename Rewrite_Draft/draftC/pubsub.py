# from dataclasses import dataclass, field
from enum import Enum

class EventEnum(Enum):
    command_called = "command_called"
    paused = "paused"

    print = "print"


class Event():
    pass


class KeyPressed(Event):
    keyname:str



def dispatchEvent(event:EventEnum, params:dict):
    pass



class recordModeEvents():
    def key_pressed(self, keyName):
        pass
    def time_reached(self, time):
        pass


def subscribeToEvent(event:str, callback):
    pass