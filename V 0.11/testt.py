import keyboard


from proccessor_outside_interface.proccessor_interface_factory import InterfaceFactory
from proccessor_control.proccessors import Proccessors
from command_object import Command
from custom_timer import Timer


class X:
    def __init__(self) -> None:
        self.proccessors = Proccessors(InterfaceFactory(self))
        self.timer = Timer()

        self.recording_state = "" #wip
        

    def on_input_trigger(self, command:Command):
        if (not self.is_recording_and_unpaused()) and command.get_type() != "control":  #ie recording has not started or is paused
            return
        
        #print(f"{command}, {self.timer.get_current_time_format_1()}")
        
        self.proccessors.recieve_command(command, self.timer.get_current_time())

    def initialize(self):
        self.stall() #might be something wrong here

        #self.start_recording()
        

    
    def start_recording(self):
        self.recording_state = "Starting"
        
        self.timer.start_timer()
        #self._register_input()
        #start display / anything else
        
        
        self.recording_state = "Recording"
        
        pass

    def pause_recording(self):
        pass

    def end_recording(self):
        pass


    def get_recording_state(self):
        return self.recording_state

    def is_recording(self):
        return self.recording_state == "Recording" or self.recording_state == "Paused"
    
    def is_paused(self):
        return self.recording_state == "Paused"

    def is_recording_and_unpaused(self):
        return self.recording_state == "Recording"



    def stall(self): #wip idk
        keyboard.wait("space")


    def register_proccessor(self, proccessor_class, type):
        self.proccessors.register_proccessor(proccessor_class, type)

    def register_hotkey(self, hotkey, command):  #temp - will eventually be more than just hotkeys / might be reorganized    (dynamic input types eg hand gesture detection)
        keyboard.add_hotkey(hotkey, self.on_input_trigger, [command])



if __name__ == "__main__":
    x = X()

    #eventually this would be done by dynamic plugins
    from proccessors.testing_proccessor import TestingProccessor
    from proccessors.control_proccessor import ControlProccessor
    
    x.register_proccessor(TestingProccessor, "test")
    x.register_proccessor(ControlProccessor, "control")
    #x.register_proccessor(None, "toggle")


    x.register_hotkey("alt+x", Command(type="test", data=["alt+x"]))
    x.register_hotkey("q", Command(type="test", data=["q"]))
    
    x.register_hotkey("ctrl+shift+\\", Command(type="control", data=["start/stop"]))
    x.register_hotkey("alt+t", Command(type="control", data=["test"]))
    
    
    x.initialize()














if False:
    interface_factory = InterfaceFactory()
    p = Proccessors(interface_factory)
    p.register_proccessor(TestingProccessor, "test")
    p.recieve_command(TestingCommand("test"), 555)

    from command_object import Command

    p.recieve_command(Command("testt"), 556)


#------------------------


