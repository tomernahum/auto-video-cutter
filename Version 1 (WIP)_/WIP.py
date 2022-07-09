

#hotkeys picker thing

from plugins_interface import PluginsInterface

active_plugin_names = ["test_plugin"]
PluginsInterface(active_plugin_names)

def get_default_hotkey_command_pairs(plugins:PluginsInterface, display):  #not neccessarily same display class used during recording
    plugins.get_default_commands_by_type()
    







