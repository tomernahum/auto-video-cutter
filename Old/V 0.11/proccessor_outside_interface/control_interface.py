from .interface import Interface

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from testt import X


class ControlInterface(Interface):
    def __init__(self, engine, caller_name="N/A") -> None:
        self.engine:X = engine

        self.caller_name = caller_name

    def start_recording(self):
        self.engine.start_recording()

    def pause_recording(self):
        self.engine.pause_recording()

    def end_recording(self):
        self.engine.end_recording()
    
    def recording_is_started(self):
        return self.engine.is_recording()
