from config_data.config_file_parser import ConfigFileParser
from input_events import InputEventsMonitor


def on_input_event(self, command_data):
    pass


config_data = ConfigFileParser().parse_config_file("config_file.json")
input_events_monitor = InputEventsMonitor(config_data, on_input_event)