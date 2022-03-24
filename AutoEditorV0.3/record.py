#import hotkeys
#choose File Name
#open/create file for writting
#monitor for hotkeys & print + write to file when they are pressed
#also keep track of & print/write at end of file helpful info as user presses hotkeys:
#-segments done
#-projected edited video length

# todo eventually (maybe): Make this usable through website/localhost or whatever instead of terminal so it could be added to obs as a browser-dock
#      - would this entail replacing the print statements basically? Maybe even replacing keyboard shudder
# todo idea: should it count the projected length of the output video as you're going? Yes methinks - that could get complicated with retake a
#      - 
#bug/todo: Indent from \t between time and Accepted/Rejected/etc is too short (maybe)
#bug: pressing hotkeys in another program does activate but also can make error sound or trigger that program's hotkeys

import datetime
import time
import keyboard

#Q/N: global vars are apparently bad form but I don't think I can pass / return it (there could be a way actually)with the keyboard module I'm using... So I will put the global statement at the top so you know what modifies it... | I've also been head someone say that if your function requires a lot of inputs it's not doing one thing well enough? Well where should those inputs go the main code?
segments_done = 0
edited_vid_length_projections_history_queue = [0] #could be replaced with deque todo decide
#^last item is the most recent one (for printing), other items are history (need it when retake a ing)
last_cut_timestamp = "0"

#Main code that is called on from main.py
def start_record_timestamps_mode():
    global segments_done
    segments_done = 0

    hotkeys_dict = get_hotkeys_dict()
    settings_dict = get_settings_dict()
    output_file = open(ask_for_output_file_name(),"w+")
    
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

    
    #Tell the user a quick info summary 
    if settings_dict["Quick >>>Info after starting (yes/no)"] == "yes":
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
    
    mark_cut("end", start_time, output_file, settings_dict)
    projected_final_time = edited_vid_length_projections_history_queue[-1]
    output_file.write(f"EOF segments done: {segments_done}, projected final time: {projected_final_time} \n")#write segments/projected time summary at bottom of file
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


# Is called from pressing hotkeys (and right at end) prints and writes to file timestamp & cut label + prints and tracks segments_done & edited_vid_length
def mark_cut(label, start_time, output_file, settings_dict):
    global segments_done 
    global edited_vid_length_projections_history_queue #very long name
    global last_cut_timestamp 
    #Q/N: I am checking the label 3 times to seperate the operations. Should I just do this once for efficiency or is this better for readability
    
    #todo put a settings-togglable guard against multiple retake-accepteds in a row

    time_elapsed = get_time_elapsed_str(start_time)
    """ q/n: (if the thing calling this were a normal piece of code) 
    # time_elapsed could be moved to the outside and just passed in 
    # (still found with same function), should it be generally?)"""
    #find past tense of label (eg "accept" -> "accepted")
    past_tense_label = find_past_tense_label(label)
    
    #modify segments done if needed
    if label == "accept": segments_done += 1
    elif label == "retake accepted": segments_done += -1

    #modify edited_vid_projections_list
    if label == "accept":
        change_in_projection = float(time_elapsed) - float(last_cut_timestamp)
        new_projection = edited_vid_length_projections_history_queue[-1] + change_in_projection
        
        edited_vid_length_projections_history_queue.append(new_projection)
        
        #keep the list/queue from getting too long based on retake accepted limit
        retake_limit = settings_dict["Retake Accepted Limit (0-99/no)"]
        if retake_limit != "no" and len(edited_vid_length_projections_history_queue) > int(retake_limit):
            del edited_vid_length_projections_history_queue[0]
    if label == "retake accepted":
        if len(edited_vid_length_projections_history_queue) > 1:  #todo may need to make sure the settings number isnt off by one
            edited_vid_length_projections_history_queue.pop() #now the most recent one is the previously second to last one
        else:
            print("too many retakes!")
            segments_done += 1 #this is temp I really got to go I will rework this
            return #exit out of program
            #may want to move this up to the top & out of this potential seperate function for better form. Whole thing needs to be cleaned up but i am out of time for today
    
    last_cut_timestamp = time_elapsed
    #build the to-print string based on settings & the to-write (in file) string #Q/N: does this really need to be a func?
    to_print_str = build_to_print_str(settings_dict, time_elapsed, past_tense_label, segments_done, edited_vid_length_projections_history_queue)
    to_write_str = time_elapsed + "\t" + past_tense_label + "\n"

    #perform the final outputs
    print(to_print_str)
    output_file.write(to_write_str)

def build_to_print_str(settings_dict, time_elapsed, past_tense_label, segments_done, edited_vid_length_projections_history_queue):
    to_print_str = ""
    to_print_str += time_elapsed
    to_print_str += "\t" + past_tense_label
    if settings_dict["Include completed segment count (long/short/no)"] == "short": 
        to_print_str += "\t" + str(segments_done) 
    elif settings_dict["Include completed segment count (long/short/no)"] == "long":
        to_print_str += "\t" + str(segments_done) + "todo: put the detail back in"
    if settings_dict["Include projected final vid length (yes/no)"] == "yes":    #todo: consider long/short
        projected_final_length = edited_vid_length_projections_history_queue[-1]
        to_print_str += "\t" + str(projected_final_length)
    return to_print_str

def find_past_tense_label(label):
    past_tense_label = ""
    if label == "accept": past_tense_label = "Accepted"
    elif label == "reject": past_tense_label = "Rejected"
    elif label == "retake accepted": past_tense_label = "Retake A."
    elif label == "end": past_tense_label = "Ended"
    return past_tense_label
    
    



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
    settings_dict = {"Include completed segment count (long/short/no)" : "short",
                    "Include projected final vid length (yes/no)": "yes", #WIP
                    "Retake Accepted Limit (0-99/no)" : "no",
                    "Quick >>>Info after starting (yes/no)" : "yes"}
    return settings_dict

def ask_for_output_file_name(): 
    output_file = input("enter the name of the file to write to (no extention): ")+".txt"
    return output_file

