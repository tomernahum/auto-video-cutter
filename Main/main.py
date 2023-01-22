from typing import * #type: ignore #todo

def main():
    #ask user for mode
    mode = input("Choose Mode:   \n1)Record 2)Process 3)Settings/Info:   ")
    while mode not in {"1", "2", "3"}:
        mode = input("invalid choice, valid choices: \"1\", \"2\", \"3\":   ")
        
    #launch the correct mode
    if mode == "1":
        from record import start_record_mode
        start_record_mode(output_file_name=input("enter the name of the file to write to (no extension): ") + ".txt")
    
    elif mode == "2":
        from process import start_process_mode
        start_process_mode()
    
    elif mode == "3":

        from config import run_config_mode
        run_config_mode()







#Notes:
# potentially should move on to edit part of this before adding in every little thing
# watching a vid about object oriented programming, heres me thinking:
#     - cut class
#     - subclasses of cut (accept class, reject class, retake a class)
#     - instead of getPastTense(label) it would be [cut subclass].getPastTense
#     - can we do anything else? like build_string takes 6 inputs, but they are all changing
#           - I guess the settings could be split into relative objects
#           - segments_done and final_length change every time
#     - I will try to learn a bit more (maybe go through harvardx cs50?)before redoing the editing part, which is good because it will not have this wierd hotkey thing it will all be one after the other so it might be more typicall program
#     - 
# Will eventually take a proper classes course so that I fill in the glaring gaps in my skills/knowledge

#todo next:
# - proper display descriptions for segments done & estimated_edited_vid_time
# - Minutes/Seconds display not just seconds
# - Figure out if import is the best way to call the other files since they are both being imported despite only one being called, maybe that doesn't really matter anyway?
# - Probably better system than \t for terminal dispplay
# - maybe a current time display if thats possible (+ projected final time which would require a rework)
# - Add a beep when started (for syncing purposes)
# ^ most of these probably dont require much creative energy except 2nd to last
# - look into hotkey override for other apps
# - add some of the settings below

#Settings: 
# - Timestamp display type (s/hms)
# - Put Edited Video timestamp first (yes/no) default: no
# - 


#todo later
# - Instead of engaging with terminal, engage with anythink that can be added to obs panel (localhost)

#Later Notes:
#Could consider making a cut silence effect to run before another say music effect



"""
#Notes
    #todo: either put in subfolder for the videos or make this a system wide command (idk how currently)
    #todo: option to run time cutter automatically after writing is finished
"""


main()
