import time
from config_data.config_file_parser import ConfigFileParser
from input_events import InputEventsMonitor


def on_input_event(command_data):
    print(command_data)


config_data = ConfigFileParser().parse_config_file("config_file.json")
input_events_monitor = InputEventsMonitor(config_data, on_input_event)
input_events_monitor.start_monitoring()

time.sleep(100)