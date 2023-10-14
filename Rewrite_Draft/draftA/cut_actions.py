from plugins import Action, Plugin, PluginsToMainInterface
from utils import Timer

# Written as a 



class CutActions(Plugin):
    timer = Timer() # should this be done in main loop and then actions are called w current time?   
    #^ also todo: ms support etc/=

    def __init__(self, actions:PluginsToMainInterface):
        #self.segmentTimer = Timer()
        self.actions = actions
        pass
    
    def on_start(self):
        self.timer.start_timer()


    def get_actions(self):
        def test_2(info):
            self.actions.write_to_timestamps_file(f"{self.timer.get_formatted_current_time()} {info}")

        return {
            "StartNewSegment": self.start_new_segment_action,
            "TestAction": self.test_action,
            "Test2": test_2
        }

    # or 
    # def on_action(actionName):
    #   if actionName == this: start_new_segment()
    # that would be more consistant I think 

    def start_new_segment_action(self): # todo: `implements some type``
        self.actions.write_to_timestamps_file(f"New Segment at {self.timer.get_formatted_current_time()}")
    def test_action(self, info):
        self.actions.write_to_timestamps_file(f"{self.timer.get_formatted_current_time()} {info}")
