from flask import Flask, render_template, redirect, url_for , flash
import MySQLdb		#Mysql connector
import base64


app = Flask(__name__)

@app.route("/",methods=['GET','POST'])

def homepage():
	print("ENTERED")
	return render_template("index.html")
	

if __name__ == "__main__":
	
	app.run(debug=True)
