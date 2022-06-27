
from abc import ABC, abstractmethod, abstractproperty
from typing import TYPE_CHECKING, Protocol


if TYPE_CHECKING:
    from record_mode import EngineInterface


class Command(ABC): #WIP
    @abstractproperty
    def type(self) -> str: #aka which proccessor to send it to
        return "abstract_command"

    def get_type(self) -> str:
        return self.type

class ProccessingObj(ABC):
    
    @abstractmethod
    def trigger(self, command:"Command", interface:"EngineInterface", current_time:"float"):
        pass
    
    @abstractmethod
    def finish_up(self, interface:"EngineInterface"):
        pass






if __name__ == "__main__":
    pass