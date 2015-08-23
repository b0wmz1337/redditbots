#!/usr/bin/env python
#coding: utf-8
import praw
import OAuth2Util
import json
import re
import os
import logging
import sys

class STOCKS:
	def __init__(self, subreddit):
		self.r = praw.Reddit("/r/BRSE stock automation by /u/b0wmz")
		path = os.path.realpath(__file__)
		path = path.replace(os.path.basename(__file__), "")
		self._o = OAuth2Util.OAuth2Util(self.r, configfile=path+"oauth.txt")

		self.subreddit = self.r.get_subreddit(subreddit)
		self.prices = {}
		self.credit = []
		self.shares = []

		self.log = logging.getLogger("main")
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		ch = logging.StreamHandler(sys.stdout)
		ch.setLevel(logging.DEBUG)
		ch.setFormatter(formatter)
		self.log.addHandler(ch)
		fh = logging.FileHandler("share.log")
		fh.setLevel(logging.DEBUG)
		fh.setFormatter(formatter)
		self.log.addHandler(fh)
		self.log.setLevel(logging.DEBUG)

	def getSharePrices(self):
		post = self.subreddit.get_sticky()
		self.currentpost = post
		post = re.match(r".*?\|.*?\|.*?\|\n[--:]+\|[--:]+\|[--:]+\|(.*)", post.selftext, flags=re.DOTALL).group(1)
		post = post.replace("\n", "")
		post = post.split("|")
		del post[-1]
		for idx, val in enumerate(post[0::3],1): #probably a more pythonic/nicer way of doing this
			# self.prices.append([val, post[idx*3-1]])
			self.prices[val] = post[idx*3-1]
			print self.prices

	def getUsersCredit(self):
		self.credit = json.loads(self.r.get_wiki_page(self.subreddit, "credit").content_md)

	def getUsersShares(self):
		self.shares = json.loads(self.r.get_wiki_page(self.subreddit, "shares").content_md)

	def creditUserShare(self, username, seller, amount):
		try:
			self.credit[username]-=amount*self.prices[seller]
			self.log.info("Removed total %d from account %s. Total now is %d. Individual price for share %s %d" % (amount*self.prices[seller], username, self.credit[username], seller, self.prices[seller]))
		except IndexError:
			self.credit[username] = 1000-amount
			self.log.info("Created share account for %s and removed %d. Total is now %d. Individual price for share %s %d" % (username, amount, 1000-amount, seller, self.prices[seller]))
		return self.credit[username]


	def parseComments(self):
		try:
			for c in self.currentpost.comments:
				action = c.body.split()
				self.log.debug(c.body)

				try:
					self.log.debug(action[1])
				except IndexError:
					reply = "Invalid Code %s" % action[1]
					self.log.error(reply)
					c.reply(reply)
					continue

				try:
					action[2] = int(action[2])
				except ValueError:
					reply = "Invalid amount specified"
					self.log.error(reply)
					c.reply(reply)
					continue

				if action[0].lower() == "buy":
					remaining = self.creditUserShare(str(c.author), action[1], action[2])
				elif action[0].lower() == "sell":
					remaining = self.creditUserShare(str(c.author), action[1], -action[2])
				else:
					reply = "Invalid action %s. Valid actions are BUY and SELL." % action[0]
					self.log.error(reply)
					c.reply(reply)
					continue

				c.reply("Trade confirmed. **Balance %d cr.**" % remaining)
					
		except Exception, e:
			self.log.exception(e)

	def writeContent(self):
		self.r.edit_wiki_page(self.subreddit, "shares", json.dumps(self.shares), u"Set new shares")
		self.r.edit_wiki_page(self.subreddit, "credit", json.dumps(self.credit), u"Set new credit")

	def main(self):
		self.getSharePrices()
		self.getUsersShares()
		self.parseComments()
		self.writeContent()

if __name__ == "__main__":
	s = STOCKS("testasdf35")
	s.main()