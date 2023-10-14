


"""
    possible events:
    1) KeyPressed, keyName=""
"""

from enum import Enum
from dataclasses import dataclass


class Event:
    def __init__(self, event_name) -> None:
        self.event_name = event_name

@dataclass
class command_called(Event):
    commandName:str
    def __init__(self):
        super().__init__("command_called")


class Signal:

    def publish(self, eventName:str, **kwargs):
        print(eventName, kwargs)
        pass
    
    def publish2(self, event:Event):
        self._publish(event.event_name, event)
    def _publish(self, eventName, event:Event):
        pass

    def subscribe(self, event:str, callback):
        pass
    
    def unsubscribe(self, event, callback)





s = Signal()

s.publish2(command_called())


