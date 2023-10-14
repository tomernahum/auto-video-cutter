from plugins import PluginInterface, register_plugin
from utils import Timer 

def register_cut_action_plugin(interface:PluginInterface, config):
    timer = Timer()  # will probably to make this gettable from interface / shared
    
    def markEvent(name:str):
        interface.mark_current_timestamp(name)
        interface.print(f"{name} marked")
        # interface.mark_timestamp(interface.getCurrentTimeStamp())
    
    events = ["StartNewSegment", "RestartSegment", "RestartLastSegment"]
    for i in events:
        interface.on_event_triggered(i, lambda : markEvent(i))
    

    def edit_video(timestamps, editInterface, moviefile):
        pass
    interface.registerEditFunction(edit_video, events)

register_plugin(register_cut_action_plugin)
    
    