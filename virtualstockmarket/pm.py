#!/usr/bin/env python
#coding: utf-8
import share

s = share.STOCKS("")

s.getTotalShares()
s.getUsersCredit()
messages = s.r.get_unread()
for m in messages:
	if m.body.lower() == "list":
		message = []
		shares = s.getUserShares(str(m.author))
		if shares is None:
			message.append("%s, you have no shares." % str(m.author))
		else:
			message.append("%s, your current shares are as follows:\n\n" % str(m.author))
			for idx, val in shares.iteritems():
				message.append("%s: %s  \n" % (idx, val))
		
		credit = s.getUserCredit(str(m.author))
		if credit is None:
			message.append("\n\nYou do not appear to have a credit account. Please comment at least once to get one set up")	
		else:
			message.append("\n\nYour credit balance is: %d" % credit)
		s.log.debug(''.join(message))
		m.reply(''.join(message))
