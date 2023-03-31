'''
This .py file deals with simple download view.
'''
#imports
import os
from main import app
from flask import request,jsonify,session,send_file,g
from assets import regex,Yt
import json
import threading
import time
import random
import re
import nanoid
from nanoid import generate


download_complete=0
starter=False
file_path=""
percentage=0


def get_key(url):

    video_key = ""

    # extract video key from youtube.com/watch?v= URL format
    match = re.search(r"youtube\.com/watch\?v=([A-Za-z0-9_-]{11})", url)
    if match:
        video_key = match.group(1)
    # extract video key from youtu.be URL format
    match = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", url)
    if match:
        video_key = match.group(1)
    return video_key

@app.route("/getFile",methods=["GET"])
def send_the_file():
    return send_file(file_path,as_attachment=True)


def findIfDownloadComplete(filename,size,d,res,type):
    global download_complete
    global starter
    global file_path
    dir_path=os.getcwd()
    if str(type)=="video":
        newD=d["video"][str('"'+res+'"')][0]
    elif str(type)=="audio":   
        newD=d["audio"][str(res)][0]
    newD=str(newD).split("/")[1]
    file_path=os.getcwd()+"/static/"+filename
    print(file_path)
    dir_path=os.getcwd()

    with app.app_context():
        while starter:
            time.sleep(1)
            now_size=os.path.getsize(file_path)
            if int(size)==int(now_size):
                download_complete=1
                starter=False

@app.route("/return-percentage",methods=["POST"])
def find_percentage():
    global download_complete
    global starter
    global percentage
    try:
        if starter==False:

            t=threading.Thread(target=findIfDownloadComplete,args=(session["filename"],session["total_size"],session["d"],session["res"],session["type"]))
            t.start()
            starter=True
    except:
        #the trimmer goes here.
        pass
    if download_complete==1:
        percentage=100

    return json.dumps({'percentage':str(percentage)})


@app.route("/",methods=["POST","GET"])

#simple download post entry point
def simple():
    global yt
    global download_complete
    global d 
    download_complete=0
    starter=False
    file_path=""
    percentage=0
    if "url" in session:
        yt=Yt.Y_D(session["url"])

    if request.method=="POST" and "url" in request.form:
        url=request.form['url']
        check=regex.ReSystem(str(url))
        val=check.Check()
        if val==0:
            yt=Yt.Y_D(url)
            session["url"]=url
            filename=generate()
            session['filename']=filename
            d=yt.check_available()
            session["d"]=d
            return json.dumps({'status':'ok',"domain":"youtube","src":str(url),"key":"https://www.youtube.com/embed/"+str(get_key(url)),"data":d})
        elif val==1:
            return json.dumps({'status':'ok',"domain":"instagram","src":str(url)})
        else:
            return json.dumps({'status':'bad','domain':'none'})
    elif request.method=="POST" and "videores" in request.form:
        d=session["d"]
        res=request.form["videores"]
        session["res"]=res
        session["type"]="video"
        filename=session["filename"]
        session['filename']=filename+".mp4"
        newD=d["video"][str('"'+res+'"')]   
        session["total_size"]=yt.download(str(res),newD,filename=session["filename"])
        
        return json.dumps({'status':'ok'})
    elif request.method=="POST" and "audiores" in request.form:
        d=session["d"]
        res=request.form["audiores"]
        session["res"]=res
        session["type"]="audio"
        filename=session["filename"]
        session['filename']=filename+".webm"
        newD=d["audio"][str(res)] 
        session["total_size"]=yt.download(str(res),newD,filename=session["filename"])
        return json.dumps({'status':'ok'})
    else:
        return json.dumps({'status':'bad'})

@app.route("/trim/<thing>",methods=["GET","POST"])
def trimmer(thing):
    if request.method=="POST":
        starttime=(60*60*int(request.form["sh"])+60*int(request.form["sm"])+int(request.form["ss"]))
        endtime=(60*60*int(request.form["th"])+60*int(request.form["tm"])+int(request.form["ts"]))
        #starttime and endtime in ms
        print(starttime,endtime,thing)
        global download_complete
        download_complete=1
        return json.dumps({"status":"ok"})
