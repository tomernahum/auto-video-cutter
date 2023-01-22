import time
import keyboard

from Display.displays_inteface import DisplaysInterface
from proccessors_things.abstract_proccessor import Proccessor

class Command():
    def __init__(self, type, data=None) -> None:
        self.type = type
        self.data = data

    def get_type(self): return self.type

    def get_data(self, index):
        return self.data[index] #todo error checkig ig

    def __repr__(self) -> str:
        return f"Command(type: {self.type}, data:{self.data}"


        

class Engine:
    #maybe some responsibilities should be split up / made more clearer. Like another object for the lookups idk i didnt sleep enough
    
    def __init__(self) -> None:
        self.is_started = False
    
    def initialize_objects(self):
        from utils.custom_timer import Timer
        from proccessors_things.proccessors_interface import ProccessorsInterface
        from Display.display import Display
        
        self.timer = Timer()
        
        self.display = Display()
        self.proccessors_s_interface = ProccessorsInterface(self.display)
    
    def start_record_mode(self):
        #get output file name
        #get input config file name

        #get hotkeys out of config file
        #register hotkeys
            #each hotkey triggers a certain PRs trigger function
        
        #Run input monitoring & the display

        #get effect ranges & specifications from PRs & write them to file
        
        output_file_name = "effects_specification.txt"
        config_file_name = "config_file.json"

        self.initialize_objects()
        

        from proccessors_things.toggle_proccessor import ToggleProccessor
        from proccessors_things.control_proccessor import ControlProccessor  #temp way of importing
        from proccessors_things.abstract_proccessor import EmptyProccessor
        self.command_type_proccessor_pairs : dict[str,Proccessor] = {
            "Control": ControlProccessor(),
            "Toggle": ToggleProccessor(),
            "CutAction": EmptyProccessor(),
        }

        #proccessor_command_type_pairs = {
        #    "Toggle" : ToggleCommand,
        #}   or put that in above thing or leave it w out this to reduce complexity

        self.hotkey_command_pairs = {
            "ctrl+shift+\\" : Command("Control", ["Start/End"]),
            "ctrl+shift+p" : Command("Control", ["Pause"]),
            
            
            "alt+u" : Command("Toggle", ["URLZoom", None]),
            "alt+i" : Command("Toggle", ["SkipSilence", None]),
            
            "alt+q" : Command("CutAction", ["Accept"]),
            "alt+w" : Command("CutAction", ["Reject"]),
            
        }
        
        #register hotkeys & commands
        for hotkey, command in self.hotkey_command_pairs.items():
            proccessor = self.command_type_proccessor_pairs[command.get_type()]
            keyboard.add_hotkey(hotkey, self.trigger, args=[command, proccessor])

        #things will be started from the control proccessor hotkeys
        bad = "ctrl+shift+\\"
        print(f"press {bad} to start recording ")
        keyboard.wait()
    
    def start_recording(self):
        self.timer.start_timer()
        self.display.start_updating_display(DisplaysInterface(self.timer, self.command_type_proccessor_pairs))
        self.is_started = True
        
        time.sleep(1)
        self.display.print(f"started. current_time:{self.timer.get_current_time_formatted()}")
    
    def end_recording(self):
        #tell proccessors that we are ending
        for proccessor in self.command_type_proccessor_pairs.values():
            proccessor.finish_up(self.timer.get_current_time(), self.proccessors_s_interface)
        
        #stop the display
        self.display.stop_updating_display()
        self.is_started = False

        #close the file
        
        print("should be done now")

    def pause_recording(self):
        pass

    
    def trigger(self, command, proccessor):
        if not self.is_started:
            if not command.type == "Control":
                print(f"cant execute {command}")
                return
            
        
        interface = self.proccessors_s_interface    

        if command.type == "Control":            
            from proccessors_things.proccessors_interface import ControlProccessorsInterface
            interface = ControlProccessorsInterface(self)
        
        
        current_time = self.timer.get_current_time_truncated()
        self.display.print(f"triggering command: {command},    proccessor: {proccessor}")
        proccessor.trigger(command, current_time, interface)


if __name__ == "__main__":
    engine = Engine()
    engine.start_record_mode()




#PRS:
    #control PR can do the following:
        #start the recording
        #end the recording
        #pause the recording
    
    # a PR can do the following:
        #ask for input
        #provide information to be displayed

        #provide an effect specification for writing



