#!/usr/bin/env python
#coding: utf-8
import praw
import OAuth2Util
import os
import pickle

class NAMECHECK():
	def __init__(self, subreddit):
		self.path = os.path.realpath(__file__)
		self.path = self.path.replace(os.path.basename(__file__), "")
		self.r = praw.Reddit("/r/Username used name checker")
		self._o = OAuth2Util.OAuth2Util(self.r, configfile=self.path+"oauth.txt")
		self.subreddit = self.r.get_subreddit(subreddit)

	def parse(self):
		sub = self.subreddit.get_new()
		for i in sub:
			if i.link_flair_text == "Taken":
				continue

			if self.r.is_username_available(i.title):
				i.set_flair(flair_text="Taken", flair_css_class="Taken")

if __name__ == "__main__":
	n = NAMECHECK("Username")
	n.parse()