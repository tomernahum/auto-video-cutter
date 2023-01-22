from command import Command

class ConfigTuple():
    def __init__(self, category_name, trigger_name, command_info) -> None:
        self.trigger_category_name = category_name
        self.trigger_name = trigger_name
        self.command_info = command_info

    def __repr__(self) -> str:
        return f"({self.trigger_category_name}, {self.trigger_name}, {self.command_info})"


class InputConfigData():
    def __repr__(self) -> str:
        return f"ConfigData{self.trigger_config_data}"

    def __init__(self) -> None:
        
        self.trigger_config_data: list[ConfigTuple] = [
        ]

    def add_trigger(self, category_name, trigger_name, command_info):
        self.trigger_config_data.append(ConfigTuple(category_name, trigger_name, command_info))


    def get_trigger_data(self) -> list[ConfigTuple]:
        return self.trigger_config_data