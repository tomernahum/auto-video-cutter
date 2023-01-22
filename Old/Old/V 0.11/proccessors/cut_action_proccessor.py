
from typing import TYPE_CHECKING, OrderedDict, Protocol

if TYPE_CHECKING:
    from proccessor_outside_interface.interface import Interface
    from command_object import Command


from proccessors.proccessor_abstract import Proccessor





class CutActionProccessor(Proccessor):
    segments_done = 0
    checkpoints = []


    def recieve_command(self, command, current_time):
        action = command.get_data_piece_i(0)







class cut_action_interface()









"""
commands
Accept
Reject
Reject last accepted
Undu
Flip last action (accept<->reject    undo retake a,  undo undo)



"""