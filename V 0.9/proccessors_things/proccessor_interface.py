#eventually proccessor interface would only call on other things

class ProccessorsInterface():
    def __init__(self, display):
        self.display = display
    
    def print(self, str):
        self.display.print(str)

    def write_to_file(self, to_write):
        print(to_write)


    
