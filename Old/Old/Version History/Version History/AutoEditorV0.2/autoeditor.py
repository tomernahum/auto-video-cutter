#BTW I am not very experienced at writing programs feel free to critique bad practice /etc (if someone is reading this lol)
#+ I did not use some sort of structure/notation convention, if that is important maybe I will implement it later 
""" 
Function: Mode 1: Record timestamps file (run at the same time as recording software), 
          Mode 2: Process timestamps file + long video into edited video
Timestamps:
1. Accept Clip
2. Reject Clip
3. Retake last accepted clip

4. Effect Segments (WIP)
5. Short Effect (WIP)
"""
"""
#Effects:
    - replace segment with edited clip (edits can be done by script or manually)
        - Visual Effects
        - Replace visuals but not audio in clip
        - replace 0 lenth segment with clip (insert clip)
    - transitions between cuts (doing this last)

"""


#currently you have to start timestamps and video recording at same time (like with same hotkey)
#todo: need to add a way to adjust it. Sync start time - maybe play a beep at TS recording start?, 
# maybe that could be auto detected (stay silent until then)
#+ maybe a manual time offset set before starting the TS recording if you are doing a bunch on a stream or something
#should eventually add support for a custom browser doc in obs (local .html files seem to work)

import keyboard
import time
import datetime

#Selct mode
mode = 0
while True:
    mode = input("Choose Mode: \n1)Record 2)Proccess 3)Settings/Info:  ")
    if mode != "1" and mode != "2":
        print("invalid choice, valid choices: \"1\", \"2\", \"3\"")
        continue
    
    mode = int(mode)
    break





if mode == 1: #Record Timestamps Mode
    #todo: make hotkeys based on stored file potentially to be modified in mode 3
    #todo: pause recording hotkey
    #learn % better
    
    #Create the hotkeys dictionary based on settings file; #might need refining / redoing
    hotkeys = {}
    def find_hotkeys(): #only gonna use this once but I want to have something segmented / collapsable
        pass
        #WIP
        """ this might all be scraped
        
        def find_line(linetofind, linelist): # potential thing
            for i in range(linelist):
                if linelist[i] == linetofind
                    return i
        
        settingsfile = open("settings.txt", r)
        settingsfilelist = settingsfile.readlines()
        settingsfile.close()
        
        find_line("Hotkeys:",settingsfilelist)
        
        
        hotkeys_found = False
        for line in settingsfilelist: #might be a more elegant way of doing this
            if hotkeys_found == False and line == "Hotkeys:":
               hotkeys_found = True
               continue
            
            elif hotkeys_found == True:
                if line == "/Hotkeys":
                    break
                
                function_name = ""
                hotkey = ""
                colon_found = False
                for j in line: #yeah I might redo this with more energy or whatever or look up how
                    if colon_found == False:
                        if j == ':':
                            colon_found = 1
                        else:
                            function_name += j
                    else:
                        hotkey += j
                function_name = function_name.strip()
                hotkey = hotkey.strip()
        """
    find_hotkeys()   #should find out the formatting conventions for stuff etc
    
    
    outputfile = input("enter the name of the file to write to (no extention): ")+".txt"
    outputfile = open(outputfile, "w")
    outputfile.write("Timestamps file for [autoeditor program] recorded on " + str(datetime.datetime.now()) + "\n")
    
    segments_done = 0
    start_time = None #will be set by the time its used
    def get_time_str():
        return str( int(( time.time() - start_time )*100)/100 ) #truncates to 2 decimal places
        #return str(time.time() - start_time)
    
    #bug: see below
    def mark_cut(label, bugthingsorry): #labels: 1.Accept 2.Reject 3.Reject Accepted
        global segments_done
        time_of_cut_str = get_time_str()
        
        if label == "accept":
            segments_done += 1
            print(time_of_cut_str + "\tAccepted" 
            + "\t%2d segments accepted, now recording #%2d"%(segments_done,segments_done+1))
            
            outputfile.write(time_of_cut_str + "\tAccepted\n")
            
        elif label == "reject":
            print(time_of_cut_str + "\tRejected" 
            + "\tre-recording segment #%2d"%(segments_done+1))
            
            outputfile.write(time_of_cut_str + "\tRejected\n")
            
        elif label == "retake accepted":
            segments_done += -1   #1 2 3 working on 4
            print(time_of_cut_str + "\tRetake A." 
            + "\tre-recording the previously accepted segment #%2d"%(segments_done+1))
            outputfile.write(time_of_cut_str + "\tRetake A\n")
            #should probably make this only able to go back 1 segment todo
        #could find somewhere to display segments as time-time
        pass
    
    effects_tracking = {}
    def mark_effect(label, bts):
        global effects_tracking
        time_of_cut_str = get_time_str()
          
        #Keep track if the effect is already on or off  
        to_print = ""
        if label in effects_tracking and effects_tracking[label] == True:
            effects_tracking[label] = False
            to_print = " Effect Segment Ended"
        else:
            effects_tracking[label] = True
            to_print = " Effect Segment Started"
        
        print(time_of_cut_str + "\t" + label + to_print)
        outputfile.write(time_of_cut_str + "\t"+label+" toggled\n")
        
    
    print("Press the set hotkey when you are ready to start") #add hotkey into print when settings created
    
    
    keyboard.wait("ctrl+shift+\\") #Set this to the same thing as obs
    start_time = time.time()
    print("Started")  
    keyboard.add_hotkey("alt+q", mark_cut, ('accept', "ignore this")) #bug: alt-q still types q sometimes
    keyboard.add_hotkey("alt+w", mark_cut, ('reject', "ignore this")) #bug, not puttin in "ignore this" makes it input each letter in reject etc
    keyboard.add_hotkey("alt+e", mark_cut, ('retake accepted', "ignore this"))
    #make scalable effect marker hotkeys
    keyboard.add_hotkey("alt+z", mark_effect, ('test effect', "ignore this" ))
    
    
    keyboard.wait("ctrl+shift+\\")
    
    outputfile.close()
    print("File Saved, Goodbye.") #to change later
    
    
if mode == 2: #Auto-Edit Video Mode
    from moviepy.editor import *   
    #^ I know this usually on the top but it takes a second/resources to import and it is used
    # here, the different modes are basically different programs, maybe they should be different files / functions
    
    
    #select the files. (temporary system)
    """ commented out for ease of testing but will eventually be replaced anyway
    while True:
        try:
            timestamps_file = open(input("type the name of the timestamps file: "), 'r')
            unedited_clip = VideoFileClip(input("type the name of the video file: "))
        except:
            print("File not found, try again")
            continue
        else:
            break
    """ 
    timestamps_file = open("test2.txt", 'r')
    unedited_clip = VideoFileClip("testvid2.mkv")
    
    print("Editing the video")
    #things it should be able todo at start
    # - Auto Detect Video files   - Let you select video files with gui?
    # - pick timestamp for it to offset to   - auto detect offset (whenever sound starts)
    # - Have the option to run a command/program after you are done (for using w/ silence skipper)
    
    #find the offset, probably with sound detection #todo
    offset = 0
    #any time there is a timestamp from the file just act like its + the offset
    
    
    #create Segment objects  with times to clip
    class Segment:
        def __init__(self, raw_start, raw_end):
            self.raw_start = raw_start   #raw = timestamp in uncut video
            self.raw_end = raw_end  #
        def __str__(self):
            return str(self.raw_start) + " - "+ str(self.raw_end)
        def get_raw_start(self):
            return self.raw_start
        def get_raw_end(self): 
            return self.raw_end 
    
    #mark the effects
    #mark the accepted Segments
    #MoviePy: Apply the effects
    #MoviePy: Do the cuts
    
    
    #Find the Segments that will make it into the video   (should be refactored as they say)
    accepted_segments = []
    
    raw_pointer_timestamp = 0 + offset #end of last segment already proccessed
    for i in timestamps_file:
        if i[0] == 'T':  #first line is not a timestamp
            continue 
        
        split_line = i.split("\t") #returns a list with each item that is seperated by \t
        timestamp = float(split_line[0]) + offset
        label = split_line[1].strip()
        
        if label == "Rejected":
            pointer_timestamp = timestamp
            #accepted_pointer_timestamp = accepted_pointer_timestamp
            
            
        elif label == "Accepted":
            raw_start = pointer_timestamp
            raw_end = timestamp
            output_segment = Segment(raw_start,raw_end)
            accepted_segments.append(output_segment)
            
            pointer_timestamp = timestamp
            
        elif label == "Retake A":  #todo: make name of this function consistent
            pointer_timestamp = timestamp
            del accepted_segments[-1]

    
    
    #stitch the clips together w/ Moviepy (temp)
    print("Accepted Segments:")
    output_moviepy_clips = [] 
    for segment_i in accepted_segments:
        print(segment_i)
        vfc = unedited_clip.subclip(segment_i.get_raw_start(), segment_i.get_raw_end())
        output_moviepy_clips.append(vfc)
    print("")
    final_vfc = concatenate(output_moviepy_clips)
    final_vfc.write_videofile("output.mp4") #todo: custom name system or auto-name
    
    
     
    
    
    #later I want one of the effects to be exporting that clip for manuel editing
    #it'd also be nice to have an option to export the clips into premier pro/etc
    #like that skip_silence project but we'll see if I can while using moviepy
    
    #export it
    unedited_clip.close()
    
    