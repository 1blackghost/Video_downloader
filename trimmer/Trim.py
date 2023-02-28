from moviepy.editor import *
import uuid

'''
    This module helps to trim video and music file and saves in appropriate formats.
'''

class Trimmer():
    '''
        Takes filename along with startime ,end time and extension to be saved with,
        returns status code along with saved filename which will be unique.
    '''
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
    
    def trim_video(self, start: int, end: int) -> str:
        video = VideoFileClip(self.file_name);
        clip = video.subclip(start, end);
        filename = f"{str(uuid.uuid4())}.mp4"
        clip.write_videofile(filename, codec='libx264')
        return filename