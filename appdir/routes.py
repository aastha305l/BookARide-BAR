#Name: Aastha Lamichhane
#File: routes.py

from appdir import app
from flask import request, render_template
from random import randint
from geopy.geocoders import Nominatim
import pymysql, string, hashlib, random, datetime

DRIVERORRIDER = "rider"
DRIVERID = -1;
RIDERID = -1;
RIDERSREVIEW = 0;
DRIVERLOCATION = ""
TOLOCATION = ""
FROMLOCATION = ""
DATE = ""
TIME = ""
COST = ""
COSTWITHSEC = 0.01
ALLOWEDTIME = 1 * 60 * 60 #in seconds

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        name = request.form["driverOrRider"]
        print(name)
        global DRIVERORRIDER
        if (name == "driver"):
            DRIVERORRIDER = "driver"
            print("From home: " + DRIVERORRIDER)
            return render_template("driverLogin.html")
        elif (name == "rider"):
            DRIVERORRIDER = "rider"
            return render_template("riderLogin.html")
    elif request.method == 'GET':
        return render_template("home.html")



#==========================================================================================================================================================================================#
#Driver Side


@app.route('/driverLogin', methods = ['POST', 'GET'])
def driverLogin():
    if request.method == 'POST':
        #fetch data from form
        formEmail = request.form.get("email")
        formPassword = request.form.get("password")
        global DRIVERORRIDER

        print("From driver login " + DRIVERORRIDER)
        
        #mysql part
        conn = pymysql.connect(user="root", passwd="Gyanisha@123", db="BookARide")
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlCommand = "SELECT * FROM RegisteredUsers where email=%s and driverRider=%s LIMIT 1"
        findDriverID = "SELECT * FROM DriverInfo where registeredID=%s;"
        findRiderID = "SELECT * FROM RiderInfo where registeredID=%s;"
        cursor.execute(sqlCommand, (formEmail, DRIVERORRIDER))
        user = cursor.fetchone()

        #if user does not exist anywhere
        if (user == None):
            #lets also check on the unregistered users if there is time
            sqlCommand = "select * from UnregisteredUsers where email=%s and driverRider=%s LIMIT 1;"
            cursor.execute(sqlCommand, (formEmail, DRIVERORRIDER))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if (user != None and user['email'] == formEmail.lower()):
                return """<html><body>Email is not verified yet. Please verify your email from your gmail account.</body></html>""" + render_template("driverLogin.html")
            elif (user == None):
                return """<html><body><p>Email not found!!! Please sign up!</p></body></html>""" + render_template("driverLogin.html")
        
        #get hashedPassword and randomString to cross-check
        formPassword += user['randString']
        
        #need to hash the password and check against the stored one
        temp = hashlib.md5(formPassword.encode())
        formHashedPassword = temp.hexdigest()

        
        #fetch the homepage
        if (user != None and user['email'] == formEmail.lower() and user['hashedPassword'] == formHashedPassword):
            if (DRIVERORRIDER == "driver"):
                cursor.execute(findDriverID, user['id'])
                driver = cursor.fetchone();
                DRIVERID = driver['id']
            else:
                cursor.execute(findRiderID, user['id'])
                rider = cursor.fetchone();
                RIDERID = user['id']
        
            cursor.close()
            conn.close()
            return render_template("riderHomePage.html")
        elif (user != None and user['hashedPassword'] != formHashedPassword):
            cursor.close()
            conn.close()
            return """<html><body><p>Wrong Password!!!</p></body></html>""" + render_template("driverLogin.html")
        
    elif request.method == 'GET':
        return render_template("driverLogin.html")

    

@app.route('/driverSignup', methods=['POST', 'GET'])
def driverSignup():
    global DRIVERORRIDER, DRIVERLOCATION
    if request.method == 'POST':
        #fetch data from form:
        formFirstName = request.form.get("firstName")
        formLastName = request.form.get("lastName")
        formEmail = request.form.get("email")
        formPhoneNumber = request.form.get("phoneNumber")
        formCarColor = request.form.get("carColor")
        formLicenseNum = request.form.get("licenseNumber")
        formCarModel = request.form.get("carModel")
        formCurrentLocation = request.form.get("currentLocation")
        formPassword = request.form.get("password1")
        DRIVERLOCATION = formCurrentLocation
        #print("Driverlocation ", DRIVERLOCATION, " ", formCurrentLocation)
        
        print("From Signup " + DRIVERORRIDER) 

        #connect to sql
        conn = pymysql.connect(user="root", passwd="Gyanisha@123", db="BookARide")
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        #check if the email is already registered
        sqlCommand = "select * from RegisteredUsers where email=%s"
        cursor.execute(sqlCommand, (formEmail))
        user = cursor.fetchone()
        if (user != None and user['driverRider'] == DRIVERORRIDER):
            cursor.close()
            conn.close()
            return "<html><body>Email already registered</body></head>" + render_template("driverLogin.html")

        #check if the email is in unregistered table
        sqlCommand = "select * from UnregisteredUsers where email=%s"
        cursor.execute(sqlCommand, (formEmail))
        user = cursor.fetchone()
        if (user != None and user['driverRider'] == DRIVERORRIDER):
            cursor.close()
            conn.close()
            return "<html><body>Email already used. Check your email inbox for email verification</body></head>" + render_template("driverLogin.html")

        
        #if not registered then insert into the database
        if (formPhoneNumber == ""):
            sqlCommand = "INSERT INTO UnregisteredUsers (firstName, lastName, email, hashedPassword, randString, driverRider, timeNow, timeThen, carColor, licenseNumber, carModel, currentLocation) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        else:
            sqlCommand = "INSERT INTO UnregisteredUsers (firstName, lastName, email, phoneNumber, hashedPassword, randString, driverRider, timeNow, timeThen, carColor, licenseNumber, carModel, currentLocation) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

            
        #generate random string of random length
        randLength = randint(5, 15)
        randString = ""
        t = string.ascii_letters + string.digits
        for i in range(randLength):
            randString += random.choice(t)
        formPassword += randString

        #hash the password
        temp = hashlib.md5(formPassword.encode())
        hashedPassword = temp.hexdigest()

        #time for them to confirm their id
        now = datetime.datetime.now()
        then = now + datetime.timedelta(days = 0, hours = 0, minutes = 10, seconds = 1)

        if (formPhoneNumber == ""):
            cursor.execute(sqlCommand, (formFirstName, formLastName, formEmail, hashedPassword, randString, DRIVERORRIDER, now, then, formCarColor, formLicenseNum, formCarModel, formCurrentLocation))
        else:
            #formPhoneNumber = int(formPhoneNumber)
            cursor.execute(sqlCommand, (formFirstName, formLastName, formEmail, formPhoneNumber, hashedPassword, randString, DRIVERORRIDER, now, then, formCarColor, formLicenseNum, formCarModel, formCurrentLocation))

        conn.commit()
        cursor.close()
        conn.close()

        ##this is here just for now.
        checkUnregisteredUsers()
        
        #if signup successful, return to login page
        return """<html><body>Signup successful!!! Please confirm your email</body><html>""" + render_template("driverLogin.html")
    elif request.method == 'GET':
        return render_template("driverSignup.html")



    
#==========================================================================================================================================================================================#
#Rider Side


@app.route('/riderLogin', methods = ['POST', 'GET'])
def riderLogin():
    global DRIVERORRIDER, DRIVERID, RIDERID
    if request.method == 'POST':
        #fetch data from form
        formEmail = request.form.get("email")
        formPassword = request.form.get("password")
        
        #mysql part
        conn = pymysql.connect(user="root", passwd="Gyanisha@123", db="BookARide")
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlCommand = "select * from RegisteredUsers where email=%s and driverRider=%s LIMIT 1"
        findDriverID = "SELECT * FROM DriverInfo where registeredID=%s;"
        findRiderID = "SELECT * FROM RiderInfo where registeredID=%s;"
        cursor.execute(sqlCommand, (formEmail, DRIVERORRIDER))
        user = cursor.fetchone()
        print(DRIVERORRIDER)

        #if user does not exist anywhere
        if (user == None):
            #lets also check on the unregistered users if there is time
            sqlCommand = "select * from UnregisteredUsers where email=%s LIMIT 1;"
            cursor.execute(sqlCommand, (formEmail))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if (user != None and user['email'] == formEmail.lower()):
                return """<html><body>Email is not verified yet. Please verify your email from your gmail account.</body></html>""" + render_template("riderLogin.html")
            elif (user == None):
                return """<html><body><p>Email not found!!! Please sign up!</p></body></html>""" + render_template("riderLogin.html")
        
        #get hashedPassword and randomString to cross-check
        formPassword += user['randString']
        
        #need to hash the password and check against the stored one
        temp = hashlib.md5(formPassword.encode())
        formHashedPassword = temp.hexdigest()

        
        #fetch the homepage
        if (user != None and user['email'] == formEmail.lower() and user['hashedPassword'] == formHashedPassword):
            if (DRIVERORRIDER == "driver"):
                cursor.execute(findDriverID, user['id'])
                driver = cursor.fetchone()
                DRIVERID = driver['id']
            else:
                cursor.execute(findRiderID, user['id'])
                rider = cursor.fetchone()
                #print(user['id'], rider)
                RIDERID = rider['id']
        
            cursor.close()
            conn.close()
            return render_template("riderHomePage.html")
        elif (user != None and user['hashedPassword'] != formHashedPassword):
            cursor.close()
            conn.close()
            return """<html><body><p>Wrong Password!!!</p></body></html>""" + render_template("riderLogin.html")
        
    elif request.method == 'GET':
        return render_template("riderLogin.html")

    

@app.route('/riderSignup', methods=['POST', 'GET'])
def riderSignup():
    global DRIVERORRIDER
    if request.method == 'POST':
        #fetch data from form:
        formFirstName = request.form.get("firstName")
        formLastName = request.form.get("lastName")
        formEmail = request.form.get("email")
        formPhoneNumber = request.form.get("phoneNumber")
        formPassword = request.form.get("password1")
        

        #connect to sql
        conn = pymysql.connect(user="root", passwd="Gyanisha@123", db="BookARide")
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        #check if the email is already registered
        sqlCommand = "select * from RegisteredUsers where email=%s and driverRider=%s"
        cursor.execute(sqlCommand, (formEmail, DRIVERORRIDER))
        user = cursor.fetchone()
        if (user != None and user['driverRider'] == DRIVERORRIDER):
            conn.commit()
            cursor.close()
            conn.close()
            return "<html><body>Email already registered</body></head>" + render_template("riderLogin.html")

        #check if the email is in unregistered table
        sqlCommand = "select * from UnregisteredUsers where email=%s and driverRider=%s"
        cursor.execute(sqlCommand, (formEmail, DRIVERORRIDER))
        user = cursor.fetchone()
        if (user != None and user['driverRider'] == DRIVERORRIDER):
            conn.commit()
            cursor.close()
            conn.close()
            return "<html><body>Email already used. Check your email inbox for email verification</body></head>" + render_template("riderLogin.html")

        
        #if not registered then insert into the database
        if (formPhoneNumber == ""):
            sqlCommand = "INSERT INTO UnregisteredUsers (firstName, lastName, email, hashedPassword, randString, driverRider, timeNow, timeThen) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
        else:
            sqlCommand = "INSERT INTO UnregisteredUsers (firstName, lastName, email, phoneNumber, hashedPassword, randString, driverRider, timeNow, timeThen) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"

            
        #generate random string of random length
        randLength = randint(5, 15)
        randString = ""
        t = string.ascii_letters + string.digits
        for i in range(randLength):
            randString += random.choice(t)
        formPassword += randString

        #hash the password
        temp = hashlib.md5(formPassword.encode())
        hashedPassword = temp.hexdigest()

        #time for them to confirm their id
        now = datetime.datetime.now()
        then = now + datetime.timedelta(days = 0, hours = 0, minutes = 10, seconds = 1)

        if (formPhoneNumber == ""):
            cursor.execute(sqlCommand, (formFirstName, formLastName, formEmail, hashedPassword, randString, DRIVERORRIDER, now, then))
        else:
            #formPhoneNumber = int(formPhoneNumber)
            cursor.execute(sqlCommand, (formFirstName, formLastName, formEmail, formPhoneNumber, hashedPassword, randString, DRIVERORRIDER, now, then))

        conn.commit()
        cursor.close()
        conn.close()

        ##this is here just for now.
        checkUnregisteredUsers()
        
        #if signup successful, return to login page
        return """<html><body>Signup successful!!! Please confirm your email</body><html>""" + render_template("riderLogin.html")
    elif request.method == 'GET':
        return render_template("riderSignup.html")


@app.route('/riderHomePage', methods = ['POST', 'GET'])
def riderHomePage():
    pass


@app.route('/riderHomePage/findDrivers', methods = ['POST', 'GET'])
def findDrivers():
    global DRIVERORRIDER, FROMLOCATION, TOLOCATION
    if (request.method == "GET"):
        return """<html><body>Finding Driver for you!</body></html>""" + render_template("riderHomePage.html")
    elif (request.method == "POST"):
        button_clicked = request.form['findDrivers']
        fromLocation = request.form.get("from")
        toLocation = request.form.get("to")
        
        FROMLOCATION = fromLocation
        TOLOCATION = toLocation

        if (button_clicked == "Request Now"):
            #connect to sql
            conn = pymysql.connect(user="root", passwd="Gyanisha@123", db="BookARide")
            cursor = conn.cursor(pymysql.cursors.DictCursor)

            #find Drivers nearby
            sqlCommand = "select * from DriverInfo, (select * from RegisteredUsers where driverRider = 'driver') as T0 where DriverInfo.registeredID = T0.id"
            cursor.execute(sqlCommand)
            user = cursor.fetchall()
            #print("users from finddrivers: ", user);
            
            cursor.close()
            conn.close()
            #lets allow javascript to calculate the distance
            return render_template('searching.html', user=user, fromLocation=fromLocation, toLocation=toLocation)
        elif (button_clicked == "Schedule"):
            pass


    
@app.route('/riderHomePage/findDrivers/searching', methods = ['POST', 'GET'])
def searching():
    if (request.method == "GET"):
        render_template("searching.html")


@app.route('/riderHomePage/driverFound', methods = ['POST'])
def driverFound():
    global DRIVERID, DATE, TIME, COST, COSTWITHSEC
    if (request.method =="POST"):
        time = int(request.form.get("driverDist"))
        print("time: ", time)
        if (time > ALLOWEDTIME):
            return """<html><body><p>No drivers available at the range. Try again in few minutes.</p></body></html>""" + render_template("riderHomePage.html")
        
        driverId = request.form.get("driverId")
        destTime = int(request.form.get("timeToDest"))
        
        if (destTime > ALLOWEDTIME):
            return """<html><body><p>Travelling too far.</p></body></html>""" + render_template("riderHomePage.html")
        
        DRIVERID = driverId
        print("Driver found: ", DRIVERID, " " , driverId);
        t = datetime.datetime.now()
        TIME = t.strftime("%H:%M:%S")
        DATE = t.strftime("%Y-%m-%d")
        print(destTime, DATE, TIME, t)
        print(type(destTime))
        COST = 5.0 + float(destTime) * COSTWITHSEC

        conn = pymysql.connect(user="root", passwd="Gyanisha@123", db="BookARide")
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlcommand = "SELECT * FROM DriverInfo where id = %s;";
        print("DriverId from driverFound: ", DRIVERID)
        cursor.execute(sqlcommand, DRIVERID);
        user = cursor.fetchone();
        conn.close();
        cursor.close();

        if (user == None):
            return """<html><body><p>No driver available at the moment</p><p></p></body></html>""" + render_template("riderHomePage.html")
        
        name = user['firstName'] + " " + user['lastName'];
        location = user['location'];
        ridesCompleted = user['ridesCompleted'];
        review = user['review'];
        carColor = user['carColor'];
        licenseNumber = user['licenseNumber'];
        carModel = user['carModel'];

        return render_template("foundDriver.html", time=time, location=location, destTime=destTime, name=name, ridesCompleted=ridesCompleted, review=review, carColor=carColor, licenseNumber=licenseNumber, carModel=carModel, cost=COST)


    
@app.route('/riderHomePage/reviewed', methods = ['POST'])
def addToDatabase():
    global DRIVERID, RIDERID, FROMLOCATION, TOLOCATION, COST, RIDERSREVIEW, DATE, TIME
    if (request.method == "POST"):
        r = int(request.form.get("r"))

        driverInfo = "SELECT * FROM DriverInfo where id = %s;"
        riderInfo = "SELECT * FROM RiderInfo where id = %s;"

        updateDriver = "UPDATE DriverInfo SET ridesCompleted = %s, review = %s, sumOfReview = %s where id = %s;"
        updateRider = "UPDATE RiderInfo SET review = %s where id = %s;"
        updateRideHistory = "INSERT INTO RideHistory (riderId, date, time, driverId, fromLocation, toLocation, cost, ridersReview) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"


        #if being reviewed by the rider
        if (DRIVERORRIDER == "rider"):
            conn = pymysql.connect(user="root", passwd="Gyanisha@123", db="BookARide")
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(driverInfo, DRIVERID)
            driver = cursor.fetchone()
            #print("DRiver: ", driver, " driverID ", DRIVERID)
            ridesCompleted = driver['ridesCompleted'] + 1
            reviewSums = driver['sumOfReview']
            review = driver['review'] * reviewSums
            RIDERSREVIEW = r
            review = r + review
            reviewSums = reviewSums if (r == 0) else reviewSums + 1
            review = review  if (reviewSums == 0) else review // reviewSums
            cursor.execute(updateDriver, (ridesCompleted, review, reviewSums, DRIVERID));
            conn.commit();
            cursor.close();
            conn.close();

        
        if (DRIVERORRIDER == "driver"):
            conn = pymysql.connect(user="root", passwd="Gyanisha@123", db="BookARide")
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute(riderInfo, RIDERID)
            rider = cursor.fetchone()
            reviewSums = rider['sumOfReview']
            review = rider['review'] * reviewSums
            review = r + review
            reviewSums = reviewSums if (r == 0) else reviewSums + 1
            review = review if (reviewSums == 0) else review // reviewSums
            cursor.execute(updateRider, (review, RIDERID));
            conn.commit();
            cursor.close();
            conn.close();

        
        conn = pymysql.connect(user="root", passwd="Gyanisha@123", db="BookARide")
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        #print(RIDERID, DATE, TIME, DRIVERID, FROMLOCATION, TOLOCATION, COST, RIDERSREVIEW)
        print(RIDERID);
        cursor.execute(updateRideHistory, (RIDERID, DATE, TIME, DRIVERID, FROMLOCATION, TOLOCATION, COST, RIDERSREVIEW))
        conn.commit();
        cursor.close();
        conn.close();
        
        return render_template("riderHomePage.html")

    
def checkUnregisteredUsers():
    global DRIVERORRIDER, DRIVERLOCATION
    #we need to check if they registered
    conn = pymysql.connect(user="root", passwd="Gyanisha@123", db="BookARide")
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    #check if the email is already registered
    sqlCommand = "SELECT * FROM UnregisteredUsers"
    cursor.execute(sqlCommand)
    users = cursor.fetchall()
    sqlCommand = "DELETE FROM UnregisteredUsers"
    cursor.execute(sqlCommand)
    conn.commit()
    cursor.close()
    conn.close()

    registerUsers = "INSERT INTO RegisteredUsers (email, phoneNumber, hashedPassword, randString, driverRider) VALUES(%s, %s, %s, %s, %s);"
    getId = "SELECT id FROM RegisteredUsers where email=%s and driverRider=%s;"
    riderInfo = "INSERT INTO RiderInfo (registeredId, firstName, lastName, review, sumOfReview) VALUES(%s, %s, %s, %s, %s);"
    driverInfo = "INSERT INTO DriverInfo (registeredId, firstName, lastName, ridesCompleted, review, sumOfReview, active, location, carColor, licenseNumber, carModel) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    
    for user in users:
        conn = pymysql.connect(user="root", passwd="Gyanisha@123", db="BookARide")
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        
        #print(user['driverRider'])
        cursor.execute(registerUsers, (user['email'], user['phoneNumber'], user['hashedPassword'], user['randString'], user['driverRider']))
        cursor.execute(getId, (user['email'], user['driverRider']))
        userId = cursor.fetchone()
        
        if (user['driverRider'] == 'rider'):
            #print(userId)
            cursor.execute(riderInfo, (userId['id'], user['firstName'], user['lastName'], 0, 0))
        elif (user['driverRider'] == 'driver'):
            #print(type(str(userId['id'])), type(user['firstName']), type(user['lastName']), type(DRIVERLOCATION), type(user['carColor']), type(user['licenseNumber']), type(user['carModel']))
            #print("driver location: ", DRIVERLOCATION)
            cursor.execute(driverInfo, (userId['id'], user['firstName'], user['lastName'], 0, 0, 0, 1, DRIVERLOCATION, user['carColor'], user['licenseNumber'], user['carModel']))
        conn.commit()
        cursor.close()
        conn.close()
        
    return


#checkUnregisteredUsers()
