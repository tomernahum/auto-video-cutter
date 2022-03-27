
import keyboard
import time

class CutAction:
    test = 0
    def __init__(self, timestamp):
        
        #self.timestamp = timestamp
        #self.action_type = action_type
        #self.past_tense_label = past_tense_label
        pass
    
    def get_original_timestamp(self):
        return self.timestamp

    def get_action_type(self):
        return self.action_type
    
    def get_past_tense_label(self):
        return self.past_tense_label
    
    def get_segments_done_change(self):
        return self.segments_done_change
    
    def get_segments_done_blurb(self, segments_done):
        output = self.segments_done_blurb_template
        output = output.replace("[[segments_done]]", str(segments_done))
        output = output.replace("[[segments_done_+1]]", str(segments_done + 1))
        return output

# we could make CutAction(action_type) if action_type=accept: set appropriate variabls
# or we could mak subclasses 

class AcceptCut(CutAction):
    def __init__(self, timestamp):
        self.timestamp = timestamp

        self.action_type = "accept"
        self.past_tense_label = "Accepted"
        self.segments_done_change = +1 
        self.segments_done_blurb_template = "[[segments_done]] segments accepted, now recording #[[segments_done_+1]]"     

class RejectCut(CutAction):
    def __init__(self, timestamp):
        self.timestamp = timestamp
        
        self.action_type = "reject"
        self.past_tense_label = "Rejected"
        self.segments_done_change = 0
        self.segments_done_blurb_template = "re-recording segment #[[segments_done_+1]]"

class RetakeAcceptedCut(CutAction):
    def __init__(self, timestamp):
        self.timestamp = timestamp
        
        self.action_type = "retake accepted"
        self.past_tense_label = "Retaking A."
        self.segments_done_change = -1
        self.segments_done_blurb_template = "re-recording previously accepted segment #[[segments_done_+1]]"

class EndCut(CutAction):
    def __init__(self, timestamp):
        self.timestamp = timestamp
        
        self.action_type = "end"
        self.past_tense_label = "Ended   "
        self.segments_done_change = 0
        self.segments_done_blurb_template = "total segments accepted: [[segments_done]]"


class Settings:
    #settings are static vars that can be accessed by eg Settings.start_hotkey

    option_var = "long"
    print_quick_starting_info = True #
    #tbdone
    
    start_hotkey = "ctrl+shift+\\"
    stop_hotkey = "ctrl+shift+\\"
    accept_hotkey = "alt+q"
    reject_hotkey = "alt+w"
    retake_accepted_hotkey = "alt+e"

    @classmethod
    def init_settings(cls):
        cls.option_var = "test"
        pass #will find user specified settings from file or whereva, for now just do manually above


def get_current_time():
    global START_TIME
    return truncate_number_str(time.time() - START_TIME, 2)
def truncate_number_str(number, digits_after_decimal):
    multiplier = 10 ** digits_after_decimal # to the power of
    num = float(number) #just in case
    truncated_num = int(num * multiplier)  /  multiplier  #eg x = 25.54321: x=(x*100)=2554.321| x=(int(x)) = 2554| x = x/100 = 25.54
    
    #make the decimals place have the appropriate number of digits if it has less (might be a better way to do this)
    semifinal_string = str(truncated_num)
    while len(semifinal_string.split(".")[1]) < digits_after_decimal:
        semifinal_string += "0"

    return semifinal_string


def on_cut_hotkey_pressed(action_type):
    timestamp = get_current_time() 
    
    cut_action = None
    if action_type == "accept": cut_action = AcceptCut(timestamp)
    elif action_type == "reject": cut_action = RejectCut(timestamp)
    elif action_type == "retake accepted": cut_action = RetakeAcceptedCut(timestamp)
    
    mark_cut_action(cut_action)

#nothing really changes in CutAction class and also this method could be part of it
def mark_cut_action(cut_action):
    global output_file
    global segments_done #I hear these are bad but I don't know how else to do it here. actually it could  be a class static variable if i moved this into cutaction - sam thing though right?
    #sadly vscode does not realize cut_action is a CutAction and doesn't autocomplete function names here
    
    #Update segments_done
    segments_done += cut_action.get_segments_done_change()
    #check for over-retakes
    if segments_done == -1 or False:
        segments_done += 1
        print("To many retakes!")
        return
    
    
    #build print and file write strings
    class ToPrintString:
        def __init__(self, initial_string):
            self.string = initial_string
        def __str__(self):
            return self.string
        
        def add(self, to_add):
            if self.string != "": self.string += "\t"  #could replace this with different system of tabeling
            self.string += str(to_add)
    
    to_print = ToPrintString("")
    to_print.add(cut_action.get_original_timestamp())
    to_print.add(cut_action.get_past_tense_label())
    
    if False: to_print.add(segments_done)
    elif True: to_print.add(cut_action.get_segments_done_blurb(segments_done))
    
    
    to_write = ToPrintString("") #misnomer
    to_write.add(cut_action.get_original_timestamp()) 
    to_write.add(cut_action.get_past_tense_label())
    
    #write to file and print
    output_file.write(str(to_write) + "\n")
    print(to_print)




def main():
    #wip
    Settings.init_settings() #settings are stored in settings class as static variables

    def ask_user_for_file():
        filename = input("Enter the name of the file pls (no prefix)") + ".txt"
        return open(filename, 'w')
    CutAction.output_file = ask_user_for_file()
    CutAction.segments_done = 0  #we keep track of accepted segments for printing to the user
    #...
    
    
    print(f"Press [{Settings.start_hotkey}] to start recording...   ([{Settings.stop_hotkey}] to end)")
    keyboard.wait(Settings.start_hotkey)
    CutAction.start_time = time.time()
    
    if Settings.print_quick_starting_info: 
        print(">>> Info:   to be put in")
    print("Started")

    keyboard.add_hotkey(Settings.accept_hotkey, on_cut_hotkey_pressed, ["accept"])
    keyboard.add_hotkey(Settings.reject_hotkey, on_cut_hotkey_pressed, ["reject"])
    keyboard.add_hotkey(Settings.retake_accepted_hotkey, on_cut_hotkey_pressed, ["retake accepted"])
    
    keyboard.wait(Settings.stop_hotkey)
    
    #mark_cut_action( EndCut(get_current_time()) )
    output_file.close()
    print("Ended")

    



if __name__ == "__main__":

    output_file = open("1.txt",'w') #this too (read next comment first) except this gets closed so
    
    segments_done = 0
    #....
    
    #Wait for user to start & print 4 them, also set start time
    print("Press [ctrl+shift+\\] to start")
    keyboard.wait("ctrl+shift+\\")
    START_TIME = time.time() #this is what a constant is right?? It never changes after here
    if False:
        print(">>> Info:   to be put in")
    print("Started")
    
    keyboard.add_hotkey("alt+q", on_cut_hotkey_pressed, ["accept"])
    keyboard.add_hotkey("alt+w", on_cut_hotkey_pressed, ["reject"])
    keyboard.add_hotkey("alt+e", on_cut_hotkey_pressed, ["retake accepted"])
    #might be an alternative to strings here
    
    
    keyboard.wait("ctrl+shift+\\")
    
    mark_cut_action( EndCut(get_current_time()) )
    output_file.close()
    print("Ended")

    