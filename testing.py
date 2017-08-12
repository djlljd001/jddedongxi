# -*- coding: utf-8 -*-

# IMPORTANT: DO NOT MANIPULATE DATA HERE! READ ONLY.	 	


from reward import *
import numpy as np
#Author:	Jinglong Du
#email:		jid020@ucsd.edu

# which user?
UserID = 0

# which query?
keyword = "手机"

#similarity?

#init data
init = np.array([])
# READ IN DATA


# READ IN QUERY
prods = None
try:
	files = open(str("Query/" + keyword + ".QL"), "r")
	prods = files.read().splitlines()
	files.close()
except Exception, e:
	print "DATA WARNING:	Failed in Finding/Reading in Query list."




# READ IN Q-Value if we have.
try:
	name = "model/" +str(UserID) + "&" + keyword + ".Mod"
	files = open(name, "r")
	init = files.readline().split()
	init = [float(num) for num in init]
	files.close()
	print init
except Exception, e:
	print "DATA WARNING:	Failed reading in model data in 41"

# get q value
if len(init) > 0:
	q = init
else:
	q = list(reversed(range(len(prods))))


# sort order to print
orig = q[:]
q.sort();
OrderL = []

# find match
for i in xrange(len(q)):
	for j in xrange(len(q)):
		if q[i] == orig[j]:
			orig[j] = -100000
			OrderL.append(prods[j]);
			break
OrderL.reverse()

# print
print "=============================="
print "== Customer:      ", UserID, "       =="
print "== keyword:       ", keyword, "    =="
print "=============================="
print "Rank     Original              New"
for x in xrange(len(OrderL)):
	print x+1, "      ", prods[x], "     ", OrderL[x]