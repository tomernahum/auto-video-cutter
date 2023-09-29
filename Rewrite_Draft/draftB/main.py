
import time



from plugins import main_loop
# Register Plugins
from example_plugin import register_example_plugin
from cut_actions_plugin import register_cut_action_plugin
# ^ this will be standardized differently. right now it registers them as it loads the file (or inits the module if we kept this into production version)


main_loop.startRecordMode()

main_loop.triggerEvent("myEvent")
main_loop.triggerEvent("nooneslistening")

main_loop.triggerEvent("printTime")
time.sleep(1.5)
main_loop.triggerEvent("printTime")

time.sleep(1.5)
main_loop.triggerEvent("printTime")

# obviously irl to be triggered by shortcuts