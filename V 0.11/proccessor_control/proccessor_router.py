from typing import Protocol


class Command(Protocol):
    def get_type(self) -> str:
        ...


class ProccessorInterface(Protocol):
    def recieve_command(self, command, current_time):
        ...
    
    def finish_up(self):
        pass

    #def set_outside_interface(self, interface):
    #    ...   #this would be in the proccessor but not for the purposes of router



class ProccessorRouter:
    proccessor_interfaces : dict[str, ProccessorInterface] = {
    }  #command_type : proccessor_interface  #interface is just a proccessor in this context see above

    def register_proccessor(self, proccessor_interface:ProccessorInterface, command_type_it_handles:str):
        self.proccessor_interfaces[command_type_it_handles] = proccessor_interface


    def recieve_command(self, command:Command, current_time):
        if command.get_type() not in self.proccessor_interfaces.keys():
            raise self.CommandTypeNotRecognized(command.get_type())

        proccessor_interface = self.proccessor_interfaces[command.get_type()]
        
        proccessor_interface.recieve_command(command, current_time)

    class CommandTypeNotRecognized(Exception):
        pass



#-------

class commanddirty():
    def __init__(self, name, type):
        self.type = type

    def get_type(self):
        return self.type

class proccessordirty(ProccessorInterface):
    def __init__(self, interface, whattoprint="") -> None:
        self.interface = interface
        self.what_to_print = whattoprint

    def recieve_command(self, command, current_time):
        print(f"{self.what_to_print}{command}")
    
    def finish_up(self):
        pass

    def set_outside_interface(self, interface):
        pass

if __name__ == "__main__111":
    proccessor1 = proccessordirty("none")
    
    pr = ProccessorRouter()

    #pr.register_proccessor("command_type", proccessor1)
    
    cmd = commanddirty("x", "fake type")
    pr.recieve_command(cmd, "current_time")



    proccessors = []
    def register_proccessor(proccessor, command_type_it_handles):
        proccessor.set_outside_interface("...")
        proccessors.append(proccessor)
        pr.register_proccessor(proccessor, command_type_it_handles)
    
    register_proccessor(proccessor1, "command_type")

if __name__ == "__main__":
    proccessor_1 = proccessordirty("interface", "111")
    prout = ProccessorRouter()

    prout.register_proccessor(proccessor_1, "command_type")
    cmd = commanddirty("x", "command_type")
    
    prout.recieve_command(cmd, "current_time")

    proccessor_1.what_to_print = "222"
    
    prout.recieve_command(cmd, "current_time")




    pass