from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from record_mode import Command
    from proccessors_things.proccessors_interface import ControlProccessorsInterface

from proccessors_things.abstract_proccessor import Proccessor



possible_names = [
    "Start/Stop",
    "Start",
    "Stop",
    "Pause"

]



class ControlProccessor(Proccessor):
    def __init__(self) -> None:
        self.possible_commands_to_function = {
            "Start/End" : self.on_start_stop_command,
            "Start": self.on_start_command,
            "Stop" : self.on_stop_command,
            "Pause" : self.on_pause_command,

            
            "Start/Stop" : self.on_start_stop_command,
            }

        pass


    interface: "ControlProccessorsInterface" = None

    def trigger(self, command:"Command", current_time, interface:"ControlProccessorsInterface"):
        self.interface = interface
        command_name = command.get_data(0)
        self.possible_commands_to_function[command_name]()
    
    def on_start_stop_command(self):
        if self.interface.recording_is_started():
            self.on_stop_command()
        else:
            self.on_start_command()

    def on_start_command(self):
        self.interface.start_recording()

    def on_stop_command(self):
        self.interface.end_recording()

    def on_pause_command(self):
        self.interface.pause_recording()