'''
This is the main file of video downloader
'''
#imports
from flask import *
from assets import regex

#Creation of flask app
app=Flask(__name__)


#Main Entry Point Here.
@app.route("/")
def home():
    return render_template("index.html")

with app.app_context():
    #importing views from different files
    from simple_view import *
    from extras import *

if __name__=="__main__":
    app.run(debug=True)