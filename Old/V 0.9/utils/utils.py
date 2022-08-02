#misc functions - probably should be reorginized or smth




def truncate_number(number, digits_after_decimal=2): #copied from other file
        multiplier = 10 ** digits_after_decimal # to the power of
        num = float(number) #just in case
        truncated_num = int(num * multiplier)  /  multiplier  #eg x = 25.54321: x=(x*100)=2554.321| x=(int(x)) = 2554| x = x/100 = 25.54
        
        #make the decimals place have the appropriate number of digits if it has less (might be a better way to do this)
        semifinal_string = str(truncated_num)
        while len(semifinal_string.split(".")[1]) < digits_after_decimal:
            semifinal_string += "0"

        return float(semifinal_string)




def format_time(secs_time:float, shorten_seconds_above_1_min=False) -> str:
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

