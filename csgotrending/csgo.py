#!/usr/bin/env python
#coding:utf-8
from BeautifulSoup import BeautifulSoup
import requests
import re
import praw
from random import choice
import OAuth2Util
import os

r = praw.Reddit("CS:GO trending workshop skins poster for /r/CSGOArmory")
o = OAuth2Util.OAuth2Util(r, os.getcwd()+ "/oauth.txt")

t = requests.get("https://steamcommunity.com/workshop/browse/?appid=730&browsesort=trend&section=mtxitems")
soup = BeautifulSoup(t.content)
items = soup.findAll("div", {"class": re.compile("workshopItem \w")})

item = choice(items)
r.submit(subreddit="CSGOArmory", title=item.find("div", {"class": "workshopItemTitle ellipsis"}).text, url=item.find("a")["href"], resubmit=False)
