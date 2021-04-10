#Name: Aastha Lamichhane
#File: routes.py

from appdir import app
from flask import request, render_template
import pymysql

@app.route('/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        #fetch data from form
        email = request.form.get("email")
        password = request.form.get("password")
        
        #mysql part
        conn = pymysql.connect(root="root", passwd="root", db="BookARide")
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlCommand = "select * from registeredUsers where email=%s"
        cursor.execute(sqlCommand, (email))
        user = cursor.fetchall()
        cursor.close()
        conn.close()
        
        #fetch the homepage
        if (user[email] == email.lower()):
            return render_template("home.html")
        else:
            ### need to change this. This should call login
            ### saying invalid email or password
            return render_template("home.html")
    elif request.method == 'GET':
        return render_template("login.html")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        return render_template("signup.html")
    elif request.method == 'GET':
        return render_template("signup.html")
