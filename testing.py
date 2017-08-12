# -*- coding: utf-8 -*-
from reward import *
import numpy as np
#Author:	Jinglong Du
#email:		jid020@ucsd.edu

# which user&query?
WhichOne = 0

#query?
keyword = "手机"
QueryList = 0

#similarity?

init = np.array([])
# READ IN DATA
try:
	files = open(str(WhichOne), "r")
	init = files.readline().split()
	init = [float(num) for num in init]
	print init
except Exception, e:
	pass

# get q value
if len(init) > 0:
	q = init
else:
	q = list(range(len(prod[QueryList])))


# sort order to print
orig = q[:]
q.sort();
OrderL = []

# find match
for i in xrange(len(q)):
	for j in xrange(len(q)):
		if q[i] == orig[j]:
			orig[j] = -100000
			OrderL.append(prod[QueryList][j]);
			break
OrderL.reverse()

# print
print "=============================="
print "== Customer:      ", WhichOne,    "    =="
print "=============================="
print "Rank     Original              New"
for x in xrange(len(OrderL)):
	print x+1, "      ", prod[QueryList][9-x], "     ", OrderL[x]