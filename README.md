# asset_creator
Python and ffmpeg tool to generate images out of text prompts and convert to mp4 files.


Install:
    Pillow
    PyQt5
    ffmpeg

The `Assets_creator_v5.py`, `prompts.txt` and `arial.ttf` `video_converter_.v2.sh` 
files all neeed to be in the same folder location. 

The `video_converter_v2.sh` file can be edited to allow for different video lengths by changing the `libx265 -r 1 -t 300` line from `300` for seconds to however long you want the videoe to be.
