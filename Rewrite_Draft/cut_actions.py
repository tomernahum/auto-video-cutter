from plugins import Action, Plugin, PluginsToMainInterface
from utils import Timer

# Written as a 



class CutActions(Plugin):
    timer = Timer() # should this be done in main loop and then actions are called w current time?   
    #^ also todo: ms support etc

    def __init__(self, actions:PluginsToMainInterface):
        #self.segmentTimer = Timer()
        self.actions = actions
        pass
    
    def on_start(self):
        self.timer.start_timer()


    def get_actions_1(self) -> list[Action]:
        return [self.StartNewSegment(self)]

    def get_actions_2(self):
        return {
            "StartNewSegment": self.start_new_segment_action,
            "TestAction": self.test_action
        }

    # choose one of the below 2 formats
    class StartNewSegment(Action):
        def __init__(self, outer):  #outer:CutActions
            self.outer = outer

        name = "StartNewSegment" #name used for config file etc
        
        def run(self):
            self.outer.actions.write_to_timestamps_file(f"New Segment at {self.outer.timer.get_formatted_current_time()}")
            # `self.outer.actions` when I really just want to write `actions`. I also notice that classes and files are redundant abstractions. I'm using classes because they provide ability for dependency injection
    
    def start_new_segment_action(self): # todo: `implements some type``
        self.actions.write_to_timestamps_file(f"New Segment at {self.timer.get_formatted_current_time()}")
    def test_action(self, info):
        self.actions.write_to_timestamps_file(f"{self.timer.get_formatted_current_time()} {info}")