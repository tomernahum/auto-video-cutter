"""
Things we want:
- Segments accepted count
- Vid runtime accepted count
- How long we've been recording time
- Pause Recording

- Continuos Running update count on time & accepted_vid_time

- Hotkey Detection
- Print the above things we are keeping track of when hotkey is pressed
- Write timestamp & effect or cutaction into output file (w/ header & footer)

- Key Actions:
- Start / Stop  Recording (1 end cutaction upon stoping)
- Pause Recording
- Accept, Reject, Retake Accepted
- Start/Stop Effect
- Single Timestamp Effect
"""
#bug: it'd be nice if it didn't flash when printing
#todo next: figure out paused (it's not done!) (make it stop the counting)



import time
import keyboard


#main
def start_record_mode():
    output_file_name = get_output_file_name()
    output_file = open(output_file_name, "w")
    
    #wait for start key & start recording
    start_hotkey = "ctrl+shift+\\"
    print(f"press [{start_hotkey}] to start recording")
    #keyboard.wait(start_hotkey)
    start_time = time.time()

    #add hotkeys
    hotkey_list = ["alt+q","alt+w","alt+p"]
    for hotkey in hotkey_list:
        keyboard.add_hotkey(hotkey, on_hotkey_press, args=[hotkey, start_time])
    

    #run continuous display (todo: make its own function)
    global ended  #will be called on from hotkey function
    global paused
    ended = False
    paused = False
    while True:
        current_time = str(time.time() - start_time)
        to_print = "Time Elapsed: "
        to_print += truncate_number_str(current_time) 
        to_print += "\tTime Accepted: " + truncate_number_str(current_time) + str(paused) + str(ended)
        print("\r" + to_print, end="")
        
        if ended is True: 
            break
        while paused == True:
            pass #stall
        time.sleep(0.0001)
    
    #finish up
    print("Wow!")
    output_file.close()


def print_over_updating_display(string_to_print, min_len=70):
    def replace_tabs_w_spaces(input_string, tabstop = 8):
        result = ""
        for c in input_string:
            if c == "\t": 
                while (len(result) % tabstop != 0): result += ' '
            else: result += c
        return result
    
    to_print = replace_tabs_w_spaces(str(string_to_print)) #otherwise it doesn't overide the updating timer display

    print_fill = " " * (min_len - len(to_print))
    print("\r" + str(to_print) + print_fill)
    
    return
    

def truncate_number_str(number, digits_after_decimal=2):
    multiplier = 10 ** digits_after_decimal # to the power of
    num = float(number) #just in case
    truncated_num = int(num * multiplier)  /  multiplier  #eg x = 25.54321: x=(x*100)=2554.321| x=(int(x)) = 2554| x = x/100 = 25.54
    
    #make the decimals place have the appropriate number of digits if it has less (might be a better way to do this)
    semifinal_string = str(truncated_num)
    while len(semifinal_string.split(".")[1]) < digits_after_decimal:
        semifinal_string += "0"

    return semifinal_string
    

def on_hotkey_press(hotkey, start_time):
    global paused

    #pause hotkey check
    if hotkey == "alt+p":
        #pause/unpause
        paused = not paused
        if paused: print_over_updating_display("Paused")
        else: print_over_updating_display("Unpaused")
        
        return
    
    #end hotkey check
    if hotkey == "ctrl+shift+\\":
        global ended
        ended = True
        return
    
    #don't run if recording is paused (pause key already checked for)
    if paused is True: 
        return 

    
    
    #run cut action
    if hotkey in {"alt+q", "alt+w", "alt+e"}:
        pass
    
    #effect
    else:
        pass
    
    to_print = ""
    to_print += truncate_number_str(time.time() - start_time)
    to_print += "\t"  #bug: \t does not overwrite updating display
    to_print += hotkey
    to_print += "\ttest"
    print_over_updating_display(to_print)




def get_output_file_name():
    return "1.txt" #for testing
    return input("enter the name of the file to write to (no extention): ") + ".txt"

if __name__ == "__main__":
    start_record_mode()