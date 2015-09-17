#!/usr/bin/env python	
#coding: utf-8
import praw
import OAuth2Util
import requests
import os
import re
import pickle
import urllib
from BeautifulSoup import BeautifulSoup

class NETRUNNER():
	def __init__(self, subreddit):
		self.path = os.path.realpath(__file__)
		self.path = self.path.replace(os.path.basename(__file__), "")
		self.r = praw.Reddit("Netrunner Cardbot")
		self._o = OAuth2Util.OAuth2Util(self.r, configfile=self.path+"oauth.txt")
		self.me = self.r.get_me()
		self.subreddit = self.r.get_subreddit(subreddit)
		self.bodyreg = re.compile(r"\[\[([)\w ]+)\]\]")
		self.urlreg = re.compile(r"http:\/\/netrunnerdb.com\/en\/card\/(\d+)")
		self.comment = """[{0}](http://netrunnerdb.com/bundles/netrunnerdbcards/images/cards/en/{1}.png) - [NetrunnerDB](http://netrunnerdb.com/en/card/{1}), [ANCUR](http://ancur.wikia.com/wiki/{2})

"""
		self.footer = """
___
[[Contact]](/message/compose/?to=b0wmz&subject=NetrunnerBot) [[Source]](https://github.com/b0wmz1337/redditbots/tree/master/netrunnerbot)"""

		with open("doneposts", "rb") as file:
			self.doneposts = pickle.load(file)

	def checkBody(self, body): # checks for something like [[*]]
		reg = self.bodyreg.findall(body)
		if not reg:
			return None
		return reg

	def searchNDB(self, query): # checks if nrdb has entry
		query = urllib.quote_plus(query)
		req = requests.get("http://netrunnerdb.com/find/?q="+query)
		if "Your query didn't match any card." in req.text:
			return None
		soup = BeautifulSoup(req.content)
		try:
			cardid = self.urlreg.search(soup.find("a", {"class": re.compile("card-title( card-preview)?")})['href'])
		except TypeError:
			return None
		return cardid.group(1)

	def save(self):
		with open("doneposts", "wb") as file:
			pickle.dump(self.doneposts, file)

	def parseComment(self, c):
		if c.id in self.doneposts or c.author is self.me:
			return
		cb = self.checkBody(c.body)
		if cb is not None:
			comment = "I couldn't find any cards :(."
			for idx,card in enumerate(cb):
				cid = self.searchNDB(card)
				if cid is None:
					comment = ("" if idx == 0 else comment) + "I couldn't find {} \n\n".format(card)
				else:
					comment = ("" if idx == 0 else comment) + self.comment.format(card, cid, card.replace(" ", "_"))
				if idx+1 == len(cb):
					comment = comment+self.footer
			com = c.reply(comment)
			self.doneposts.append(c.id)
			self.doneposts.append(com.id)
			self.save()

	def parseSelf(self, n):
		if n.id in self.doneposts or n.author is self.me:
			return
		if not n.selftext:
			self.doneposts.append(n.id)
			return
		cb = self.checkBody(n.selftext)
		if cb is not None:
			comment = "I couldn't find any cards :(."
			for idx,card in enumerate(cb):
				cid = self.searchNDB(card)
				if cid is None:
					comment = ("" if idx == 0 else comment) + "I couldn't find {} \n\n".format(card)
				else:
					comment = ("" if idx == 0 else comment) + self.comment.format(card, cid, card.replace(" ", "_"))
				if idx+1 == len(cb):
					comment = comment+self.footer
			com = n.add_comment(comment)
			self.doneposts.append(n.id)
			self.doneposts.append(com.id)
			self.save()

	def main(self):
		for c in self.subreddit.get_comments():
			self.parseComment(c)
		for n in self.subreddit.get_new():
			self.parseSelf(n)