#what we need is a EffectData class
#effect packs will import that and make classes that extend it for each effect 
# (like the cut/effectactions in record mode)
#EffectData will have info about displayin


def print_hello_world():
    print("Hello World")



functions = {"print_hello_world": print_hello_world}


class Effect:
    def __init__(self) -> None:
        self.name = "print_hello_world"
        self.function = print_hello_world
        self.default_hotkey = "alt+0"

        self.name_for_UD = "HW" #need getter
        self.name_for_record_mode = "Hello World" #nee

    def get_name_for_UD(self):
        return "HW"
    
    def get_updating_display_text(self):
        output = "[[name]]:[[time]]"#str(self.display_blurb)
        output = output.replace("[[name]]", str(self.get_name_for_UD()))
        output = output.replace("[[time]]", str(self.get_formatted_running_time()))
        return output

    def get_record_mode_display_list(self):
        
        
        
        pass