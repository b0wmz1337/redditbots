#!/usr/bin/env python
#coding: utf-8
import praw
import OAuth2Util
import sqlite3
import os
import re

class COUNT():
	def __init__(self, subreddit):
		path = os.path.realpath(__file__)
		path = path.replace(os.path.basename(__file__), "")

		self.r = praw.Reddit("Flair Counter for /r/HWYA") #new reddit connection
		self.o = OAuth2Util.OAuth2Util(self.r, configfile=path+"oauth.txt") #authenticates via OAuth
		self.subreddit = subreddit

		self.db = sqlite3.connect('flaircount.db') #connects to database
		self.c = self.db.cursor() #creates a cursor object, which we will use to modify stuff in the db

	def getUserCount(self, user):
		self.c.execute("SELECT count FROM users WHERE username = ?", (str(user),))
		return self.c.fetchone()[0]

	def parseNewComments(self):
		com = self.r.get_comments(self.subreddit) #gets the newest comments
		
		for c in com:
			self.c.execute("SELECT * FROM submissions WHERE subid = ?", (c.submission.id,))
			if len(self.c.fetchall()) > 0: #checks if thread was already parsed
				continue

			self.c.execute('SELECT * FROM posts WHERE postid = ?', (c.id,))

			if len(self.c.fetchall()) > 0: #checks if comment was already parsed
				continue #skips this comment, if already parsed
			c.body.strip() #remove leading and trailing spaces
			if c.body[0:3] == u"☆☆☆" and c.author == c.submission.author: #checks if the first three characters are stars and if the comment is by the op
				count = c.body.count(u"☆")
				parent = self.r.get_info(thing_id=c.parent_id)

				self.c.execute('SELECT * FROM users WHERE username = ?', (str(parent.author),))
				if len(self.c.fetchall()) <= 0: #user hasn't commented ever before
					self.c.execute("INSERT INTO users (username, count) VALUES (?, 1)", (str(parent.author),))
					print "Inserted one"
				else:
					self.c.execute("UPDATE users SET count = count + 1 WHERE username = ?", (str(parent.author),))
					print "Added one"
				self.c.execute("INSERT INTO posts (postid) VALUES (?)", (c.id,)) #mark post as read
				self.c.execute("INSERT INTO submissions (subid) VALUES (?)", (c.submission.id,)) #mark submission as read
				customflair = self.r.get_flair(self.subreddit, parent.author)["flair_text"]
				reg = re.match(ur"\d ☆☆☆ (.*)", customflair, flags=re.UNICODE)
				if reg is not None:
					self.r.set_flair(self.subreddit, parent.author, u"%s ☆☆☆ %s" % (self.getUserCount(parent.author), reg.group(1)))
				else:
					if u"☆" in customflair:
						self.r.set_flair(self.subreddit, parent.author, u"%s ☆☆☆	" % self.getUserCount(parent.author))
					else:
						self.r.set_flair(self.subreddit, parent.author, u"%s ☆☆☆	%s" % (self.getUserCount(parent.author), customflair))
				self.db.commit() #write to database



if __name__ == "__main__":
	c = COUNT("HWYA")
	c.parseNewComments()
	# c.c.execute("DELETE FROM posts") #uncomment to truncate database
	# c.c.execute("DELETE FROM users")
