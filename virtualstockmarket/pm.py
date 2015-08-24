#!/usr/bin/env python
#coding: utf-8
import share

s = share.STOCKS("testasdf35")
s.getTotalShares()
s.getUserShares("b0wmz")

# messages = s.r.get_messages()
messages = s.r.get_unread()
for m in messages:
	if m.body.lower() == "list":
		message = ["%s, your current shares are as follows:\n\n" % str(m.author)]
		shares = s.getUserShares(str(m.author))
		if shares is None:
			message = "%s, you have no shares." % str(m.author)
		else:
			for idx, val in shares.iteritems():
				message.append("%s: %s  \n" % (idx, val))
		s.log.debug(''.join(message))
		m.reply(''.join(message))