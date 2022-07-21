from command import Command

class CommandConverter():
    def get_input_call_function(self, output_call):
        def call_function(command_data):
            self.convert_command_and_call_next(output_call, command_data)
        
        return call_function
        #I believe this is how its done
    
    
    def convert_command_and_call_next(self, output_call_func, command_data):
        command = CommandConverter().convert_command(command_data)
        output_call_func(command)

    

class CommandConvertertt():
    def convert_command(self, command_data):
        pass

        

    