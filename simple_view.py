'''
This .py file deals with simple download view.
'''
#imports
from main import app
from flask import request
from assets import regex
import json

@app.route("/",methods=["POST","GET"])

#simple download post entry point
def simple():
    if request.method=="POST":
        url=request.form['url']
        check=regex.ReSystem(str(url))
        val=check.Check()
        if val==0:
            return json.dumps({'status':'ok',"domain":"youtube","src":str(url),"key":"https://www.youtube.com/embed/"+str(url.split("=")[1])})
        elif val==1:
            return json.dumps({'status':'ok',"domain":"instagram","src":str(url)})
        else:
            return json.dumps({'status':'bad','domain':'none'})