from tumblpy import Tumblpy
import praw
import OAuth2Util
import os
import cPickle as pickle
import traceback

SUBREDDIT = "Showerthoughts"
TUMBLRBLOG = "example.tumblr.com"
KARMATHRESHOLD = 100
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_SECRET = ""

# gets current path for reddit oauth
path = os.path.realpath(__file__)
path = path.replace(os.path.basename(__file__), "")

try:
	with open(path+"doneposts", "rb") as file:
		doneposts = pickle.load(file)
except (IOError, EOFError) as e:
	with open(path+"doneposts", "wb") as file:
		pickle.dump([], file)
	doneposts = []

t = Tumblpy(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_SECRET)
r = praw.Reddit("/r/Showerthoughts Tumblr Reposter")
o = OAuth2Util.OAuth2Util(r, configfile=path+"oauth.txt")
sub = r.get_subreddit(SUBREDDIT)

def save():
	with open(path+"doneposts", "wb") as file:
		pickle.dump(doneposts, file)

def handle(submissionobject):
	if submissionobject.permalink in doneposts:
		return
	elif submissionobject.stickied:
		doneposts.append(submissionobject.permalink)
		return
	if submissionobject.ups < KARMATHRESHOLD:
		return
	result = t.post("post", blog_url=TUMBLRBLOG, params={"type": "text", "body": submissionobject.title, "source_url": submissionobject.permalink})
	try:
		print result['id']
		doneposts.append(submissionobject.permalink)
	except KeyError:
		print "Couldn't post to Tumblr, error: \n{}".format(traceback.format_exc())
	save()

for i in sub.get_hot():
	handle(i)