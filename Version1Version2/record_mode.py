"""
Structure 2:
running list of segments
effects can:
 - start segment
 - end segment
 - split a previous segment
 - apply to any previous segment
 - apply to next segment
 - apply to all upcoming segments until it is toggled off
 - 
 - 
 - 
 need subsegments then
 eg timelapse effec
 - split next segment?????

so:
active effects recieve a ping every time:
 - new segment starts/ends
 - their hotkey is pressed again (can have multiple hotkeys)

active effects can:
 - apply to the most recent segment(s)
 - end
 - apply to other segments
 - talk to the user (maybe pause/cut part where talking)

effects under this system:
    - reject/cut
        - Cut: cut last segment, Accept: Nothing, 
        Retake A, go through segments that are not cut and make the 1st cut
        -needs not to step on other effect's segments
    - simple effect:
        - hotkey starts
        - hotkey stops
        - ()









System 2

each effect/module has its own stop/start tracking


effects under this system:
    - simple effect:
        - hotkey starts
        - hotkey stops
    - reject/accept
        - h







"""
