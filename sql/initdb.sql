drop table weeks;
drop table words;
drop table tests;

CREATE TABLE IF NOT EXISTS weeks
(
id integer primary key autoincrement,
name VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS words
(
id integer primary key autoincrement,
name VARCHAR(100),
success boolean,
known boolean,
weekid integer,
FOREIGN KEY(weekid) REFERENCES weeks(id)
ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS tests
(
id integer primary key autoincrement,
number int,
weekid integer,
FOREIGN KEY(weekid) REFERENCES weeks(id)
ON DELETE CASCADE ON UPDATE CASCADE
);
