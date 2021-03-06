#!/usr/bin/env python
#coding: utf-8
import praw
import OAuth2Util
import json
import re
import os
import logging
import sys
import time
import pickle

class STOCKS:
	def __init__(self, subreddit):
		self.r = praw.Reddit("/r/BRSE stock automation by /u/b0wmz")
		self.path = os.path.realpath(__file__)
		self.path = self.path.replace(os.path.basename(__file__), "")
		self._o = OAuth2Util.OAuth2Util(self.r, configfile=self.path+"oauth.txt")

		self.subreddit = self.r.get_subreddit(subreddit)
		self.prices = {} #share prices
		self.credit = {} #users individual bagelance
		self.shares = {} #users individual shares
		self.margin = {}
		with open(self.path+"doneposts", "rb") as file:
			self.doneposts = pickle.load(file)

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

		try:
			self.currentpost = self.r.get_sticky(self.subreddit)
			self.log.info("Attempting to load ALL comments ...")
			self.currentpost.replace_more_comments()
			self.log.info("Loaded all comments successfully")
		except praw.errors.NotFound:
			self.log.critical("No sticky found, aborting.")
			exit()

	def getSharePrices(self):
		page = self.r.get_wiki_page(self.subreddit, "prices").content_md
		for idx,val in json.loads(page).iteritems():
			self.prices[idx] = val['Value']
		self.log.debug("Loaded share prices")

	def getUsersCredit(self):
		credit = json.loads(self.r.get_wiki_page(self.subreddit, "credit").content_md)
		for idx, val in credit.iteritems():
			self.credit[idx] = val["Balance"]
			self.margin[idx] = val["Margin"]
		self.log.debug("Loaded user credit")
		
	def getUserCredit(self, username):
		for idx, val in self.credit.iteritems():
			if idx == username:
				return val

	def getUserShares(self, username):
		for idx, val in self.shares.iteritems():
			if idx == username:
				return val

	def getTotalShares(self):
		self.shares = json.loads(self.r.get_wiki_page(self.subreddit, "shares").content_md)
		self.log.debug("Loaded user shares")

	def creditUserShare(self, username, seller, amount):
		try:
			if self.credit[username] - (amount*self.prices[seller]) < 0:
				return "nocash"
			if amount < 0:
				try:
					if abs(amount) > self.shares[username][seller]: #user actually has shares
						return "noshares"
				except KeyError:
					return "noshares"
			self.credit[username]-=amount*self.prices[seller]
			self.log.info("Removed total %d from account %s. Total now is %d. Individual price for share %s %d" % (amount*self.prices[seller], username, self.credit[username], seller, self.prices[seller]))
		except KeyError:
			removable = amount*self.prices[seller]
			if removable > 1000:
				self.log.error("%s doesn't have enough money to buy %d shares of %s" % (username, amount, seller))
				return "nocash"
			self.credit[username] = 1000-removable
			self.margin[username] = ""
			self.log.info("Created share account for %s and removed %d. Total is now %d. Individual price for share %s %d" % (username, amount, self.credit[username], seller, self.prices[seller]))
		return self.credit[username]


	def parseComments(self):
		try:
			for c in self.currentpost.comments:
				if c.id in self.doneposts:
					self.log.debug("Not checking post %s, since already checked" % c.id)
					continue
				if c.edited is True:
					self.log.debug("Post %s is edited, skipping" % c.id)
					self.doneposts.append(c.id)
					c.reply("Post is edited, ignoring.")
					continue
				action = c.body.split()
				if len(action) < 3:
					self.log.debug("Post %s doesn't have 3 parameters, skipping")
					self.doneposts.append(c.id)
					c.reply("Invalid amount of parameters")
					continue
				self.log.debug(c.body)

				if action[0].lower() != "buy" and action[0].lower() != "sell":
					self.log.info("Post isn't buy/sell post, ignoring %s" % c.id)
					self.doneposts.append(c.id)
					continue

				try:
					action[1] = action[1].upper()
					self.log.debug(self.prices[action[1]])
				except KeyError:
					reply = "Invalid Code %s" % action[1]
					self.log.error(reply)
					c.reply(reply)
					self.doneposts.append(c.id)
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
					try:
						int(remaining)
						self.addUserShares(str(c.author), action[1], action[2])
					except ValueError:
						self.log.info("Doesn't have something: %s" % c.id)
				elif action[0].lower() == "sell":
					remaining = self.creditUserShare(str(c.author), action[1], -action[2])
					try:
						int(remaining)
						self.addUserShares(str(c.author), action[1], -action[2])
					except ValueError:
						self.log.info("Doesn't have something: %s" % c.id)
				else:
					reply = "Invalid action %s. Valid actions are BUY and SELL." % action[0]
					self.log.error(reply)
					c.reply(reply)
					continue

				try:
					int(remaining)
					c.reply("Trade confirmed. **Balance %d cr.**" % remaining)
					self.doneposts.append(c.id)
				except ValueError:
					if remaining == "nocash":
						c.reply("You do not have enough money to make this trade.")
						self.doneposts.append(c.id)
						continue
					elif remaining == "noshares":
						c.reply("You do not have this many shares.")
						self.doneposts.append(c.id)
						continue
		except Exception, e:
			self.log.exception(e)

	# self.shares["example"] = {"ZUL": 5, "AME": 5}
	def addUserShares(self, username, share, amount):
		try: #user's share exists
			self.shares[username]
			self.log.debug("User's share exists %s" % username)
			try: #share exists
				self.shares[username][share]+=amount
				self.log.debug("Share %s exists in user %s" % (share, username))
				self.log.info("Added %d shares to %s's %s account" % (amount, username, share))
			except KeyError: #share doesn't exist
				self.shares[username][share] = amount
				self.log.debug("%s's account exists, created %s share" % (username, share))
				self.log.info("Added %d shares to %s's %s account" % (amount, username, share))
		except KeyError:
			self.shares[username] = {share: amount}
			self.log.debug("%s's account doesn't exist, created" % username)
			self.log.info("Added %d shares to %s's %s account" % (amount, username, share))


	def writeContent(self):
		self.r.edit_wiki_page(self.subreddit, "shares", json.dumps(self.shares), "Set new shares")
		credit = {}
		for idx,val in self.credit.iteritems():
			try:
				self.margin[idx]
			except KeyError:
				self.margin[idx] = None
			credit[idx] = {"Balance": val, "Margin": self.margin[idx]}
		self.r.edit_wiki_page(self.subreddit, "credit", json.dumps(credit), "Set new credit")

		with open(self.path+"doneposts", "wb") as file:
			pickle.dump(self.doneposts, file)

		self.log.debug("Saved everything")

	def main(self):
		self.getSharePrices()
		self.getUsersCredit()
		self.getTotalShares()
		self.parseComments()
		time.sleep(2)
		self.writeContent()

if __name__ == "__main__":
	s = STOCKS("")
	s.main()
