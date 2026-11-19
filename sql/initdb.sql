drop table weeks;
drop table words;
drop table tests;

CREATE TABLE IF NOT EXISTS weeks
(
id integer primary key autoincrement,
name VARCHAR(100)
total integer,
known integer
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


drop TRIGGER update_total_words;
CREATE TRIGGER IF NOT EXISTS update_total_words
AFTER insert
   ON words
BEGIN
update weeks set total=(select count(*) from words where weekid=new.weekid) where weeks.id=new.weekid;
end;


drop TRIGGER update_total_words_known;
CREATE TRIGGER IF NOT EXISTS update_total_words_known
AFTER update
   ON words
BEGIN
update weeks set known=(select count(*) from words where weekid=new.weekid and success=true) where weeks.id=new.weekid;
end;
