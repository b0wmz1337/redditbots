#!/usr/bin/env python	
#coding: utf-8
import praw
import OAuth2Util
import os
import re
import requests
import json
import pickle
from datetime import datetime

class CARDLIST():
	def __init__(self, file):
		try:
			with open(file, "rb") as cardFile:
				self.cards = pickle.load(cardFile)
		except (IOError, EOFError) as e:
			with open(file, "wb") as cardFile:
				pickle.dump([], cardFile)	
			self.cards = []

	def updateAll(self):
		for i in self.cards:
			i.update()

	def fetchAll(self):
		req = requests.get("http://netrunnerdb.com/api/cards/")
		js = json.loads(req.content)
		self.cards = []
		for i in js:
			self.cards.append(CARD(json.dumps(i)))

	def search(self, search):
		result = []
		for i in self.cards:
			if search.lower() in i.title.lower():
				result.append(i)
		return result

	def saveAll(self, file):
		with open(file, "wb") as cardFile:
			pickle.dump(self.cards, cardFile)

class CARD():
	def __init__(self, cardJson):
		self.assignValues(json.loads(cardJson))

	def update(self):
		try:
			req = requests.get("http://netrunnerdb.com/api/card/{}".format(self.code))
			cardJson = json.loads(req.content)
			self.assignValues(cardJson[0])
		except requests.exceptions.RequestException:
			#doshit
			pass

	def assignValues(self, dict):
		self.dict = dict
		self.lastmodified = datetime.strptime(self.dict['last-modified'], "%Y-%m-%dT%H:%M:%S+00:00")
		self.code = self.dict['code']
		self.title = self.dict['title']
		self.type = self.dict['type']
		self.typecode = self.dict['type_code']
		try:
			self.subtype = self.dict['subtype']
			self.subtypecode = self.dict['subtype_code']
		except KeyError:
			pass
		try:
			self.text = self.dict['text']
		except KeyError:
			pass
		try:
			self.baselink = self.dict['baselink']
		except KeyError:
			pass
		self.faction = self.dict['faction']
		self.factioncode = self.dict['faction_code']
		self.factionletter = self.dict['faction_letter']
		try:
			self.flavor = self.dict['flavor']
		except KeyError:
			pass
		try:
			self.illustrator = self.dict['illustrator']
		except KeyError:
			pass
		try:
			self.influencelimit = self.dict['influencelimit']
		except KeyError:
			pass
		try:
			self.minimumdecksize = self.dict['minimumdecksize']
		except KeyError:
			pass
		self.number = self.dict['number']
		self.quantity = self.dict['quantity']
		self.setname =  self.dict['setname']
		self.setcode = self.dict['set_code']
		self.side = self.dict['side']
		self.sidecode = self.dict['side_code']
		self.uniqueness = bool(self.dict['uniqueness'])
		self.limited = bool(self.dict['limited'])
		self.cyclenumber = self.dict['cyclenumber']
		self.ancurLink = self.dict['ancurLink']
		self.url = self.dict['url']
		self.img = self.dict['imagesrc']

class NETRUNNER():
	def __init__(self, subreddit, clist):
		self.path = os.path.realpath(__file__)
		self.path = self.path.replace(os.path.basename(__file__), "")
		self.r = praw.Reddit("Netrunner Card Fetcher v0.1 by /u/b0wmz")
		self._o = OAuth2Util.OAuth2Util(self.r, configfile=self.path+"oauth.txt")
		self.me = str(self.r.get_me())
		self.subreddit = self.r.get_subreddit(subreddit)
		self.bodyreg = re.compile(r"\[\[([)\w :&.\-'\"]+)\]\]")
		self.cardslist = CARDLIST(clist)
		self.comment = """[{0}](http://netrunnerdb.com{1}) - [NetrunnerDB]({2}), [ANCUR]({3})  
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

	def save(self):
		with open("doneposts", "wb") as file:
			pickle.dump(self.doneposts, file)

	def parseComment(self, c):
		try:
			if c.id in self.doneposts or str(c.author) == self.me:
				return
		except praw.errors.NotFound:
			return
		if not c.body:
			self.doneposts.append(c.id)
			return
		cb = self.checkBody(c.body)
		if cb is not None:
			comment = "I couldn't find any cards :(."
			for idx,cardl in enumerate(cb):
				result = self.cardslist.search(cardl)
				if not result:
					comment = ("" if idx == 0 else comment) + "I couldn't find {} \n\n".format(cardl)
				else:
					if len(result) > 1:
						if idx == 0:
							comment = ""
						comment = comment + "I found multiple results for `{}`:\n\n".format(cardl)
					for thisisacard in result:
						# self.comment = """[{0}]({1}) - [NetrunnerDB]({2}), [ANCUR]({3})
						comment = ("" if (idx == 0 and len(result) == 1) else comment) + self.comment.format(thisisacard.title, thisisacard.img, thisisacard.url, thisisacard.ancurLink)
				if idx+1 == len(cb):
					comment = comment+self.footer
			com = c.reply(comment)
			self.doneposts.append(c.id)
			self.doneposts.append(com.id)
			self.save()

	def parseSelf(self, n):
		try:
			if n.id in self.doneposts or str(n.author) == self.me:
				return
		except praw.errors.NotFound:
			return
		if not n.selftext:
			self.doneposts.append(n.id)
			return
		cb = self.checkBody(n.selftext)
		if cb is not None:
			comment = "I couldn't find any cards :(."
			for idx,cardl in enumerate(cb):
				result = self.cardslist.search(cardl)
				if not result:
					comment = ("" if idx == 0 else comment) + "I couldn't find {} \n\n".format(cardl)
				else:
					if len(result) > 1:
						if idx == 0:
							comment = ""
						comment = comment + "I found multiple results for `{}`:\n\n".format(cardl)
					for thisisacard in result:
						# self.comment = """[{0}]({1}) - [NetrunnerDB]({2}), [ANCUR]({3})
						comment = ("" if (idx == 0 and len(result) == 1) else comment) + self.comment.format(thisisacard.title, thisisacard.img, thisisacard.url, thisisacard.ancurLink)
				if idx+1 == len(cb):
					comment = comment+self.footer
			com = n.add_comment(comment)
			self.doneposts.append(n.id)
			self.doneposts.append(com.id)
			self.save()

	def main(self):
		for c in self.subreddit.get_comments():
			print "comment"
			self.parseComment(c)
		for n in self.subreddit.get_new():
			print "text"
			self.parseSelf(n)

if __name__ == "__main__":
	u = NETRUNNER("testasdf35", "thiscontainsthecards")
	u.main()