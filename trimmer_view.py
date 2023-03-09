#this file deals with the trimmer routes

#imports
import os
from main import app
from flask import request
import json


@app.route("/trim/<thing>",methods=["GET","POST"])
def trimmer(thing):
	if request.method=="POST":
		starttime=request.form["sh"]
		print(thing,starttime)
		return json.dumps({"status":"ok"})
