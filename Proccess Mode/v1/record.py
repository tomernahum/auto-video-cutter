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
Note: Global variables are apparently bad form but it seemed cleaner |: I guess that's a sign that
I'm not doing it right? Maybe it should be all in classes? I think this could also be a special case
as I am essentially running 2 scripts at once (check for hotkeys & update live timer) (seems to work fine as of now though)
"""
#bug: it'd be nice if it didn't flash when printing




from math import ceil
import time
import keyboard

#global vars: #may organize some into classes or something
global output_file
global start_time
global time_before_pause
global paused
global ended 
global segments_done



class CutAction:
    def __init__(self):
        pass

    def get_action_type(self): return self.action_type
    def get_past_tense_label(self): return self.past_tense_label
    def get_segments_done_change(self): return self.segments_done_change

    def get_segments_done_blurb(self, segments_done):
        output = self.segments_done_blurb_template
        output = output.replace("[[segments_done]]", str(segments_done))
        output = output.replace("[[segments_done_+1]]", str(segments_done + 1))
        return output

class Accept(CutAction):
    def __init__(self):
        self.action_type = "accept"
        self.past_tense_label = "Accepted"
        self.segments_done_change = +1 
        self.segments_done_blurb_template = "[[segments_done]] segments accepted, now recording #[[segments_done_+1]]"   

class Reject(CutAction):
    def __init__(self):
        self.action_type = "reject"
        self.past_tense_label = "Rejected"
        self.segments_done_change = 0 
        self.segments_done_blurb_template = "re-recording segment #[[segments_done_+1]]" 

class RetakeAccepted(CutAction):
    def __init__(self):
        self.action_type = "retake accepted"
        self.past_tense_label = "Retaking A."
        self.segments_done_change = -1
        self.segments_done_blurb_template = "re-recording previously accepted segment #[[segments_done_+1]]"

class End(CutAction):
    def __init__(self):
        self.action_type = "end"
        self.past_tense_label = "Ended   "
        self.segments_done_change = 0
        self.segments_done_blurb_template = "total segments accepted: [[segments_done]]"




#main
def start_record_mode():
    global start_time
    global segments_done
    global output_file
    
    output_file_name = get_output_file_name()
    output_file = open(output_file_name, "w")

    segments_done = 0
    
    #wait for start key & start recording
    start_hotkey = "ctrl+shift+\\"
    print(f"press [{start_hotkey}] to start recording")
    #keyboard.wait(start_hotkey)
    start_time = time.time()
    print("0.00    Started")

    
    #add hotkeys
    hotkey_list = ["alt+q","alt+w", "alt+e", "alt+p"]
    for hotkey in hotkey_list:
        keyboard.add_hotkey(hotkey, on_hotkey_press, args=[hotkey])
    

    #run continuous display until ended is set to true by on_hotkey_press function
    run_updating_display() #will run forever until ended = True
    
    #finish up
    print("Wow!")
    output_file.close()

def run_updating_display():
    global ended  #these are changed (or "broadcasted") in the on_hotkey_press function
    global paused
    global time_before_pause
    global start_time
    
    ended = False
    paused = False
    time_before_pause = 0
    
    if False: #toggle off running display - there will be a setting for this
        while not ended: time.sleep(0.1)
        return
    
    while True:
        if not paused:
            current_time = str(time.time() - start_time + time_before_pause) 
        else:
            current_time = time_before_pause

        to_print = ""
        to_print += "Time Elapsed: " + truncate_number_str(current_time) 
        if paused: to_print += "(P)"
        
        to_print += "\tTime Accepted TODO: " + truncate_number_str(current_time) + str(paused) + str(ended)
        
        to_print = replace_tabs_w_spaces(to_print)
        print("\r" + to_print, end="")
        
        if ended is True: 
            return
        
        time.sleep(0.001)



    

def on_hotkey_press(hotkey):
    global paused
    global start_time

    #pause hotkey check
    if hotkey == "alt+p":
        pause_or_unpause()
        return
    
    #end hotkey check
    if hotkey == "ctrl+shift+\\":
        global ended
        ended = True
        return
    
    #don't run if recording is paused (pause key already checked for)
    if paused is True: 
        return 


    current_time = get_current_time()
    
    #run cut action
    if hotkey == "alt+q":
        mark_cut_action(Accept(), current_time)
        return
    elif hotkey == "alt+w":
        mark_cut_action(Reject(), current_time)
        return
    elif hotkey == "alt+e":
        mark_cut_action(RetakeAccepted(), current_time)
        return
    
    #effect
    else:
        pass
    
    to_print = ""
    to_print += truncate_number_str(time.time() - start_time + time_before_pause)
    to_print += "\t"  #bug: \t does not overwrite updating display
    to_print += hotkey
    to_print += "\ttest"
    print_over_updating_display(to_print)

def pause_or_unpause():
    global paused
    global time_before_pause
    global start_time
    
    if paused is True: #unpause
        start_time = time.time()
        paused = False
        #print_over_updating_display("Unpaused")
        
        
    else:
        paused = True
        elapsed_time = time.time() - start_time
        time_before_pause += elapsed_time 
        start_time = None
        #print_over_updating_display("Paused")

def mark_cut_action(cut_action:CutAction, timestamp):
    #segments done
    #estimated total vid time
    #print: timestamp, past tense label, segments_done_blurb, total vid time left, 
    
    #timestamp = get_current_time()

    
    #update segments_done
    global segments_done 
    segments_done += cut_action.get_segments_done_change()
    #check for too many retakes
    if segments_done == -1 or (False):
        segments_done += 1
        print("To many retakes!")
        return

    #update estimated total vid time WIP

    #build to print string and to write string
    class StringBuilder:
        def __init__(self, initial_string=""):
            self.string = initial_string
        
        def get_string(self): return self.string
        
        def add(self, to_add):
            if self.string != "":
                self.string += "\t"
            self.string += str(to_add)
    
    to_print = StringBuilder("")
    to_print.add(timestamp)
    to_print.add( cut_action.get_past_tense_label() )
    if False: to_print.add(segments_done)
    if True: to_print.add(cut_action.get_segments_done_blurb(segments_done))

    to_write = StringBuilder("")
    to_write.add(timestamp)
    to_write.add(cut_action.get_past_tense_label())

    print_over_updating_display(to_print.get_string())
    output_file.write(to_write.get_string())
    

    



def print_over_updating_display(string_to_print:str, min_len=70):
    to_print = replace_tabs_w_spaces(str(string_to_print)) #otherwise it doesn't overide the updating timer display

    print_fill = " " * (min_len - len(to_print))
    print("\r" + str(to_print) + print_fill)
    
    return

def replace_tabs_w_spaces(input_string, tabstop = 8):
        def find_next_multiple(x, base):
            return base * ceil(x/base)
        
        result = ""
        split_string = input_string.split('\t')
        for section in split_string: 
            diff = find_next_multiple(len(section), tabstop) - len(section)
            if diff == 0: diff = tabstop
            result += section
            result += " " * diff
        return result

def get_current_time():
    global start_time
    global time_before_pause
    global paused
    
    if paused:
        current_time = time_before_pause
    else:
        current_time = time.time() - start_time + time_before_pause
    return truncate_number_str(current_time, 2)


def truncate_number_str(number, digits_after_decimal=2):
    multiplier = 10 ** digits_after_decimal # to the power of
    num = float(number) #just in case
    truncated_num = int(num * multiplier)  /  multiplier  #eg x = 25.54321: x=(x*100)=2554.321| x=(int(x)) = 2554| x = x/100 = 25.54
    
    #make the decimals place have the appropriate number of digits if it has less (might be a better way to do this)
    semifinal_string = str(truncated_num)
    while len(semifinal_string.split(".")[1]) < digits_after_decimal:
        semifinal_string += "0"

    return semifinal_string



def get_output_file_name():
    return "1.txt" #for testing
    return input("enter the name of the file to write to (no extention): ") + ".txt"


if __name__ == "__main__":
    start_record_mode()





#Considering using this 
#(to group the timer related functions and global vars, I wouldn't instansiate it... I guess maybe I could)
class Timer_not_in_use:
    start_time
    time_before_pause
    global paused
    
    @staticmethod
    def truncate_number_str():
        pass
    
    @staticmethod
    def convert_to_mins_format(secs_time):
        minutes, seconds = divmod(secs_time, 60) #returns division and remainder(modulus)

        return f"{minutes}m{seconds}s"
    
    @staticmethod
    def convert_to_h_m_s_format(secs_time):
        minutes, seconds = divmod(secs_time, 60)
        hours, minutes = divmod(minutes, 60)
        
        if hours == 0:
            return f"{minutes}m{seconds}"
        else:
            return f"{hours}h{minutes}m{seconds}s"


    @staticmethod
    def start_timer():
        Timer.start_time = time.time()
        Timer.time_before_pause = 0

    @staticmethod
    def pause_or_unpause():
        pass

    @staticmethod
    def get_time():
        if paused: current_time = time_before_pause
        else: current_time = time.time() - start_time + time_before_pause #time since pause + time before pause
        return current_time
    
    @staticmethod
    def get_formatted_time(format="hms", digits_after_decimal=None):
        current_time = Timer.get_time()
        
        current_time = Timer.truncate_number_str(current_time)

        if format == "hms":
            return Timer.convert_to_hms_format(current_time)
        elif format == "secs":
            return current_time

class Timer_also_not_yet_in_use:
    start_time #really time since last pause
    time_before_pause
    paused
    
    def __init__(self, start_time=time.time()):
        self.start_time = start_time
        self.time_before_pause = 0
        #self.paused = True

    def start_timer(self, start_time=time.time()):
        self.start_time = start_time
        self.time_before_pause = 0

    def get_current_time(self):
        if paused:
            current_time = time_before_pause
        else:
            current_time = (time.time() - start_time) + time_before_pause
        return truncate_number_str(current_time, 2)
    
    def get_formatted_time(self):
        return self.get_current_time()

    def is_paused(self): return paused
    
    def toggle_pause(self):
        if paused: #unpause
            self.start_time = time.time()
            self.paused = False
        
        else: #pause
            self.paused = True
            elapsed_time = time.time() - start_time
            time_before_pause += elapsed_time 
            start_time = None
            
    #add in functionality for estimated post-cut time (reject)




