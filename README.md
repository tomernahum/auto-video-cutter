# auto-video-cutter
Edits videos based on timestamps you mark with hotkeys as you record the video. \
Core mechanic is Accept Segment / Reject Segment (see below) \
Does not trim silence as many other programs exist to do that, but can automatically run a silence trimming program after cuts are made. (*not yet implemented)

Timestamps are created with keyboard shortcuts while you are recording, afterward the program will edit the video automatically based on the timestamps file
 

- Any time you [Accept Segment] that segment makes it into the final video, 
- Every time you [Reject Segment] that segment gets cut out and you are left to do a retake
- You can also [Reject Last Accepted] which will delete the last already accepted segment leaving you to retake it 
- You can also mark timestamps or segments for effects to be applied (*COMING SOON (I am working on this currently (I want to try make the system modular & robust))

Hit reject as many times as you want till you get a good take then hit accept (it will put in the segment from the last time you hit Reject till the time you hit Accept) 

Currently Implemented Features:
- Running total time & time after cuts in record mode




Features described are not necessarily implemented yet this is a work in progress
Also I will clean up the code more / properly learn proper coding structure / design pattern principles. Lots of things missing but the very basic functionality works and i wanted to publish this. I will work on this a lot more during the summer & create a framework for custom effects

Also I used github but did not really use git as it was intended fyi (so there are old versions in the files instead of branches and sometimes i commited very infrequently)

# How to Use
1. Open OBS or other video recording program and set start/stop recording hotkey to cntrl+shift+\ (hotkey custimization will be added later sorry)
2. Navigate to the folder in command terminal
3. run main.py and select record mode (or run record.py)
4. follow instructions   Note: Hotkeys will be detected even if window is not focused
5. press [alt+q for accept] [alt+w for reject] & [alt+e for retake/reject last accepted]   [alt+p for pause]
6. press cntrl+shift+\ to end
7. Put your video file in the main code folder
8. run proccess mode and type in the video & timestamps file names
9. wait
10. Done.

