#!/usr/bin/env python	
#coding: utf-8
import praw
import OAuth2Util
import requests
import os
import re
import pickle
from BeautifulSoup import BeautifulSoup

class NETRUNNER():
	def __init__(self, subreddit):
		self.subreddit = subreddit
		self.path = os.path.realpath(__file__)
		self.path = self.path.replace(os.path.basename(__file__), "")
		self.r = praw.Reddit("Netrunner Cardbot")
		self._o = OAuth2Util.OAuth2Util(self.r, configfile=self.path+"oauth.txt")
		self.bodyreg = re.compile(r"\[\[([)\w ]+)\]\]")
		self.urlreg = re.compile(r"http:\/\/netrunnerdb.com\/en\/card\/(\d+)")
		self.comment = """[{0}](http://netrunnerdb.com/bundles/netrunnerdbcards/images/cards/en/{1}.png) - [NetrunnerDB](http://netrunnerdb.com/en/card/{1}), [ANCUR](http://ancur.wikia.com/wiki/{2})"""
		self.footer = """
___
[[Contact]](/message/compose/?to=b0wmz&subject=NetrunnerBot) [[Source]](https://github.com/b0wmz1337/redditbots/tree/master/netrunnerbot)"""

		with open("doneposts", "rb") as file:
			self.doneposts = pickle.load(file)

	def checkBody(self, body): # checks for something like [[*]]
		reg = self.bodyreg.search(body)
		if reg is None:
			return None
		return reg.group(1)

	def searchNDB(self, query): # checks if nrdb has entry
		query = query.replace(" ", "+")
		req = requests.get("http://netrunnerdb.com/find/?q="+query)
		if "Your query didn't match any card." in req.text:
			return None
		soup = BeautifulSoup(req.content)
		cardid = self.urlreg.search(soup.find("a", {"class": "card-title"})['href'])
		return cardid.group(1)

	def save(self):
		with open("doneposts", "wb") as file:
			pickle.dump(self.doneposts, file)

	def main(self):
		for c in self.r.get_subreddit(self.subreddit).get_comments():
			if c.id in self.doneposts:
				continue

			cb = self.checkBody(c.body)
			if cb is not None:
				cid = self.searchNDB(cb)
				if cid is None:
					c.reply("I couldn't find that card."+self.footer)
					self.doneposts.append(c.id)
					continue
				comment = self.comment.format(cb, cid, cb.replace(" ", "_"))+self.footer
				c.reply(comment)
				self.doneposts.append(c.id)
		self.save()