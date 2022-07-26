from proccessors.proccessor_abstract import Proccessor


class TestingProccessor(Proccessor):
    
    def recieve_command(self, command:"TestingCommand", current_time=None):
        print(f"recieved {command} at {current_time}.  Interface: {self.outside_interface}")
    
    def finish_up(self, current_time):
        pass

class TestingCommand():  #probably commands will not be classes just objects w type & data
    type = "test"
    def __init__(self, name="unspecified_name") -> None:
        self.name = name
    
    def get_type(self):
        return self.type

    def __repr__(self) -> str:
        return f"TestingCommand({self.name})"


#---------

#interface = "interface"
#proccessor1 = ToggleEffectProccessor(interface)
