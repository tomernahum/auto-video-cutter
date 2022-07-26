
from proccessors.proccessor_abstract import Proccessor

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from proccessor_outside_interface.control_interface import ControlInterface
    from command_object import Command


class ControlProccessor(Proccessor):

    outside_interface:"ControlInterface"

    def __init__(self, outside_interface=None) -> None:
        super().__init__(outside_interface)


        self.commands_func_dict = {
            "test" : self.on_test,
            "start/stop" : self.start_stop,
        }

    
    
    def recieve_command(self, command:"Command", current_time):
        command2 = command.get_data_piece_i(0)
        self.commands_func_dict[command2](current_time)



    def on_test(self, current_time):
        self.outside_interface.notify("hello!", current_time)


    def start_stop(self, current_time):
        if self.outside_interface.recording_is_started():
            self.outside_interface.end_recording()
            self.outside_interface.notify("ended recording", current_time)
        else:
            self.outside_interface.start_recording()
            self.outside_interface.notify("started recording", current_time)