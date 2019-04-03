from flask import Flask, render_template, redirect, url_for ,flash
import MySQLdb		#Mysql connector
import base64
import re
from passlib.hash import pbkdf2_sha256
from flask import request

conn = MySQLdb.connect(host='localhost',user='root',password='utdnetzu',port=8080,db="HR_management")
cursor = conn.cursor()

app = Flask(__name__)

app.secret_key = 'my unobvious secret key'

def checkstring(inputstring):
	F = 0;
	length = len(inputstring)
	for a in range(0,length):
		if (inputstring[a] >= 'a' and inputstring[a] <= 'z') or (inputstring[a] >= 'A' and inputstring[a] <= 'Z'):
			F = 1
		else:
			F = 0
	if F == 1:
		return False
	else:
		return True
	
@app.route("/",methods=['GET','POST'])

def homepage():
	print("ENTERED")
	flash("Welcome!! ")
	return render_template("index.html")

@app.route("/login",methods=['GET','POST'])

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
		return redirect('/dashboard')
	else:
		flash("Incorrect Password")
		return render_template("index.html")

@app.route("/dashboard",methods=['GET','POST'])

def dashboard():
	print("ENTERED")
	return render_template("dashboard.html")
	
@app.route("/create_emp",methods=['GET','POST'])
	
def create_emp():
	print("ENTERED")
	return render_template("create_employee.html")	
	
@app.route("/add_employee",methods=['GET','POST'])
	
def add_employee():
	print("entered")
	Gender = ['Male','Female','Other']
	Username_to_string1 = ""
	flag = False
	cursor = conn.cursor()
	
	try:
		Name=request.form["Name"]
		value1 = checkstring(Name)
		if value1 == True:
			flash("Please enter a Valid First Name !!!")
			return redirect('/create_emp')
			
		F_name=request.form["F_name"]
		value2 = checkstring(F_name)
		if value2 == True:
			flash("Please enter a Valid Fathers  Name !!!")
			return redirect('/create_emp')
		
		birth_date=request.form["dob"]
			
		email = request.form["Email"]
		if re.search('@',email):
			em = 0
		else:
			flash("Please Enter Valid Email  !!!")
			return 	redirect('/create_emp')
		
		password = request.form["Password"]
		hash_password = pbkdf2_sha256.hash(password)
		gender=request.form["optionsRadios"]
		gender_index = int(gender)		
		actual_gender = Gender[gender_index]
		local_addr=request.form["LA"]	
		permanent_addr=request.form["PA"] 
		
		cursor.execute("""Insert into employee(name,fathername, dob ,email ,gender, local_address,permanent_address,employee_id) values (%s,%s,%s,%s,%s,%s,%s,%s)""",(Name,F_name,birth_date,email,actual_gender,local_addr,permanent_addr,1))
		conn.commit()
		flash("Employee successfully added !!!")
		return redirect('/dashboard')
		
	except Exception as e:
		return(str(e))	

@app.route("/employee_list",methods=['GET','POST'])
	
def employee_list():
	print("ENTERED")
	return render_template("employee_list.html")	

@app.route("/holiday_list",methods=['GET','POST'])
	
def holiday_list():
	print("ENTERED")
	return render_template("holiday_list.html")	


@app.route("/add_holiday",methods=['GET','POST'])
	
def add_holiday():

	try:
		Date=request.form["Date"]
		Date.split('/')
		print("Date")
		month,date,year=Date.split('/')
		Occasion=request.form["occasion"]
		
		cursor.execute("""Insert into holidays(month,year,occasion) values (%s,%s,%s)""",(month,year,Occasion))
		conn.commit()
		flash("Holiday successfully added !!!")
		return redirect('/holiday_list')
		
	except Exception as e:
		return(str(e))
			
if __name__ == "__main__":
	app.run(debug=True)
