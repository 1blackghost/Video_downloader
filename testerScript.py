

#this is file used to test the overall functionality of the website and rough works.


#-------------------Start Here-------------------------#
'''
Currently, this script testing the creation of custom named file during download of youtube
contents.

'''
#imports
from nanoid import generate

print(generate())


from assets import Yt

yt= Yt.Y_D("https://www.youtube.com/watch?v=UrZhrchVhSg")
d=yt.check_available()
print(d)
newD=d["video"][str('"720p"')]  
print(newD)
res="720p"
yt.download(str(res),newD,"blah.mp4")