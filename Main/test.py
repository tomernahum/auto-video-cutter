import keyboard

import config
config.get_record_mode_config()




hotkey = keyboard.read_hotkey()
print(hotkey)


#keyboard.wait("space")