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


download_complete=0
starter=False
percentage=0
sender=False
file_path=""
current_data=0
d={}

@app.route("/getFile",methods=["GET"])
def send_the_file():
    return send_file(file_path,as_attachment=True)

def trap_Value():
    return random.randint(90,95)

def value_check():
    return random.randint(1,20)


def findIfDownloadComplete(filename,size):
    global download_complete
    global starter
    global file_path
    global sender
    dir_path=os.getcwd()
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.startswith(filename):
                file_path = os.path.join(root, file)
                

    with app.app_context():
        while starter:
            time.sleep(1)
            if download_complete==1:
                download_complete=0
            now_size=os.path.getsize(file_path)
            print("SIZER :  !!!!",size,now_size)
            if int(size)==int(now_size):
                download_complete=1
                starter=False
                if not sender:
                    sender=True


@app.route("/return-percentage",methods=["POST"])
def find_percentage():
    global download_complete
    global starter
    global percentage

    if starter==False:

        t=threading.Thread(target=findIfDownloadComplete,args=(session["filename"],session["total_size"]))
        t.start()
        starter=True
    if "speed" not in session:
        session["speed"]=value_check()
    total=session["total_size"]
    global current_data
    if (percentage<95):
        current_data=int(session["speed"])+current_data
        percentage=int(int((current_data/total)*100)/2)
    else:
        percentage=96
    if download_complete==1:
        percentage=100


    trap=trap_Value()
    return json.dumps({'percentage':str(percentage),"trap":str(trap)})


@app.route("/",methods=["POST","GET"])

#simple download post entry point
def simple():
    global yt
    global download_complete
    global percentage
    global current_data
    current_data=0
    download_complete=0
    percentage=0
    starter=False
    sender=False
    file_path=""
    if request.method=="POST" and "url" in request.form:
        url=request.form['url']
        check=regex.ReSystem(str(url))
        val=check.Check()
        if val==0:
            global d
            yt=Yt.Y_D(url)
            session['filename']=yt.get_title()
            d=yt.check_available()
            session["d"]=d
            return json.dumps({'status':'ok',"domain":"youtube","src":str(url),"key":"https://www.youtube.com/embed/"+str(url.split("=")[1]),"data":d})
        elif val==1:
            return json.dumps({'status':'ok',"domain":"instagram","src":str(url)})
        else:
            return json.dumps({'status':'bad','domain':'none'})
    elif request.method=="POST" and "videores" in request.form:
        d=session["d"]
        res=request.form["videores"]
        newD=d["video"][str('"'+res+'"')]   
    
        session["total_size"]=yt.download(str(res),newD)
        
        return json.dumps({'status':'ok'})
    elif request.method=="POST" and "audiores" in request.form:
        d=session["d"]

        res=request.form["audiores"]
        newD=d["audio"][str(res)] 
        session["total_size"]=yt.download(str(res),newD)
        return json.dumps({'status':'ok'})
    else:
        return json.dumps({'status':'bad'})
