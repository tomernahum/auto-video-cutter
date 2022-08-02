import time

#todo add error checking for if you didnt start the timer

#timer mostly copied from old version of this
class Timer:
    def __init__(self) -> None:
        self.start_time:float = None #really time at last unpause
        self.time_before_pause:float = None
        self.is_paused:bool = None

        self.default_formater = Timer._default_formater
    
    def start_timer(self, start_time="now"): 
        if start_time == "now": self.start_time = time.time()
        else: self.start_time = start_time
        self.time_before_pause = 0
        self.is_paused = False
    
    def toggle_pause(self):

        if self.is_paused: # then unpause
            self.start_time = time.time()
            self.is_paused = False
        
        else: # then pause
            self.is_paused = True
            elapsed_time = time.time() - self.start_time
            self.time_before_pause += elapsed_time 
            self.start_time = None
    def skip_ahead(self, secs): self.time_before_pause += secs


    
    def get_current_time(self) -> float:
        if self.start_time == None:
            return None
        
        if self.is_paused:
            current_time = self.time_before_pause
        else:
            current_time = (time.time() - self.start_time) + self.time_before_pause
        return current_time
    
    def get_current_time_truncated(self, digits_after_decimal=2):
        if self.start_time == None:
            return None
        
        return Timer._truncate_number_str(self.get_current_time(), digits_after_decimal)
    
    def get_current_time_formatted(self, formatter="default"):
        if formatter == "default":
            formatter = self.default_formater
        current_time = self.get_current_time()
        return formatter(current_time)
    

    @staticmethod
    def _truncate_number_str(number, digits_after_decimal): #copied from other file
            multiplier = 10 ** digits_after_decimal # to the power of
            num = float(number) #just in case
            truncated_num = int(num * multiplier)  /  multiplier  #eg x = 25.54321: x=(x*100)=2554.321| x=(int(x)) = 2554| x = x/100 = 25.54
            
            #make the decimals place have the appropriate number of digits if it has less (might be a better way to do this)
            semifinal_string = str(truncated_num)
            while len(semifinal_string.split(".")[1]) < digits_after_decimal:
                semifinal_string += "0"

            return float(semifinal_string)

    @staticmethod
    def _default_formater(secs_time:float, shorten_seconds_above_1_min=False) -> str:
        secs_time = float(secs_time)
        minutes, seconds = divmod(secs_time, 60)
        hours, minutes = divmod(minutes, 60)
        
        minutes = int(minutes)
        hours = int(hours)
        seconds = Timer._truncate_number_str(seconds, 1)

        if minutes == 0 and hours == 0:
            return f"{seconds}s"
        
        if shorten_seconds_above_1_min is True:
            seconds = int(float(seconds))
        
        if hours == 0:
            return f"{minutes}m:{seconds}s"
        else:
            return f"{hours}h:{minutes}:m{seconds}s"



    
