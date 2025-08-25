
"""
IDK how I would do this if I was starting over, but I just want to add 
config file to my existing messy code
"""

from record import CutAction, Accept, Reject, RetakeAccepted


class Config:  # to be used as a dataclass and just modified raw by the config file parser

    # control hotkeys
    pause_hotkey = "alt+p"
    start_hotkey = "ctrl+shift+\\"
    end_hotkey = "ctrl+shift+\\"

    # cutaction hotkeys
    cut_action_hotkeys_to_data_obj = {  # actually not ideal format for changing
        "alt+q": Accept(),
        "alt+w": Reject(),
        "alt+e": RetakeAccepted(),
    }

    def lookup_cut_action_hotkey(self, hotkey):
        if hotkey in self.cut_action_hotkeys_to_data_obj:
            return self.cut_action_hotkeys_to_data_obj[hotkey]
        # elif hotkey in self.effect_action_hotkeys_to_data_obj:
        raise ValueError()

    def get_list_of_hotkeys(self):
        list_of_hotkeys = []

        list_of_hotkeys.append(self.pause_hotkey)
        list_of_hotkeys.append(self.end_hotkey)
        # list_of_hotkeys.append(self.start_hotkey)

        for i, _ in self.cut_action_hotkeys_to_data_obj.items():
            list_of_hotkeys.append(i)
        # for i, _ in self.effect_action_hotkeys_to_data_obj.items():
        #    list_of_hotkeys.append(i)

        return list_of_hotkeys


def get_record_mode_config(system="from file") -> Config: #main1
    config = Config()

    if system == "from file":
        import json
        with open("config.json", 'r') as file:
            config_map = json.load(file)
        
        # control hotkeys
        config.start_hotkey = config_map["Start Hotkey"]
        config.end_hotkey = config_map["End Hotkey"]
        config.pause_hotkey = config_map["Pause Hotkey"]

        # cutaction hotkeys
        config.cut_action_hotkeys_to_data_obj = {
            config_map["Accept Hotkey"]: Accept(),
            config_map["Reject Hotkey"]: Reject(),
            config_map["Retake Accepted Hotkey"]: RetakeAccepted(),
        }

        return config
        #if i did this again I might just have it be one dictionary instead of config objecthaha
    
    elif system == "default" or system == "qwe":
        # control hotkeys
        config.start_hotkey = "ctrl+shift+\\"
        config.end_hotkey = "ctrl+shift+\\"
        config.pause_hotkey = "alt+p"

        # cutaction hotkeys
        config.cut_action_hotkeys_to_data_obj = {
            "alt+q": Accept(),
            "alt+w": Reject(),
            "alt+e": RetakeAccepted(),
        }

    elif system == "alternate":
        # control hotkeys
        config.start_hotkey = "ctrl+shift+\\"
        config.end_hotkey = "ctrl+shift+\\"
        config.pause_hotkey = "alt+p"

        # cutaction hotkeys
        config.cut_action_hotkeys_to_data_obj = {
            "alt+1": Accept(),
            "alt+2": Reject(),
            "alt+3": RetakeAccepted(),
        }

    elif system == "alternate2":
        # control hotkeys
        config.start_hotkey = "ctrl+shift+\\"
        config.end_hotkey = "ctrl+shift+\\"
        config.pause_hotkey = "alt+p"

        # cutaction hotkeys
        config.cut_action_hotkeys_to_data_obj = {
            "alt+z": Accept(),
            "alt+x": Reject(),
            "alt+c": RetakeAccepted(),
        }

    elif system == "game":
        # control hotkeys
        config.start_hotkey = "ctrl+shift+\\"
        config.end_hotkey = "ctrl+shift+\\"
        config.pause_hotkey = "alt+p"

        # cutaction hotkeys
        config.cut_action_hotkeys_to_data_obj = {
            "`": Accept(),  # need to test
            "r": Reject(),
            "shift+r": RetakeAccepted(),
        }

    return config

#to be used by mode 3 config mode
def reset_config_file_to_default():
    pass

def set_hotkey_in_config_file(name, new_hotkey):
    pass


def run_config_mode():  #main
    import keyboard

    print("To config, modify the config.json file")

    print("Type a hotkey now to see its name (then you can write it in the config file manually for now).") 
    print(keyboard.read_hotkey())
    
