#!/usr/bin/env python
import sqlite3
db = sqlite3.connect("flaircount.db")
c = db.cursor()
c.execute("CREATE TABLE `submissions` (subid varchar(20) NOT NULL)")
db.commit()
db.close()
print "Updated database"