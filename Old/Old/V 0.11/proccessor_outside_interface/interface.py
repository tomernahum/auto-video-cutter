
class Interface():
    def __init__(self, tbd, caller_name="N/A") -> None:
        self.caller_name = caller_name


    def notify(self, msg, current_time): #temp implementation obviously
        print(f"{self.caller_name} says: {msg}  at {current_time}")
    


