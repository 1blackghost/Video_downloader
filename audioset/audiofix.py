import subprocess


class Audio_fix:

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def check_for_audio(self) -> int:
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=nb_streams", "-of",
                             "default=noprint_wrappers=1:nokey=1", self.filepath],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        return (int(result.stdout) - 1)
    
    def join_audio(self):
        pass

    def download_audio(self):
        pass
