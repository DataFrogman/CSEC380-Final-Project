DROP DATABASE IF EXISTS db;
CREATE DATABASE db;
USE db;

DROP TABLE IF EXISTS users;
CREATE TABLE users(
	UserID INTEGER NOT NULL AUTO_INCREMENT,
	Username VARCHAR(30) NOT NULL,
	Password VARCHAR(128) NOT NULL,
	TotalVideos INTEGER,
	DateCreated DATE,
	Email VARCHAR(50),
	CONSTRAINT users_pk PRIMARY KEY(UserID)
);
