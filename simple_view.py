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
import re
from nanoid import generate
from trimmer import Trim
import time
from DBMS import helper





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
    values=helper.read_for(session["uid"])
    return send_file(values[2],as_attachment=True)


def findIfDownloadComplete(uid,filename,size,d,res,type):
    dir_path=os.getcwd()
    if str(type)=="video":
        newD=d["video"][str('"'+res+'"')][0]
    elif str(type)=="audio":   
        newD=d["audio"][str(res)][0]
    newD=str(newD).split("/")[1]
    file_path=os.getcwd()+"/static/"+filename
    print(file_path)
    helper.update_this(uid,filename=file_path)
    dir_path=os.getcwd()
    starter=1
    with app.app_context():
        while starter:
            time.sleep(1)
            now_size=os.path.getsize(file_path)
            if int(size)==int(now_size):
                helper.update_this(uid,download_complete=1,starter=0)
                starter=0
                break

                

@app.route("/return-percentage",methods=["POST","GET"])
def find_percentage():
    value=helper.read_for(session["uid"])
    if int(value[4])==0:
        t=threading.Thread(target=findIfDownloadComplete,args=(session["uid"],session["filename"],session["total_size"],session["d"],session["res"],session["type"]))
        t.start()
        helper.update_this(session["uid"],starter=1)

    if int(value[3])==1:
        helper.update_this(session["uid"],percentage=100)
        percentage=100
    read_again=helper.read_for(session["uid"])

    return json.dumps({'percentage':str(read_again[5])})


@app.route("/",methods=["POST","GET"])

#simple download post entry point
def simple():
    global conn
    global cursor
    uid=helper.insert_this()
    session["uid"]=uid
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
            session["filename"]=filename
            helper.update_this(uid=session["uid"],domain="youtube",filename=filename)
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
        helper.update_this(uid=session["uid"],filename=session["filename"])
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
        helper.update_this(uid=session["uid"],filename=session["filename"])
        newD=d["audio"][str(res)] 
        session["total_size"]=yt.download(str(res),newD,filename=session["filename"])
        return json.dumps({'status':'ok'})
    else:
        return json.dumps({'status':'bad'})

@app.route("/trim/<thing>", methods=["GET", "POST"])
def trimmer(thing: str) -> json:
    if request.method == "POST":
        starttime = (
            3600 * int(request.form.get("sh"))
            + 60 * int(request.form.get("sm"))
            + int(request.form.get("ss"))
        )
        endtime = (
            3600 * int(request.form.get("th"))
            + 60 * int(request.form.get("tm"))
            + int(request.form.get("ts"))
        )
        thread_func_thread = threading.Thread(target=thread_func, args=(thing, starttime, endtime, session.get('url')))
        thread_func_thread.start()
        
        return json.dumps({"status": "ok"})


def download_thread_func(yt_download_obj: object, newD: list, resolution: str, title: str) -> None:
    total_size = yt_download_obj.download(resolution, newD, filename=title)
    while True:
            time.sleep(1)
            now_size=os.path.getsize(f'static/{title}')
            if int(total_size) == int(now_size):
                return


def trim(starttime: int, endtime: int, title: str) -> None:
    trim_obj = Trim.Trimmer(title)
    filename = trim_obj.trim_video(starttime, endtime)
    global file_path
    file_path = os.getcwd()+"/static/"+filename
    print("file_path: ", file_path)

    global download_complete
    download_complete = 1


def thread_func(thing: str, starttime: int, endtime: int, url: str) -> None:
    yt_download_obj = Yt.Y_D(url)
    availablity = yt_download_obj.check_available()
    resolution = list(availablity[thing])[0]
    newD = availablity[thing][resolution]
    resolution = resolution.replace('"', "")

    ext = newD[0].split("/")[1]
    title = f"{str(generate(size=10))}.{ext}"

    download_thread = threading.Thread(
        target=download_thread_func, args=(yt_download_obj, newD, resolution, title)
    )
    download_thread.start()
    download_thread.join()
    trim_thread = threading.Thread(target=trim, args=(starttime, endtime, title))
    trim_thread.start()
