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



import datetime
from math import ceil
import time
import keyboard

#global vars: #may organize some into classes or something
global output_file
global main_timer
global ended 
global printing_line
global segments_done
global active_effect_names

class Timer:
    start_time = None#really time since last pause
    time_before_pause = None
    paused = None
    
    def __init__(self):
        self.start_time = None
        self.time_before_pause = None
        self.paused = None
        pass

    def start_timer(self, start_time="now"): 
        if start_time == "now": self.start_time = time.time()
        else: self.start_time = start_time
        self.time_before_pause = 0
        self.paused = False

    def reset_timer(self, start_time="now"):
        self.start_timer(start_time)

    def get_current_time(self):
        if self.paused:
            current_time = self.time_before_pause
        else:
            current_time = (time.time() - self.start_time) + self.time_before_pause
        return Timer.trunc_time(current_time)
    
    def get_current_time_trunc(self):
        return Timer.trunc_time(self.get_current_time())

    def skip_ahead(self, secs): self.time_before_pause += secs


    def get_formatted_current_time(self):
        return Timer.convert_to_h_m_s_format(float(self.get_current_time_trunc()))
    
    @staticmethod
    def trunc_time(secs_time):
        return float(truncate_number_str(secs_time, digits_after_decimal=2))
    
    @staticmethod
    def convert_to_h_m_s_format(secs_time, shorten_seconds_above_1_min=False):
        secs_time = float(secs_time)
        minutes, seconds = divmod(secs_time, 60)
        hours, minutes = divmod(minutes, 60)
        
        minutes = int(minutes)
        hours = int(hours)
        seconds = truncate_number_str(seconds, 1)

        if minutes == 0 and hours == 0:
            return f"{seconds}s"
        
        if shorten_seconds_above_1_min is True:
            seconds = int(float(seconds))
        
        if hours == 0:
            return f"{minutes}m:{seconds}s"
        else:
            return f"{hours}h:{minutes}:m{seconds}s"
    
    
    def is_paused(self): return self.paused
    
    def toggle_pause(self):
        if self.is_paused(): #unpause
            self.start_time = time.time()
            self.paused = False
        
        else: #pause
            self.paused = True
            elapsed_time = time.time() - self.start_time
            self.time_before_pause += elapsed_time 
            self.start_time = None
            
    #add in functionality for estimated post-cut time (reject)

class CutTimer():
    #todo: look over cuttimer for any inconsistencies and consider making it inherent
    timer = Timer()  #Q/N this was easier to understand than a superclass, might actually be simple to change, this is basically just 3 variables
    accepted_segment_times_list = []
    #timer resets every segment, past timer counts are stored in list (kind of like start_time vs time_before_paused)

    def __init__(self):
        self.timer = Timer()
        self.accepted_segment_times_list = []

    def start_timer(self):
        self.timer.start_timer()      #we could inherit class timer and just let these things be infferred
    
    def toggle_pause(self):
        self.timer.toggle_pause()
    
    def is_paused(self): 
        return self.timer.is_paused()
    
    def get_running_time(self):
        running_time = self.timer.get_current_time_trunc()
        for i in self.accepted_segment_times_list: 
            running_time += i
        return running_time

    def cut_action(self, cut_action):  
        if isinstance(cut_action, Accept):
            self.accepted_segment_times_list.append(self.timer.get_current_time_trunc())
        elif isinstance(cut_action, RetakeAccepted):
           self.accepted_segment_times_list.pop()
        else: #reject or ended
            pass

        
        self.timer.reset_timer() #bug: doesnt seem to be working
        
    def get_formatted_current_time(self):
        #return "|timer: " + str(self.timer.get_formatted_current_time()) + " total: " + Timer.convert_to_h_m_s_format(self.get_running_time())
        
        return Timer.convert_to_h_m_s_format(self.get_running_time())

    
    

    pass





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
        self.segments_done_blurb_template = "[[segments_done]] segments accepted, now recording #[[segments_done_+1]]      "   

class Reject(CutAction):
    def __init__(self):
        self.action_type = "reject"
        self.past_tense_label = "Rejected"
        self.segments_done_change = 0 
        self.segments_done_blurb_template = "re-recording segment #[[segments_done_+1]]                    " 

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

class EffectAction:
    def __init__(self):
        self.effect_name = "Test Toggle Effect"
        self.name_for_printing = "ToggleEffect"
    def get_effect_name(self): return self.effect_name
    def get_name_for_printing(self): return self.name_for_printing

class Flip(EffectAction):
    def __init__(self):
        self.effect_name = "Flip"
        self.name_for_printing = "Flip"

class BlackWhite(EffectAction):
    def __init__(self):
        self.effect_name = "BlackWhite"
        self.name_for_printing = "Black/White"



def start_record_mode(): #main
    global main_timer
    global cut_timer
    global segments_done
    global output_file
    
    output_file_name = get_output_file_name()
    output_file = open(output_file_name, "w")
    
    file_header = "Timestamps file for [autoeditor program] recorded on " + str(datetime.datetime.now())
    output_file.write(file_header + "\n")

    main_timer = Timer()
    cut_timer = CutTimer()  #time elapsed that made it into final vid / isn't cut

    segments_done = 0
    
    #wait for start key & start recording
    start_hotkey = "ctrl+shift+\\"
    print(f"press [{start_hotkey}] to start recording")
    keyboard.wait(start_hotkey)
    main_timer.start_timer()
    cut_timer.start_timer()
    print("0.0s    Started") #todo: should replace this with a phony mark_cut

    
    #add hotkeys
    hotkey_list = ["alt+q","alt+w", "alt+e", "alt+p", "ctrl+shift+\\", "alt+1", "alt+2"] #todo: hotkeys added & defined in different places, not convienient for adding
    for hotkey in hotkey_list:
        keyboard.add_hotkey(hotkey, on_hotkey_press, args=[hotkey])
    

    #run continuous display until ended is set to true by on_hotkey_press function
    run_updating_display() #will run forever until ended = True
    
    #finish up
    mark_cut_action(End(), main_timer.get_current_time_trunc())
    footer = f"EOF. segments done: {segments_done}, projected final time: {None}"
    output_file.write(footer)
    output_file.close()

def run_updating_display():
    global ended  #these are changed (or "broadcasted") in the on_hotkey_press function
    global printing_line
    global main_timer
    global cut_timer
    
    ended = False
    printing_line = False
    
    
    if False: #toggle off running display - there will be a setting for this
        while not ended: time.sleep(0.1)
        return
    
    while True:
        current_time = main_timer.get_formatted_current_time()
        uncut_time = cut_timer.get_formatted_current_time()

        to_print = ""
        
        to_print += "Recording Time: " + current_time
        if main_timer.is_paused(): to_print += "(P)"
        else: to_print += "   " #so the tabing is the same
        
        to_print += "\tAccepted Time: "  + uncut_time
        
        
        #print the updating display
        if not printing_line: #if a line is not being printed rn (cause it might override)
            to_print = replace_tabs_w_spaces(to_print)
            print("\r" + to_print, end="")
        
        if ended is True: 
            return
        
        #for testing
        if False:
            act = float(main_timer.get_current_time_trunc())
            if  act > 5 and act < 6:
                main_timer.skip_ahead(50)
            elif act > 70 and act < 71:
                main_timer.skip_ahead(600)

        time.sleep(0.005)



    

def on_hotkey_press(hotkey):
    global main_timer

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
    if main_timer.is_paused() is True: 
        return 


    current_time = main_timer.get_current_time_trunc()
    
    #run cut action
    if hotkey == "alt+q":
        mark_cut_action(Accept(), main_timer)
        return
    elif hotkey == "alt+w":
        mark_cut_action(Reject(), main_timer)
        return
    elif hotkey == "alt+e":
        mark_cut_action(RetakeAccepted(), main_timer)
        return
    
    #effect
    elif hotkey == "alt+1":
        mark_effect_action(Flip(), main_timer)
    elif hotkey == "alt+2":
        mark_effect_action(BlackWhite(), main_timer)
    

def pause_or_unpause():
    global main_timer
    global cut_timer
    main_timer.toggle_pause()
    cut_timer.toggle_pause()
    #do anything else

def mark_cut_action(cut_action:CutAction, timer):
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
        print_over_updating_display("To many retakes!")
        return

    #update estimated total vid time
    global cut_timer
    cut_timer.cut_action(cut_action)

    #build to print and to write lists & print/write with mark_action
    to_write_list = [cut_action.get_past_tense_label()]
    
    to_print_list = []
    to_print_list.append(cut_action.get_past_tense_label())
    if True: to_print_list.append(cut_action.get_segments_done_blurb(segments_done))
    elif False: to_print_list.append(segments_done)
    if True: to_print_list.append("Edited Vid Time: " + cut_timer.get_formatted_current_time())
    elif False: to_print_list.append(cut_timer.get_formatted_current_time())

    print_and_write_action(timer, to_write_list, to_print_list)

   
active_effect_names = set() #would make this objects with timers in them if I wanted to display that elsewhere
def mark_effect_action(effect_action:EffectAction, timer):
    #keep track of if effect is on or off
    #write timestamp and effect_name in file
    #print timestamp effect name & wether the effect is on or off
        #todo * maybe: make a timer for each effect &/or show effect status on updating display
    
    effect_name = effect_action.get_effect_name()

    #keep track of whether the effect is on or off
    global active_effect_names  
    effect_was_active = effect_name in active_effect_names
    if effect_was_active: active_effect_names.remove(effect_name)
    else: active_effect_names.add(effect_name)
    effect_is_active = not effect_was_active


    #write & print (using mark_action)
    to_write_list = [effect_name]
    
    on_or_off = lambda : ["Off","On"][int(effect_is_active)]
    to_print_list = [f"Toggled {effect_action.get_name_for_printing()}",
                    on_or_off()]
    #todo: effect stutus & timer display (replace active effect names with effects objects w timers)
    
    print_and_write_action(timer, to_write_list, to_print_list)
    
    
def print_and_write_action(main_timer:Timer, write_list:list, print_list:list):
    global output_file
    #timestamp formatting
    #print
    #write

    #timestamp formatting
    timestamp_to_print = main_timer.get_formatted_current_time()
    timestamp_to_write = main_timer.get_current_time_trunc()

    #build print & write Strings
    to_print = str(timestamp_to_print)
    to_write = str(timestamp_to_write)
    for i in print_list:
        to_print += "\t" + str(i)
    for i in write_list: 
        to_write += "\t" + str(i)

    #write
    output_file.write(to_write + "\n")

    #print
    print_over_updating_display(to_print)


def print_over_updating_display(string_to_print:str, min_len=70): #could use a better name maybe
    global printing_line
    
    to_print = replace_tabs_w_spaces(str(string_to_print)) #otherwise it doesn't overide the updating timer display

    print_fill = " " * (min_len - len(to_print))
    
    printing_line = True   #fixes bug of occasional overwriting of this by updating display
    print("\r" + str(to_print) + print_fill)
    printing_line = False
    
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




def truncate_number_str(number, digits_after_decimal=2):
    multiplier = 10 ** digits_after_decimal # to the power of
    num = float(number) #just in case
    truncated_num = int(num * multiplier)  /  multiplier  #eg x = 25.54321: x=(x*100)=2554.321| x=(int(x)) = 2554| x = x/100 = 25.54
    
    #make the decimals place have the appropriate number of digits if it has less (might be a better way to do this)
    semifinal_string = str(truncated_num)
    while len(semifinal_string.split(".")[1]) < digits_after_decimal:
        semifinal_string += "0"

    return semifinal_string


class StringBuilder:
        def __init__(self, initial_string=""):
            self.string = str(initial_string)
        
        def get_string(self): return self.string
        
        def add(self, to_add):
            if self.string != "":
                self.string += "\t"
            self.string += str(to_add)


def get_output_file_name():
    return "1.txt" #for testing
    return input("enter the name of the file to write to (no extention): ") + ".txt"


if __name__ == "__main__":
    start_record_mode()












