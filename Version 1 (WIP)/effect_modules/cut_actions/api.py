#Q/N: Not sure about best practices for this sort of thing / etc

print("HELLO!")



from . import get_segment_blueprints

def get_segment_blueprints_list(timestamps_file):
    return get_segment_blueprints.get_segment_blueprints_list(timestamps_file)



def get_file_name():
    return "timestamps.txt"


def test():
    print("TEST!")




