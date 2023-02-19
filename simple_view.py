'''
This .py file deals with simple download view.
'''
#imports
from main import app
from flask import request
from assets import regex

@app.route("/simple",methods=["POST","GET"])

#simple download post entry point
def simple():
    if request.method=="POST":
        url=request.form['url']
        check=regex.ReSystem(str(url))
        val=check.Check()
        if val==0:
            return "Youtube"
        elif val==1:
            return "Instagram"
        else:
            return "Invalid Url Detected"