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

#
import datetime
import os
import time
import keyboard

#Q/N: global vars are apparently bad form but I don't think I can pass / return it (there could be a way actually)with the keyboard module I'm using... So I will put the global statement at the top so you know what modifies it... | I've also been head someone say that if your function requires a lot of inputs it's not doing one thing well enough? Well where should those inputs go the main code?
segments_done = 0
projected_final_vid_length_history_queue = [0] #could be replaced with deque 
    #^last item is the most recent one (for printing), other items are history (need it when retake a. ing)
    #this is used for reverting the time after a retake a. is called. The length of this has to do with the setting max retakes
    #Q/N/todo: I feel like the implementation of this could stand to be a little clearer, 
last_cut_timestamp = "0"

#Main code that is called on from main.py
def start_record_timestamps_mode():
    global segments_done
    global projected_final_vid_length_history_queue #

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
    
    #todo: maybe add running time count
    
    #wait till stop hotkey is pressed (hotkeys are detected while waiting)
    keyboard.wait(hotkeys_dict["end recording"]) 
    
    #Finish up: mark ending cut, write info footer in file, and close file
    mark_cut("end", start_time, output_file, settings_dict)
    projected_final_vid_length = projected_final_vid_length_history_queue[-1]
    output_file.write(f"EOF segments done: {segments_done}, projected final time: {projected_final_vid_length} \n")#write segments/projected time summary at bottom of file
    output_file.close()
    print("File Saved. Goodbye")
    
    #todo "would you like to edit it now?"

#todo onhotkey then pass timestamp into mark_cut
def add_hotkey_detection(hotkeys_dict, start_time, output_file, settings_dict):
    #keyboard.add_hotkey(hotkeys_dict["accept"]) reject, 3rd
    
    for hotkey_function_label, literal_hotkey_str in hotkeys_dict.items():
        if  hotkey_function_label in {"start recording","end recording"}: continue  #is this inneficient?
        
        if hotkey_function_label in {"accept","reject","retake accepted"}:
            keyboard.add_hotkey(literal_hotkey_str, mark_cut, args=[hotkey_function_label, start_time, output_file, settings_dict])
            # makes it so that if you press the hotkey while code is running
            # it runs the function mark_cut w/ the label as an input
        else:
            keyboard.add_hotkey(literal_hotkey_str, print, args=["temp - pressed ", literal_hotkey_str])
            #this will be custom effects markers&doers hotkeys



# Is called from pressing hotkeys (and right at end) prints and writes to file timestamp & cut label + prints and tracks segments_done & edited_vid_length
def mark_cut(label, start_time, output_file, settings_dict):
    global segments_done 
    global projected_final_vid_length_history_queue #very long name
    global last_cut_timestamp 
    #Q/N: I am checking the label 3 times to seperate the operations. Should I just do this once for efficiency or is this better for readability

    if label == "retake accepted" and len(projected_final_vid_length_history_queue) <= 1: 
        print("too many retakes!")
        return #abandon the cut

    cut_timestamp = get_time_elapsed_str(start_time)  # q/n: (if the thing calling this were a normal piece of code) time_elapsed could be moved to the outside and just passed in (still found with same function), should it be generally?)
    
    past_tense_label = find_past_tense_label(label)  #find past tense of label (eg "accept" -> "accepted")
    
    #modify segments done if needed
    if label == "accept": segments_done += 1
    elif label == "retake accepted": segments_done += -1

    #modify edited_vid_projections_list & get current projection
    projected_final_vid_length = modify_projected_final_vid_length_history_and_return_current(label, settings_dict, cut_timestamp)
    #these things could have a shorter name lol and possibly the modify & return in 1 func is bad form. Idk what to do though
    
    #write to file
    to_write_str = cut_timestamp + "\t" + past_tense_label + "\n"
    output_file.write(to_write_str) 
        
    #print the information
    to_print_str = build_to_print_str(settings_dict, cut_timestamp, past_tense_label, segments_done, projected_final_vid_length, label)
    print(to_print_str)


    last_cut_timestamp = cut_timestamp #needs to be done after modify projection

 




def modify_projected_final_vid_length_history_and_return_current(label, settings_dict, cut_timestamp):
    global projected_final_vid_length_history_queue
    if label == "accept":
        change_in_projection = float(cut_timestamp) - float(last_cut_timestamp)
        new_projection = projected_final_vid_length_history_queue[-1] + change_in_projection
        projected_final_vid_length_history_queue.append(new_projection)
        
        #keep the list/queue from getting too long based on retake accepted limit #may not be neccisary
        retake_limit = settings_dict["Retake Accepted Limit (0-99/no)"]
        if retake_limit != "no" and len(projected_final_vid_length_history_queue) > int(retake_limit):
            del projected_final_vid_length_history_queue[0]
        #retake limit,
    elif label == "retake accepted":
        projected_final_vid_length_history_queue.pop() #now the most recent one is the previously second to last one
        #this can't run out of things to pop since we check for that at top of function
    
    return projected_final_vid_length_history_queue[-1]

def build_to_print_str(settings_dict, time_elapsed, past_tense_label, segments_done, projected_final_vid_length, label):
    #todo: better system of structuring outputs than \t 

    to_print_str = ""
    to_print_str += time_elapsed
    
    to_print_str += "\t" + past_tense_label
    
    if settings_dict["Include completed segment count (long/short/no)"] == "short": 
        to_print_str += "\t" + str(segments_done) 
    elif settings_dict["Include completed segment count (long/short/no)"] == "long":
        if label == "accept": 
            to_print_str += "\t%3d segments accepted, now recording #%2d" % (segments_done,segments_done+1)
        elif label == "reject":
            to_print_str += "\t re-recording segment #%2d               " % (segments_done+1) # so \t will line up the same
        elif label == "retake accepted": 
            to_print_str += "\t re-recording previously accepted segment #%2d" % (segments_done+1) #rerecording -the- previously...
        elif label == "end":
            to_print_str += "\t>total accepted segments: %2d             " % (segments_done)
    
    if settings_dict["Include projected final vid length (long/short/no)"] == "short":    #todo: consider long/short
        to_print_str += "\t" + truncate_number_str(projected_final_vid_length, 2)
    elif settings_dict["Include projected final vid length (long/short/no)"] == "long":
        to_print_str += "\t Edited Vid Time: " + truncate_number_str(projected_final_vid_length, 2) #todo possibly rework name
    
    return to_print_str

def find_past_tense_label(label):
    #todo pretty sure this should be switch case Edit: match case and apparently my python is too old for it?
    past_tense_label = ""

    if label == "accept": past_tense_label = "Accepted"
    elif label == "reject": past_tense_label = "Rejected"
    elif label == "retake accepted": past_tense_label = "Retake A."
    elif label == "end": past_tense_label = "Ended   "
    return past_tense_label
    
    



def get_time_elapsed_str(start_time):
    time_elapsed = time.time() - start_time
    return truncate_number_str(time_elapsed,2)

def truncate_number_str(number, digits_after_decimal):
    multiplier = 10 ** digits_after_decimal # to the power of
    num = float(number) #just in case
    truncated_num = int(num * multiplier)  /  multiplier  #eg x = 25.54321: x=(x*100)=2554.321| x=(int(x)) = 2554| x = x/100 = 25.54
    
    #make the decimals place have the appropriate number of digits if it has less (might be a better way to do this)
    semifinal_string = str(truncated_num)
    while len(semifinal_string.split(".")[1]) < digits_after_decimal:
        semifinal_string += "0"

    return semifinal_string
    
    
def get_hotkeys_dict():
    return {"start recording":"ctrl+shift+\\", "end recording":"ctrl+shift+\\",
            "accept":"alt+q", "reject":"alt+w", "retake accepted":"alt+e",
            "test-effect":"alt+z"}
    #todo: Settings file with hotkeys customization + infinite custom name effect hotkeys

def get_settings_dict():
    #In file will be under Record Mode Settings
    settings_dict = {"Include completed segment count (long/short/no)" : "long",
                    "Include projected final vid length (long/short/no)" : "long",
                    "Projected final vid length display (s, m/s)" : "m/s",
                    "Retake Accepted Limit (0-99/no)" : "no",
                    "Quick >>>Info after starting (yes/no)" : "yes"}
    return settings_dict
    # Settings notes:
    # - need a setting for seconds/minutes:seconds
    # - may replace this 

def ask_for_output_file_name(): 
    user_input = input("enter the name of the file to write to (no extention): ")
    file_name = user_input + ".txt"
    folder_name = "Timestamp Files"
    
    #go into subfolder - semi broken
    fileDir = os.path.dirname(os.path.realpath('__file__'))     
    tmp = folder_name+'/'+ file_name
    file_path = os.path.join(fileDir, tmp) #this does n
    
    #return file_path  #only works if you are already in the same directory as the python file: not if you click the play button in VSCode
    return file_name


if __name__ == '__main__':
    start_record_timestamps_mode()