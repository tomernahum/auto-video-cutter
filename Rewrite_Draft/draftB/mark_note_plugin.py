
from plugins import PluginInterface, register_plugin
from utils import Timer 

# somewhat pseudocode due to interface not implementing any of these methods
def register_note_plugin(interface:PluginInterface):
    timer = Timer()  # will probably to make this gettable from interface / shared
    
    def action():
        timestamp = interface.getCurrentTimestamp()
        interface.pauseFlow()
        note = interface.requestUserInputPausingFlow("Enter Note")
        interface.unPauseFlow()
        interface.mark_timestamp(timestamp, note)
    interface.on_event_triggered("MarkNote", action)
    

    def edit_video(timestamps, editInterface, moviefile):
        for t in timestamps:
            editInterface.addHumanReadableTimestamp(t.timestamp, t.text)
    interface.registerEditFunction(edit_video, events)

register_plugin(register_note_plugin)
    
    