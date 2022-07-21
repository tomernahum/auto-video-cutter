

from typing import Protocol


class GeneralProccessorOutsideInterface():
    def __init__(self) -> None:
        
        pass

    def set_proccessor_who_it_belongs_to(self, val):
        pass

class ControlProccessorOutsideInterface():
    pass


class ProccessorOutsideInterface(Protocol):
    def set_proccessor_who_it_belongs_to(self, val):
        pass


class ProccessorHolder():
    proccessors = []

    general_proccessors_interface:ProccessorOutsideInterface = GeneralProccessorOutsideInterface()
    control_proccessors_interface = ControlProccessorOutsideInterface()

    def register_proccessor(self, proccessor, proccessor_router):
        interface = self.get_outside_interface_for_proccessor(proccessor)
        
        self.proccessors

    def get_outside_interface_for_proccessor(self, proccessor):
        
        if proccessor.get_command_type_handled() == "Control":
            return "..."
        
        return self.general_proccessors_interface.set_proccessor_who_it_belongs_to("")

        #maybe input proccessor i belong to to interface








if __name__ == "__main__":
    from proccessor_router import ProccessorRouter


    proccessor_router = ProccessorRouter()
    proccessor_router.register_proccessor()

    pass


#we will in another file define the full abstract proccessor (probably an abc)
#then in our main program we will call proccessor_holder.register_proccessor(x), with x being a proccessor of course
#that may have been defined in a plugin etc