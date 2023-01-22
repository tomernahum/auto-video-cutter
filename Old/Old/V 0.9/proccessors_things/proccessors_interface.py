#eventually proccessor interface would only call on other things

class ProccessorsInterface():  
    def __init__(self, display):
        self.display = display
    
    def print(self, str):
        self.display.print(str)
        
    def write_effect_to_file(self, effect_name, start_time, stop_time, parameters:list = []):
        to_write = [effect_name, start_time, stop_time] + parameters
        print(f"wants to write: {to_write}")
        #todo pass this into writer etc


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from record_mode import Engine
class ControlProccessorsInterface(): #special. also this might not be the best place for it idk. also this 's interface system might get revised
    def __init__(self, engine) -> None:
        self.engine: "Engine" = engine

    def start_recording(self):
        self.engine.start_recording()
    
    def end_recording(self):
        self.engine.end_recording()
    
    def pause_recording(self):
        self.engine.pause_recording()

    def recording_is_started(self):
        return self.engine.is_started
    
