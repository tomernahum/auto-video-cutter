import time
from typing import Callable

class Timer:
    def __init__(self) -> None:
        self.time_at_last_unpause:float = None         #type: ignore
        self.time_before_pause:float = 0          #type: ignore 
        self.is_paused:bool = None                   #type: ignore 

    def start_timer(self, start_time:float="now"): #type: ignore
        if start_time == "now": 
            self.time_at_last_unpause = time.time()
        
        else: self.time_at_last_unpause = start_time 
        
        #self.additional_time = 0
        self.is_paused = False

    def is_started(self):
        if self.is_paused == None:
            return False
        return True

    def get_current_time(self) -> float:
        if not self.is_started():
            return 0
            #class TimerNotStarted(Exception): pass
            #raise TimerNotStarted

        
        if self.is_paused:
            return self.time_before_pause
        else:
            return (time.time() - self.time_at_last_unpause) + self.time_before_pause
        
        
        return current_time

    def toggle_pause(self):
        if self.is_paused:
            #unpause
            self.time_at_last_unpause = time.time()
            self.is_paused = False
        
        else:
            #pause
            self.is_paused = True
            elapsed_time = time.time() - self.time_at_last_unpause
            self.time_before_pause += elapsed_time

    def skip_ahead(self, secs): 
        self.time_before_pause += secs


    def get_current_time_formatted(self, formatting_function:Callable[[float],object]):
        return formatting_function(self.get_current_time())

    def get_current_time_truncatied(self):
        return self.get_current_time_formatted(truncate_number)

    def get_current_time_format_1(self):
        return self.get_current_time_formatted(format_time_1)


#----time formatting------

def truncate_number(number, digits_after_decimal=2): #copied from other file
        multiplier = 10 ** digits_after_decimal # to the power of
        num = float(number) #just in case
        truncated_num = int(num * multiplier)  /  multiplier  #eg x = 25.54321: x=(x*100)=2554.321| x=(int(x)) = 2554| x = x/100 = 25.54
        
        #make the decimals place have the appropriate number of digits if it has less (might be a better way to do this)
        semifinal_string = str(truncated_num)
        while len(semifinal_string.split(".")[1]) < digits_after_decimal:
            semifinal_string += "0"

        return float(semifinal_string)


def format_time_1(secs_time:float, shorten_seconds_above_1_min=False) -> str:
        secs_time = float(secs_time)
        minutes, seconds = divmod(secs_time, 60)
        hours, minutes = divmod(minutes, 60)
        
        minutes = int(minutes)
        hours = int(hours)
        seconds = truncate_number(seconds, 1)

        if minutes == 0 and hours == 0:
            return f"{seconds}s"
        

        if shorten_seconds_above_1_min is True:
            seconds = int(float(seconds))
        
        if hours == 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{hours}h {minutes}m {seconds}s"