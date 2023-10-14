# Using an interface object and callbacks instead of inheriting from class
# Kind of JavaScript style / """Functional""". In honesty I think "functional" is better cause it's slightly less concepts, more accessable peraps. but maybe it's less idiomatic or maybe it only seems that way

from utils import Timer
from plugins import PluginInterface, register_plugin

timer = Timer()


def register_example_plugin(interface:PluginInterface):
    def do_action():
        interface.write_to_file("Hello")


    
    interface.on_start(lambda : timer.start_timer())

    interface.on_event_triggered("myEvent", do_action)
    interface.on_event_triggered("myEvent", lambda: print("Hello2"))

    interface.on_event_triggered("printTime", lambda: print(f"{timer.get_formatted_current_time()} Hi"))

    #maybe
    cut_actions = interface.request_module_reference("cut_actions")
    effects = interface.request_module_reference("effects")
    getTime = lambda: (cut_actions.get_cut_timer() + effects.get_total_added_time())
    interface.on_display_update(lambda: getTime().format())


    # editing part
    def edit_video(timestamps, editInterface, moviefile):

        for i in timestamps:
            editInterface.cutTimeRange(i, i+10)
            moviefile.cut(i, i+10)

        return moviefile
        """
            editInterface:
                cutTimeRange
                InsertTimeRange
                ReplaceTimeRange (with timerange of different length)
                
                could all be last one


            this is necessary to keep the timestamps in sync for other plugins (instead of write to file we will have add_timestamp_mark_in_file)
            still a draft

            what timestamps this file will see will either be ones the same plugin created, or ones it is interested in (by slug/nameId), im yet to decide
        """
    events_im_interested_in = ["myEvent", "printTime"]
    interface.registerEditFunction(edit_video, events_im_interested_in)

    pass


# only thing required from plugin writer. Hopefully typing will work 
# will probably replace this with a callable function interface not just whenever file is loaded and a global main list lol
register_plugin(register_example_plugin)