from typing import Protocol
from command_object import Command


class interface(Protocol):
    pass



class Proccessor:

    def __init__(self, outside_interface=None) -> None:
        self.outside_interface=outside_interface

    
    def set_outside_interface(self, outside_interface:interface):
        self.outside_interface = outside_interface

    
    def recieve_command(self, command:Command, current_time):
        ...

    def finish_up(self, current_time):
        pass










