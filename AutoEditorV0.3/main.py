# 2 modes: Record & Proccess (Possibly Settings mode too)

from record import start_record_timestamps_mode


#ask user for mode
mode = input("Choose Mode:   \n1)Record 2)Proccess 3)Settings/Info:   ")
while mode != "1" and mode != "2":
    mode = input("invalid choice, valid choices: \"1\", \"2\":   ")
    
#launch the correct mode
if mode == "1":
    start_record_timestamps_mode()
elif mode == "2":
    #start edit video mode
    pass




#Later Notes:
#Could consider making a cut silence effect to run before another say music effect

