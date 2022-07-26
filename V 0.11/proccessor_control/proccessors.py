from typing import Protocol
from proccessors.proccessor_abstract import Proccessor
from proccessor_control.proccessor_router import ProccessorRouter
#from proccessor_outside_interface.proccessor_interface_factory import InterfaceFactory
class InterfaceFactoryProtocol(Protocol):
    def get_interface(self, type_handled, proccessor_name="N/A"):
        ...


class ProccessorHolder():
    types_proccessors : dict[str, Proccessor] = {
    }
    
    def register_proccessor(self, proccessor:Proccessor, command_type_it_handles:str):
        self.types_proccessors[command_type_it_handles] = proccessor

    def change_interface(self, command_type, new_interface):
        self.types_proccessors[command_type].set_outside_interface(new_interface)

    def get_types_list(self):
        return self.types_proccessors.keys()


class Proccessors: #may rename
    
    
    def __init__(self, interface_factory) -> None:
        self.proccessor_router = ProccessorRouter()
        self.proccessor_holder = ProccessorHolder()  #this may be redundant?  #may be merged into this its literally a dict


        self.interface_factory:InterfaceFactoryProtocol = interface_factory

    def register_proccessor(self, proccessor_class, command_type_it_handles:str): #to be indirectly called on by plugins probably
        #get interface
        interface = self._get_interface_for_proccessor(command_type_it_handles) #will need an additional param once i fix naming
        
        #create proccessor
        proccessor = proccessor_class(interface)
        
        #register proccessor
        self.proccessor_router.register_proccessor(proccessor, command_type_it_handles)
        self.proccessor_holder.register_proccessor(proccessor, command_type_it_handles)

    def _get_interface_for_proccessor(self, command_type_proccessor_handles):
        proccessor_name = f"{command_type_proccessor_handles} proccessor" #likely will have to put name w proccessor storage or in proccessor- or maybe the name is unnecessary (probably would be used for ui display purposes)
        #ie name should be able to be specified by plugin / different from command type name (maybe a proccessor handles commands of multiple types for some reason) - I guess we can forbid that and keep the type/name the same actually
        #eg Toggle, CutAction, SkipSilence - that might be a toggle)

        interface = self.interface_factory.get_interface(command_type_proccessor_handles, proccessor_name)
        return interface
    
    def change_interfaces(self, new_interface_factory): #WIP
        self.interface_factory = new_interface_factory
        for i in self.proccessor_holder.get_types_list():
            new_interface = self._get_interface_for_proccessor(i)
            self.proccessor_holder.change_interface(i, new_interface)


    def recieve_command(self, command, current_time):
        self.proccessor_router.recieve_command(command, current_time)




    



if __name__ == "__main__":
    
    
    from proccessors.testing_proccessor import TestingProccessor, TestingCommand
    from proccessor_outside_interface.proccessor_interface_factory import InterfaceFactory
    
    
    x = Proccessors(InterfaceFactory())
    
    x.register_proccessor(TestingProccessor, "test")
    
    c = TestingCommand()

    x.proccessor_router.recieve_command(c, 0)

    
    x.proccessor_router.recieve_command(c, 1)