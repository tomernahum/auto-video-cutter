#import hotkeys
#choose File Name
#open/create file for writting
#monitor for hotkeys & print + write to file when they are pressed
#also print helpful info as user presses hotkeys

# todo eventually (maybe): Make this usable through website/localhost or whatever instead of terminal so it could be added to obs as a browser-dock
#      - would this entail replacing the print statements basically? Maybe even replacing keyboard shudder
# todo idea: should it count the projected length of the output video as you're going? Yes methinks - that could get complicated with retake a
#      - 
#bug/todo: Indent from \t between time and Accepted/Rejected/etc is too short (maybe)
#bug: pressing hotkeys in another program does activate but also can make error sound or trigger that program's hotkeys

import datetime
import time
from urllib.parse import parse_qs
import keyboard


segments_done = 0 #Q/N: this is apparently bad form but I don't think I can pass / return it (there could be a way actually)with the keyboard module I'm using... So I will put the global statement at the top so you know what modifies it...
edited_vid_length = 0 #post-cuts_vid_length, final_vid_length, projected_final_length



#Main code that is called on from main.py
def start_record_timestamps_mode():
    global segments_done
    segments_done = 0

    hotkeys_dict = get_hotkeys_dict()
    settings_dict = get_settings_dict()
    output_file = open(ask_for_output_file_name(),"w")
    
    #write file header
    file_header = "Timestamps file for [autoeditor program] recorded on " + str(datetime.datetime.now())
    output_file.write(file_header + "\n")

    
    #tell user the hotkey, wait till it is pressed then mark the start_time
    start_hotkey = hotkeys_dict["start recording"]
    end_hotkey = hotkeys_dict["end recording"]
    print(f"Press [{start_hotkey}] to start recording...   ([{end_hotkey}] to end)")
    keyboard.wait(start_hotkey) #wait until start key pressed
    start_time = time.time()
    #print("Started")  #should whole segment be turned into a function somehow?

    
    #Tell the user what's what (might remove)
    reject_key = hotkeys_dict["reject"]
    accept_key = hotkeys_dict["accept"]
    print(f">>> Info:   press [{reject_key}] if you mess up to rerecord from the last time you pressed [{accept_key}] or started"
    + f". Press [{accept_key}] to save")
    print("Started")

    #add hotkeys with keyboard module
    add_hotkey_detection(hotkeys_dict, start_time, output_file, settings_dict)
    #each hotkey executes a function basically, (those being mark_cut() and WIPmark_effect())
    
    #wait till stop hotkey is pressed
    keyboard.wait(hotkeys_dict["end recording"]) 
    
    mark_cut("end", start_time, output_file)
    output_file.close()
    print("File Saved. Goodbye")
    
    #maybe todo "would you like to edit it now?"

def add_hotkey_detection(hotkeys_dict, start_time, output_file, settings_dict):
    #keyboard.add_hotkey(hotkeys_dict["accept"]) reject, 3rd
    
    for hotkey_function_label, literal_hotkey_str in hotkeys_dict.items():
        if  hotkey_function_label in {"start recording","end recording"}: continue  #is this inneficient?
        
        if hotkey_function_label in {"accept","reject","retake accepted"}:
            keyboard.add_hotkey(literal_hotkey_str, mark_cut, args=[hotkey_function_label, start_time, output_file, settings_dict])
            # makes it so that if you press the hotkey while code is running
            # it runs the function mark_cut w/ the label as an input
        else:
            keyboard.add_hotkey(literal_hotkey_str, print, args=["temp"])
            #this will be custom effects markers&doers hotkeys

#prints and writes to file timestamp & cut label + prints and tracks segments_done & edited_vid_length
def mark_cut(label, start_time, output_file, settings_dict):
    global segments_done

    time_elapsed = get_time_elapsed_str(start_time)
    """ q/n: (if the thing calling this were a normal piece of code) 
    # time_elapsed could be moved to the outside and just passed in 
    # (still found with same function), should it be generally?)"""
    
    #Determine past_tense_label and modify segments_done and edited_vid_length
    #past_tense_label, segments_done_change = find_some_stuff(label)

    past_tense_label = ""
    segments_done = segments_done  #very important line of code  # could change to segments_done_change and add outside of loop
    if label == "accept": 
        past_tense_label += "Accepted"
        segments_done += 1
    elif label == "reject": 
        past_tense_label += "Rejected"
        #segments_done += 0
    elif label == "retake accepted": 
        past_tense_label += "Retake A."
        segments_done += -1
    elif label == "end": 
        past_tense_label += "Ended"
        #segments_done += 0
    
    #build the to-print string based on settings
    to_print_str = ""
    to_print_str += time_elapsed
    to_print_str += "\t" + past_tense_label
    if settings_dict["Include completed segment count (yes/no)"] == "yes": 
        to_print_str += "\t" + segments_done
    if settings_dict["Include projected final time (yes/no)"] == "yes":
        pass #WIP
    
    #build the to-write (in file) string
    to_write_str = time_elapsed + "\t" + past_tense_label + "\n"

    #perform the final outputs
    print(to_print_str)
    output_file.write(to_write_str)
    
    
    


def get_time_elapsed_str(start_time):
    time_elapsed = time.time() - start_time
    truncated_time_elapsed = int(time_elapsed * 100) / 100
    
    #make the decimals place have 2 digits if it has 1 (might be a better way to do this)
    semifinal_string = str(truncated_time_elapsed)
    if len(semifinal_string.split(".")[1]) <2:
        semifinal_string += "0"

    return str(semifinal_string)
    
    
def get_hotkeys_dict():
    return {"start recording":"ctrl+shift+\\", "end recording":"ctrl+shift+\\",
            "accept":"alt+q", "reject":"alt+w", "retake accepted":"alt+e",
            "test-effect":"alt+z"}
    #Todo: Settings file with hotkeys customization + infinite custom name effect hotkeys

def get_settings_dict():
    #In file will be under Record Mode Settings
    settings_dict = {"Include completed segment count (yes/no)" : "yes",
                    "Include projected final time (yes/no)":"no", #WIP
                    "Retake Accepted Limit (1/2/no)" : "no"}
    return settings_dict

def ask_for_output_file_name(): 
    output_file = input("enter the name of the file to write to (no extention): ")+".txt"
    return output_file

