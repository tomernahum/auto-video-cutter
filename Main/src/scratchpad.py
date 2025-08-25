
from pynput import keyboard

def on_press(key):
    if hasattr(key, 'char') and key.char == 'a':
        print("hello")
        # return False # stop listening

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
