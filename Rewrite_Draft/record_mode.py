import time


from cut_actions import CutActions
from plugins import PluginsToMainInterface

def main():
    plugin_to_main_interface = PluginsToMainInterface()
    plugin = CutActions(plugin_to_main_interface)
    plugin.on_start()

    #V A
    actions = plugin.get_actions_1()
    actions[0].run()

    #V B
    actions2 = plugin.get_actions_2()
    actions2["StartNewSegment"]() 
    actions2["TestAction"] ("Hello!!")

    print("done")
    pass

main()