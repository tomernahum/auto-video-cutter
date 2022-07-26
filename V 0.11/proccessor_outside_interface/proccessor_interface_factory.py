
from .interface import Interface
from .control_interface import ControlInterface

class InterfaceFactory():
    def __init__(self, engine) -> None:
        #needs all the components that an interface would use
        self.engine = engine
        pass
    
    
    def get_interface(self, type_handled, proccessor_name="N/A"):
        if type_handled == "control":
            return ControlInterface(self.engine, proccessor_name)

        interface = Interface("tbd", proccessor_name)
        
        return interface

#change proccessors' interfaces

#proccessors.change_interfaces(new_interface_getter_func/factory)
#   for i in proccessors : i.change_interface(factory.get_interface(type/etc))