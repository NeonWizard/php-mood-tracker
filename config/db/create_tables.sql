BEGIN TRANSACTION;
CREATE TABLE "UserMood" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`date`	TEXT NOT NULL,
	`userId`	INTEGER NOT NULL,
	`moodId`	INTEGER NOT NULL
);
CREATE TABLE `User` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`firstName`	TEXT NOT NULL,
	`lastName`	TEXT NOT NULL,
	`username`	TEXT NOT NULL UNIQUE,
	`password`	TEXT NOT NULL,
	`email`	TEXT
);
CREATE TABLE `Mood` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT NOT NULL UNIQUE,
	`color`	TEXT NOT NULL,
	`description`	TEXT
);
COMMIT;