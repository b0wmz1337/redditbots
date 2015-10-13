# README

This script reposts posts from [/r/Showerthoughts](https://www.reddit.com/r/showerthoughts) with a configurable number of minimum upvotes to Tumblr.

## Requirements
* PRAW
* PRAW-OAuth2Util
* python-tumblpy

## Setup
1. Set up OAuth2Util for Reddit, see [OAuth2Util's GitHub repo](https://github.com/SmBe19/praw-OAuth2Util/blob/master/OAuth2Util/README.md)
2. Register an app on Tumblr [here](https://www.tumblr.com/oauth/apps)
3. Copy OAuth Consumer Key and Consumer Secret Key and paste them in [Tumblr's API console](https://api.tumblr.com/console/calls/user/info)
4. Copy OAuth token and OAuth secret from API console
5. Paste keys in `shower.py` accordingly