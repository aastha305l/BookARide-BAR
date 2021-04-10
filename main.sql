/*Name: Aastha Lamichhane
File: main.sql*/

create database BookARide
use database BookARide

create table registeredUsers (
id int not null AUTO_INCREMENT,
email VARCHAR(200) not null UNIQUE9
hashedPassword VARCHAR(200) not null,
PRIMARY KEY(id)
) engine = innodb;

/*
create table wallets (
id int not null AUTO_INCREMENT,
hashedCardNum VARCHAR(200) not null UNIQUE,
hashedCVV VARCHAR(100) not null UNIQUE,
hashedExpiry VARCHAR(200) not null, //may be not make this hashed
registeredID int,
PRIMARY KEY(id),
FOREIGN KEY(registeredID) references registeredUsers(id)
) engine = innodb;

create table unregisteredUsers (
id int not null AUTO_INCREMENT,
email VARCHAR(100) not null UNIQUE,
PRIMARY KEY(id),
) engine = innodb;



*/
