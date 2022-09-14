from dataclasses import dataclass
from typing import List, Tuple
from moviepy.editor import *


class Segment:
    start_time : float
    end_time :float
    is_cut : bool
    
    def __repr__(self) -> str:
        if self.is_cut: x = "Cut"
        else: x = "Uncut"
        return f"Segment({self.start_time} - {self.end_time}: {x})"

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.is_cut = None
    
    def mark_as_cut(self):
        self.is_cut = True
    def mark_as_not_cut(self):
        self.is_cut = False

    def is_cutt(self):
        return self.is_cut



def run_process_mode(): #main
    #todo: either put in subfolder for the videos or make this a system wide command (idk how currently)

    video_file_name, ts_file_name = get_file_names_from_user() #also checks for validity
    output_file_name = get_output_file_name(video_file_name)

    edit_video(video_file_name, ts_file_name, output_file_name)

    #todo: option to run time cutter automatically after writing is finished


    pass

def edit_video(video_file_name, ts_file_name, output_file_name):
    print("Parsing timestamps file...")
    timestamps_data = parse_timestamps_file(ts_file_name)

    print("Building segments...")
    all_segments = get_list_of_segments(timestamps_data)
    uncut_segments = get_list_of_uncut_segments(all_segments)
    print(uncut_segments)


    print("Building VideoFileClips...")
    #concrete things below here :0 (im tired)
    main_vfc = VideoFileClip(video_file_name)
    vfc_list = get_vfc_list(uncut_segments, main_vfc)
    final_vfc = concatenate_videoclips(vfc_list)

    print("Writing Output File")
    final_vfc.write_videofile(output_file_name)



def get_output_file_name(video_file_name:str):
    #todo: reconsider tis + add more questions at the start
    return "CUT_"+ video_file_name + ".mp4"



def get_vfc_list(segments_list:List[Segment], main_vfc:VideoFileClip) -> List[VideoFileClip]:
    vfc_list = []
    for s in segments_list:
        vfc_list.append(main_vfc.subclip(s.start_time, s.end_time))
    return vfc_list


def get_list_of_segments(timestamps_data: List[Tuple[float, str]]):
    segments_list = []

    last_timestamp = 0
    for timestamp, action in timestamps_data:
        segment = Segment(last_timestamp, timestamp)
        
        if action == "Reject" or action == "End":
            segment.mark_as_cut()
        elif action == "Accept":
            segment.mark_as_not_cut()
        
        elif action == "Retake A":
            segment.mark_as_cut()
            #mark last uncut segment as cut
            for previous_segment in reversed(segments_list):
                if not previous_segment.is_cut:
                    previous_segment.mark_as_cut()
                    break

        segments_list.append(segment)
        last_timestamp = timestamp

    return segments_list

def get_list_of_uncut_segments(list_of_segments:List[Segment]):
    output = []
    for segment in list_of_segments:
        if not segment.is_cut:
            output.append(segment)
    return output #todo list comprehension cause why not ig



def parse_timestamps_file(ts_file_name):
    with open(ts_file_name) as file:
        timestamps_file_data = file.readlines()
    timestamps_file_data = parse_ts_file_data_into_seconds_action_format(timestamps_file_data)
    return timestamps_file_data

def parse_ts_file_data_into_seconds_action_format(file_lines):
    #todo if we changed the file to be in minutes time we'd have to deconvert it here
    
    output = []
    file_lines = file_lines[1:-1]  #todo: dont do this if there is no header or footer
    
    for line in file_lines:
        new_line = line.strip().split("\t")
        new_line[0] = float(new_line[0])
        output.append(new_line)
    
    return output





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
            x = VideoFileClip(vid_file_name)
        
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



    
    
    






if __name__ == "__main__":
    run_process_mode()