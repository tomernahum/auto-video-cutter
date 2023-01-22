from dataclasses import dataclass
from typing import List, Tuple
from moviepy.editor import *


class Segment:
    start_time : float
    end_time :float
    _is_cut : bool
    
    def __repr__(self) -> str:
        if self._is_cut: x = "Cut"
        else: x = "Uncut"
        return f"Segment({self.start_time} - {self.end_time}: {x})"

    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self._is_cut = None
    
    def mark_as_cut(self):
        self._is_cut = True
    def mark_as_not_cut(self):
        self._is_cut = False

    def is_cut(self):
        return self._is_cut



def run_process_mode(video_file_name, ts_file_name, output_file_name): #main

    #todo: maybe check if files are valid here?

    edit_video(video_file_name, ts_file_name, output_file_name)

    #alternate inputs (idk whats best): VFC, ts_file readlines data



def edit_video(video_file_name, ts_file_name, output_file_name):
    print("Parsing timestamps file...")
    timestamps_data = parse_timestamps_file(ts_file_name)
    print(timestamps_data)
    print()

    print("Building segments...")
    all_segments = get_list_of_segments(timestamps_data)
    uncut_segments = get_list_of_uncut_segments(all_segments)
    print(all_segments)
    print()


    print("Building VideoFileClips...")
    #concrete things below here :0 (im tired) #still figuring out coding philosophy haha
    main_vfc = VideoFileClip(video_file_name)
    vfc_list = get_vfc_list(uncut_segments, main_vfc)
    final_vfc = concatenate_videoclips(vfc_list)

    print("Writing Output File...")
    final_vfc.write_videofile(output_file_name)







def get_vfc_list(segments_list:List[Segment], main_vfc:VideoFileClip) -> List[VideoFileClip]:
    vfc_list = []
    for s in segments_list:
        vfc_list.append(main_vfc.subclip(s.start_time, s.end_time))
    return vfc_list

#Bugged!
def get_list_of_segments(timestamps_data: List[Tuple[float, str]]):
    segments_list: List[Segment] = []

    last_timestamp = 0
    for timestamp, action in timestamps_data:
        segment = Segment(last_timestamp, timestamp)
        
        if action == "Rejected" or action == "Ended":
            segment.mark_as_cut()
        elif action == "Accepted":
            segment.mark_as_not_cut()
        
        elif action == "Retaking A.":
            segment.mark_as_cut()
            #mark last uncut segment as cut
            for previous_segment in reversed(segments_list):
                if not previous_segment.is_cut():
                    previous_segment.mark_as_cut()
                    break
                else:
                    continue
        else:
            raise Exception("Something went wrong")

        segments_list.append(segment)
        last_timestamp = timestamp

    return segments_list

def get_list_of_uncut_segments(list_of_segments:List[Segment]):
    output = []
    for segment in list_of_segments:
        if not segment._is_cut:
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









    
    
    






if __name__ == "__main__":
    import sys
    run_process_mode(sys.argv[1], sys.argv[2], f"CUT_{sys.argv[1]}.mp4")