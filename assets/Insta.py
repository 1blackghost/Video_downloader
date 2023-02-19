'''
Module used to work with instagram downloading videos and audios.
'''
from instascrape import *

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 \
    Safari/537.36 Edg/79.0.309.43",
    "cookie": 'sessionid=58332910367%3ANA3xnanZFVLREJ%3A19%3AAYeqymjb_6806js4-BRaghhWXhKZLCZALIMi5SxiTA;'
}

insta_reel=Reel("https://www.instagram.com/reel/Couxsr3pepB")

insta_reel.scrape(headers=headers)

insta_reel.download("download_path.mp4")