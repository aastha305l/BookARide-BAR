/*Name: Aastha Lamichhane
File: main.sql*/

DROP DATABASE BookARide;
CREATE DATABASE BookARide;
USE BookARide;

/*I need to create combined uniqueness so that email is linked
to driver and rider, such that if they use same email to create
driver and rider account it is allowed. Think about it
Check Occupation table. May be that works*/

/*DROP TABLE RegisteredUsers;*/

CREATE TABLE RegisteredUsers (
id INT NOT NULL AUTO_INCREMENT,
email VARCHAR(200) NOT NULL,
phoneNumber INT,
hashedPassword VARCHAR(500) NOT NULL,
randString VARCHAR(500) NOT NULL,
driverRider VARCHAR(100) NOT NULL,
PRIMARY KEY(id),
UNIQUE KEY(email, driverRider)
) ENGINE = INNODB;


CREATE TABLE RiderInfo (
id INT NOT NULL AUTO_INCREMENT,
registeredID INT,
firstName VARCHAR(200) NOT NULL,
lastName VARCHAR(200) NOT NULL,
review INT NOT NULL,
sumOfReview INT NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(registeredID) REFERENCES RegisteredUsers(id)
) ENGINE = INNODB;


CREATE TABLE DriverInfo (
id INT NOT NULL AUTO_INCREMENT,
registeredID INT,
firstName VARCHAR(200) NOT NULL,
lastName VARCHAR(200) NOT NULL,
ridesCompleted INT NOT NULL,
review INT NOT NULL,
sumOfReview INT NOT NULL,
active INT NOT NULL,
location VARCHAR(500) NOT NULL,
carColor VARCHAR(100) NOT NULL,
licenseNumber VARCHAR(500) NOT NULL,
carModel VARCHAR(100) NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY(registeredID) REFERENCES RegisteredUsers(id)
) ENGINE = INNODB;

/*
CREATE TABLE Wallets (
id INT NOT NULL AUTO_INCREMENT,
hashedCardNum VARCHAR(200) NOT NULL UNIQUE,
hashedCVV VARCHAR(100) NOT NULL UNIQUE,
hashedExpiry VARCHAR(200) NOT NULL, //may be not make this hashed
registeredID INT,
PRIMARY KEY(id),
FOREIGN KEY(registeredID) REFERENCES RegisteredUsers(id)
) ENGINE = INNODB;
*/

/*DROP TABLE UnregisteredUsers;*/

CREATE TABLE UnregisteredUsers (
id INT NOT NULL AUTO_INCREMENT,
firstName VARCHAR(200) NOT NULL,
lastName VARCHAR(200) NOT NULL,
email VARCHAR(100) NOT NULL,
phoneNumber INT,
hashedPassword VARCHAR(500) NOT NULL,
randString VARCHAR(500) NOT NULL,
driverRider VARCHAR(100) NOT NULL,
timeNow DATETIME NOT NULL,
timeThen DATETIME NOT NULL,
carColor VARCHAR(100),
licenseNumber VARCHAR(500),
carModel VARCHAR(100),
currentLocation VARCHAR(500),
PRIMARY KEY(id),
UNIQUE KEY(email, driverRider)
) ENGINE = INNODB;


CREATE TABLE RideHistory (
id INT NOT NULL AUTO_INCREMENT,
riderId INT NOT NULL,
date DATE NOT NULL,
time TIME NOT NULL,
driverId INT NOT NULL,
fromLocation VARCHAR(250) NOT NULL,
toLocation VARCHAR(250) NOT NULL,
cost INT NOT NULL,
ridersReview INT,
PRIMARY KEY(id),
FOREIGN KEY(riderId) references RiderInfo(id),
FOREIGN KEY(driverId) references DriverInfo(id)
) ENGINE = INNODB;


/*
INSERT STATEMENTS:
*/
/*
INSERT INTO RegisteredUsers (email, hashedPassword)
VALUES ("alamichhane1@cougars.ccis.edu", "1234");
*/
