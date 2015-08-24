#!/usr/bin/env python
#coding:utf-8
import praw
import OAuth2Util
from datetime import datetime
import os

SUBREDDIT = "Pichumains"

r = praw.Reddit("Header changer based on time for /r/" % SUBREDDIT)
# r.login("username", "password")
path = os.path.realpath(__file__)
path = path.replace(os.path.basename(__file__), "")
OAuth2Util.OAuth2Util(r, path+"oauth2.txt")

hour = datetime.now()

r.upload_image(SUBREDDIT, hour.strftime("%A").lower()+".png", header=True)
