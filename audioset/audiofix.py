import subprocess
from assets import Yt
import ffmpeg
import re


class Audio_fix:
    def __init__(self, filepath: str, url: str) -> None:
        self.filepath = filepath
        self.url = url

    def check_for_audio(self) -> int:

        """
        Check if the video has the audio - return 1 if there is audio
        and return 0 if there is no audio
        """

        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=nb_streams",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                self.filepath,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return int(result.stdout) - 1

    def join_audio(self) -> str:

        """
        merge audio and video by using ffmpeg.output function
        """

        title, newD = self.download_audio()
        ext = newD[0].split("/")[1]
        cleaned_title = self.clean_title(title)

        input_video = ffmpeg.input(self.filepath)
        input_audio = ffmpeg.input(f"static/mergeAudio/{cleaned_title}.{ext}")

        output_file = f'static/{cleaned_title}_new.mp4'

        ffmpeg.output(
            input_video, input_audio, output_file, codec="copy",
        ).overwrite_output().run(quiet=True, overwrite_output=True) # overwrite_output=True not working, expected behaviour - overwrite file 

        return output_file

    def download_audio(self) -> str:
        """
        Download the audio of best quality by using download method
        from assets package Yt module
        """

        yt_download_obj = Yt.Y_D(self.url)
        availablity = yt_download_obj.check_available()

        resolution = list(availablity["audio"])[0]
        newD = availablity["audio"][str(resolution)]
        yt_download_obj.download(resolution, newD)

        return (yt_download_obj.get_title(), newD)

    def clean_title(self, title) -> str:
        """
        Downloaded files using pytube removes some special characters so for cohesive title - remove
        it using regex
        """

        cleaned_title = re.sub("[@#$%^&*_+=<>,./?;:|']", "", title)
        return cleaned_title
