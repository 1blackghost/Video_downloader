'''
This module checks the validation urls entered through the input

'''
#imports
import re

class ReSystem:
    '''
    Used to detect which url the user is trying to pass.
    Current Return values are:
    
    -1:Invalid or unidentified domain
    0:Youtube
    1:Instagram

    '''
    def __init__(self,url):
        self.url=url

    #validation for instagram 
    def validate_url_for_instagram(self):
        
        if self.url.startswith("https://www.instagram.com"):
            return True

        return None

    #validation for youtube
    def validate_url_for_youtube(self):
        youtube_regex = (
            r'(https?://)?(www\.)?'
            '(youtube|youtu|youtube-nocookie)\.(com|be)/'
            '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})')

        youtube_regex_match = re.match(youtube_regex, self.url)
        if youtube_regex_match:
            return youtube_regex_match

        return youtube_regex_match
    #Checks happens inside here
    def Check(self):
        checks=self.validate_url_for_youtube()
        if checks!=None:
            return 0
        checks=self.validate_url_for_instagram()
        if checks!=None:
            return 1
        return -1


