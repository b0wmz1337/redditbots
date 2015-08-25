#!/usr/bin/env python
#coding: utf-8
import requests
import json
import re

headers = {
	"User-Agent": "com.vine.iphone/1.0.3 (unknown, iPhone OS 6.1.0, iPhone, Scale/2.000000)",
	"accept-language": "en, sv, fr, de, ja, nl, it, es, pt, pt-PT, da, fi, nb, ko, zh-Hans, zh-Hant, ru, pl, tr, uk, ar, hr, cs, el, he, ro, sk, th, id, ms, en-GB, ca, hu, vi, en-us;q=0.8"
}

pl = {
	"username": "",
	"password": ""
}

r = requests.post("https://api.vineapp.com/users/authenticate", data=pl)
headers["vine-session-id"] = json.loads(r.content)["data"]["key"]

try: #https://stackoverflow.com/questions/13729638/how-can-i-filter-emoji-characters-from-my-input-so-i-can-save-in-mysql-5-5
	# UCS-4
	regex = re.compile(u'[\U00010000-\U0010ffff]')
except re.error:
	# UCS-2
	regex = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

r = requests.get("https://api.vineapp.com/timelines/popular", headers=headers)
for i in json.loads(r.content)["data"]["records"]:
	# print i["videoUrl"]
	r = requests.get(i["videoUrl"], headers=headers)
	i["description"] = regex.sub("", i["description"])
	i["description"] = i["description"].replace(" ", "_")
	i["description"] = i["description"].replace("/", "")
	with open(i["description"] +'.mp4', "wb") as f:
		f.write(r.content)