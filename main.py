from flask import Flask, render_template, redirect, url_for , flash
import MySQLdb		#Mysql connector
import base64
from flask import request

conn = MySQLdb.connect(host='localhost',user='mayur',passwd='mayur2219981092',port=8090,db="hr_management")
cursor = conn.cursor()

app = Flask(__name__)

app.secret_key = 'my unobvious secret key'

@app.route("/",methods=['GET','POST'])

def homepage():
	print("ENTERED")
	return render_template("index.html")

@app.route('/login',methods=['GET','POST'])

def login():
	username_present = False
	flag = False
	username_string = ""
	cursor = conn.cursor()
	Username = request.form['Username']
	Password = request.form['Password']
	print("Username",Username)
	print("Password",Password)
	cursor.execute("""SELECT username FROM login """)
	actual_usernames = cursor.fetchall()
	actual_usernames_list = list(actual_usernames)
	cust_length = len(actual_usernames_list)
	username_string = Username
	print(actual_usernames_list)
	for a in range(0,cust_length):
		if actual_usernames_list[a][0] == username_string:
			username_present = True

	if username_present == True:
		cursor.execute("""SELECT password FROM login WHERE username =%s""",[Username])
		actual_password = cursor.fetchone()
		actual_password_list = list(actual_password)
		print("password",actual_password_list)
		if actual_password[0] == Password:
			flag = True

	if flag == True:
		flash("Login Successful !!!")
		return render_template("dashboard.html")
	else:
		flash("Incorrect Password")
		return render_template("index.html")

	

if __name__ == "__main__":
	
	app.run(debug=True)
