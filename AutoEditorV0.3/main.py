# 2 modes: Record & Proccess (Possibly Settings mode too)

from record import start_record_timestamps_mode
#todo: I think I should call it from system and add a main.py (I will look into it)
#so I don't have to import both modes when I will only run one


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


#todo next:
# - proper display descriptions for segments done & estimated_edited_vid_time
# - Minutes/Seconds display not just seconds
# - Call it properly
# - maybe a current time display if thats possible (+ projected final time which would require a rework)
# - Add a beep when started (for syncing purposes)
# ^ all of these probably dont require much creative energy except 2nd to last
# - 


#Later Notes:
#Could consider making a cut silence effect to run before another say music effect

