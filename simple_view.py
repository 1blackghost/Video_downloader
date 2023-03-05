'''
This .py file deals with simple download view.
'''
#imports
from main import app
from flask import request,jsonify
from assets import regex,Yt
import json

@app.route("/return-percentage")
def find_percentage():
    return json.dumps({'percentage':0})


@app.route("/",methods=["POST","GET"])

#simple download post entry point
def simple():
    print(request.form)
    global d
    global yt
    if request.method=="POST" and "url" in request.form:
        url=request.form['url']
        check=regex.ReSystem(str(url))
        val=check.Check()
        if val==0:
            yt=Yt.Y_D(url)
            d=yt.check_available()
            return json.dumps({'status':'ok',"domain":"youtube","src":str(url),"key":"https://www.youtube.com/embed/"+str(url.split("=")[1]),"data":d})
        elif val==1:
            return json.dumps({'status':'ok',"domain":"instagram","src":str(url)})
        else:
            return json.dumps({'status':'bad','domain':'none'})
    elif request.method=="POST" and "videores" in request.form:
        res=request.form["videores"]
        newD=d["video"][str('"'+res+'"')]   
        yt.download(str(res),newD)
        return json.dumps({'status':'ok'})
    elif request.method=="POST" and "audiores" in request.form:
        res=request.form["audiores"]
        newD=d["audio"][str(res)] 
        yt.download(str(res),newD)
        return json.dumps({'status':'ok'})
    else:
        return json.dumps({'status':'bad'})
