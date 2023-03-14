#this file deals with the trimmer routes

#imports
import os
from main import app
from flask import request
import json


@app.route("/trim/<thing>",methods=["GET","POST"])
def trimmer(thing):
	if request.method=="POST":
		starttime=(60*60*int(request.form["sh"])+60*int(request.form["sm"])+int(request.form["ss"]))
		endtime=(60*60*int(request.form["th"])+60*int(request.form["tm"])+int(request.form["ts"]))
		#starttime and endtime in ms
		print(starttime,endtime,thing)
			
		return json.dumps({"status":"ok"})
