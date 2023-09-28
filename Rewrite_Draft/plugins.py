

# todo: make abstract class, can implement whichever elements it wants (callbacks)
# look into abstract class vs interface etc

class Plugin():
    def on_start():
        pass
    def on_pause():
        pass
    # etc, callbacks

"""
    I am inspired by HTML & JS elements

    We need callbacks for what happens in the main process 
    (for instance: onKeyPress/onActionCalled, onStart) 

    and also ways to call the main process to do something 
    (for instance: write_note_to_file, display_message_to_user)

    for callbacks we could
    - implement abstract plugin class and have our main loop call the appropriate callbacks of all plugins when they happen (forget what this pattern is called but I've seen it)

    for calling we could
    - (less sure)
    - implement the funcitonality in the plugin class? and call self.do_this,  no bad
    - make an interface class that Plugins are initialised with that they can call
        - I think this is good


    for registering an action function:
        - can implement register_action() function in plugin->main interface
        - can implement get_actions() functions in main->plugin interface
        - action format:
            - Name, Callback function
            - or Name, action class that implements run function

"""


class PluginsToMainInterface():
    def write_to_timestamps_file(line:str):
        # write to timestamps file with the plugin name as a prefix
        # might change it to have stricter formating idk
        pass


class Action():
    # todo: abstract function/class
    def run():
        pass