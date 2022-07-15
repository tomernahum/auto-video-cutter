import keyboard
from proccessors_things.toggle_proccessor import ToggleProccessor
from Display.displays_inteface import DisplaysInterface
from proccessors_things.abstract_proccessor import Proccessor, EmptyProccessor

class Command():
    def __init__(self, type, data=None) -> None:
        self.type = type
        self.data = data

    def get_type(self): return self.type

    def __repr__(self) -> str:
        return f"Command(type: {self.type}, data:{self.data}"


        

class Engine:
    def initialize_objects(self):
        from utils.custom_timer import Timer
        from proccessors_things.proccessor_interface import ProccessorsInterface
        from Display.display import Display
        
        self.timer = Timer()
        
        self.display = Display()
        self.interface = ProccessorsInterface(self.display)
    
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
        

        #import config_file_parser
        #config_data = config_file_parser.get_config_data(config_file_name)
        
        command_type_proccessor_pairs = {
            "Toggle": ToggleProccessor(),
            "CutAction": EmptyProccessor()
        }

        hotkey_command_pairs = {
            "alt+u" : Command("Toggle", ["URLZoom"]),
            "alt+i" : Command("Toggle", ["SkipSilence"]),
            
            "alt+q" : Command("CutAction", ["Accept"]),
            "alt+w" : Command("CutAction", ["Reject"]),
            
        }
        
        for hotkey, command in hotkey_command_pairs.items():
            proccessor = command_type_proccessor_pairs[command.get_type()]
            keyboard.add_hotkey(hotkey, self.trigger, args=[command, proccessor])

        #start stuff
        self.timer.start_timer()
        self.display.start_updating_display(DisplaysInterface(self.timer, command_type_proccessor_pairs))
        keyboard.wait("space")
    
    def trigger(self, command, proccessor):
        interface = self.interface    
        current_time = self.timer.get_current_time_truncated()
        #print(f"command: {command}, proccessor: {proccessor}, \ncurrent time: {current_time}")
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



