#import hotkeys
#choose File Name
#open/create file for writting
#monitor for hotkeys & print + write to file when they are pressed

#todo eventually: Make this usable through website/localhost or whatever instead of terminal so it could be added to obs as a browser-dock

import datetime
import time
import keyboard

segments_done = 0 #Q/N: this is apparently bad form but I don't think I can pass / return it (there could be a way actually)with the keyboard module I'm using... So I will put the global statement at the top so you know what modifies it...

#Main code that is called on from main.py
def start_record_timestamps_mode():
    global segments_done
    segments_done = 0

    hotkeys_dict = get_hotkeys_dict()
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
    add_hotkey_detection(hotkeys_dict, start_time, output_file)
    #each hotkey executes a function basically, (those being mark_cut() and WIPmark_effect())
    
    #wait till stop hotkey is pressed
    keyboard.wait(hotkeys_dict["end recording"]) 
    
    mark_cut("end", start_time, output_file)
    output_file.close()
    print("File Saved. Goodbye")
    
    #maybe todo "would you like to edit it now?"

def add_hotkey_detection(hotkeys_dict, start_time, output_file):
    #keyboard.add_hotkey(hotkeys_dict["accept"]) reject, 3rd
    
    for hotkey_function_label, literal_hotkey_str in hotkeys_dict.items():
        if  hotkey_function_label in {"start recording","end recording"}: continue  #is this inneficient?
        
        if hotkey_function_label in {"accept","reject","retake accepted"}:
            keyboard.add_hotkey(literal_hotkey_str, mark_cut, args=[hotkey_function_label, start_time, output_file])
            # makes it so that if you press the hotkey while code is running
            # it runs the function mark_cut w/ the label as an input
        else:
            keyboard.add_hotkey(literal_hotkey_str, print, args=["temp"])
            #this will be custom effects markers&doers hotkeys


def mark_cut(label, start_time, output_file):
    #prints and write to file cut + prints and tracks segments_done
    global segments_done

    time_elapsed = get_time_elapsed_str(start_time)
    """ q/n: (if the thing calling this were a normal piece of code) 
    # time_elapsed could be moved to the outside and just passed in 
    # (still found with same function), should it be generally?)"""
    
    #should this be split into 3 functions? They all essentially do the same thing
    if label == "accept":
        segments_done += 1
        print(time_elapsed + "\tAccepted" 
            + "\t%2d segments accepted, now recording #%2d" % (segments_done, segments_done+1))
        output_file.write(time_elapsed + "\tAccepted\n")
    
    elif label == "reject":
        #segments_done += 0
        print(time_elapsed + "\tRejected" 
            + "\tre-recording segment #%2d" % (segments_done+1))
        output_file.write(time_elapsed + "\tRejected\n")
    
    elif label == "retake accepted":
        segments_done += -1
        print(time_elapsed + "\tRetake A." 
            + "\tre-recording the previously accepted segment #%2d" % (segments_done+1))
        output_file.write(time_elapsed + "\tRetake A.\n")

    elif label == "end": #called from after keyboard.wait not from keyboard.addhotkey
        print(time_elapsed + "\tEnded    " 
            + "\tEnding Segment Auto-Discarded, %2d segments accepted in total," % segments_done)
        output_file.write(time_elapsed + "\tEnded\n")
    
    # this should:
    # - have the timestamp (time elapsed)
    # - update "segments done" 
    # - write to file
    # - print to terminal


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

def ask_for_output_file_name(): 
    output_file = input("enter the name of the file to write to (no extention): ")+".txt"
    return output_file

