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


    def get_actions(self):
        return [self.StartNewSegment(self)]

    # might change this
    class StartNewSegment(Action):
        def __init__(self, outer:CutActions):
            self.outer = outer

        name = "StartNewSegment" #name used for config file etc
        
        def run(self):
            self.outer.actions.write_to_timestamps_file(f"New Segment at {self.outer.timer.get_formatted_current_time}")