# 2 modes: Record & Proccess (Possibly Settings mode too)

#from record import start_record_mode
#from process_redo import run_process_mode

#todo: I think I should call it from system and add a main.py (I will look into it)
#so I don't have to import both modes when I will only run one


#will revisit/redo this whole file / input methods


def main():
    #ask user for mode
    mode = input("Choose Mode:   \n1)Record 2)Proccess 3)Settings/Info:   ")
    while mode != "1" and mode != "2":
        mode = input("invalid choice, valid choices: \"1\", \"2\":   ")
        
    #launch the correct mode
    if mode == "1":
        from record import start_record_mode
        start_record_mode(output_file_name=input("enter the name of the file to write to (no extension): ") + ".txt")
    
    elif mode == "2":
        
        video, ts = get_file_names_from_user()
        
        from process import run_process_mode
        run_process_mode(video, ts, get_output_file_name(video))








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

#used to be in proccess.py: prob will redo / seperate that
def get_file_names_from_user() -> Tuple[str, str]:  
    #establish functions  #Q: Am I overcomplicating this? Also: is this the best way to organize the place of these functions
    def ask_for_input(input_prompt:str, validity_checker_function):
        while True:
            file_name = input(input_prompt)
            
            is_valid, error_message = validity_checker_function(file_name)
            if is_valid:break
            else:
                print(error_message)
        return file_name

    def vid_file_is_valid(vid_file_name) -> Tuple[bool, str]: #todo doesnt seem to work
        try:
            #x = VideoFileClip(vid_file_name)
            pass
        
        except IOError:
            return False, "file not found"

        else:
            return True, "No Error"

    def ts_file_is_valid(vid_file_name) -> Tuple[bool, str]:
        try:
            file = open(vid_file_name, 'r')
            

        except IOError:
            return False, "file not found"
        
        else:
            
            if file.readline()[0:15] != "Timestamps file":
                return (False, "doesn't appear to be a timestamps file")
            
            file.close()
            return True, "No Error"

    if False:
        return "part0and1.mkv", "test.txt"


    #ask user for file names until it is valid  #Q: am i overcomplicating this?
    video_file_name = ask_for_input("Enter the name of the video file to process: ", vid_file_is_valid)
    ts_file_name = ask_for_input("Enter the name of the timestamps file with which to process: ", ts_file_is_valid)
    return video_file_name, ts_file_name

#same
def get_output_file_name(video_file_name:str):
    #todo: reconsider tis + add more questions at the start
    return "CUT_"+ video_file_name + ".mp4"




main()