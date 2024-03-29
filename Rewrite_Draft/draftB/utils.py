
import datetime
from math import ceil
import time

class Timer:
    last_unpause_time = None #really time since last pause
    time_before_last_pause = None
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


def truncate_number_str(number, digits_after_decimal=2):
    multiplier = 10 ** digits_after_decimal # to the power of
    num = float(number) #just in case
    truncated_num = int(num * multiplier)  /  multiplier  #eg x = 25.54321: x=(x*100)=2554.321| x=(int(x)) = 2554| x = x/100 = 25.54
    
    #make the decimals place have the appropriate number of digits if it has less (might be a better way to do this)
    semifinal_string = str(truncated_num)
    while len(semifinal_string.split(".")[1]) < digits_after_decimal:
        semifinal_string += "0"

    return semifinal_string



def addToMultiDimensionalListDict(dict, key, value):
    if key not in dict:
        dict[key] = [value]
    else:
        dict[key].append(value)

def addToListDict(dictt, key, value):
    isList = isinstance(value, list)

    if key not in dictt:
        if isList:
            dictt[key] = value
        else:
            dictt[key] = [value]
    else:
        if isList:
            dictt[key].extend(value)
        else:
            dictt[key].append(value)

