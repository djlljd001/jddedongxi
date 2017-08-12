# -*- coding: utf-8 -*-

from reward import *
import numpy as np


#Author:	Jinglong Du
#email:		jid020@ucsd.edu

#Since I already messed up the regular model, it looks not same to any model I know yet.
#It is based on Q-learning, but the function is changed.

#Global data

#gama is the iteration speed. which means how fast you want for each Iteration.
GAMA  = 0.1

# 模拟训练
IterationTime = 10
DecayRate = None



# which user?
UserID = 0

# which query?
keyword = "手机"

# # which user&query?
# UserID = 1


#the result product list?

# READ IN DATA

# READ IN QUERY
prods = None
try:
	files = open(str("Query/" + keyword + ".QL"), "r")
	prods = files.read().splitlines()
	files.close()
except Exception, e:
	print "DATA WARNING:	Failed in Finding/Reading in Query list."


# #if customer 0 and 1 is, lets assume,  >95% similarity
# similar = 0.01

# init = None
init = np.array([])

# # READ IN Q-Value if we have.
# try:
# 	files = open(str(UserID), "r")
# 	init = files.readline().split()
# 	init = [float(num) for num in init]
# 	#print init
# except Exception, e:
# 	pass

# READ IN Q-Value if we have.
try:
	name = "model/" +str(UserID) + "&" + keyword + ".Mod"
	files = open(name, "r")
	init = files.readline().split()
	init = [float(num) for num in init]
	print init
except Exception, e:
	print "DATA WARNING:	Failed in 69"


#the CORE function that calculate the Q-value.
def func(r, maxQ, q):
	# if not linked to other S1S, then maxQ won't work
	# return q + Decay(1)*GAMA*(r + maxQ - q)
	return q + Decay(DecayRate, N_sa(0, 0))*GAMA*(r - q)


# get q value
if len(init) > 0:
	q = init
else:
	q = list(reversed(range(len(prods))))


# implement iteration
print "Iterating:"
z = IterationTime/100.0
a = 0
Rew = GetReward(UserID, keyword, len(prods))
theMaxQ = max(q)
for i in xrange(IterationTime):
	# print "\nThe " , i+1 , " Round: "
	if i/z > a + 1:
		a = int(i/z)
		print a , "%"
	#for each data set:
	for k in xrange(len(q)):
		q[k] = func(Rew[k], theMaxQ, q[k])
		# print k+1, ": " , q[k]


#SAVE
name = "model/" +str(UserID) + "&" + keyword + ".Mod"
files = open( name , "w")
for x in xrange(len(q)):
	files.write(str(q[x]))
	files.write(" ")
files.close()


# sort order to print
orig = q[:]
q.sort();
OrderL = [];

# find match
for i in xrange(len(q)):
	for j in xrange(len(q)):
		if q[i] == orig[j]:
			orig[j] = -100000
			OrderL.append(prods[j]);
			break
OrderL.reverse()

print "=============================="
print "== Customer:      ", UserID, "       =="
print "== keyword:       ", keyword, "    =="
print "=============================="
print "Rank     Original              New"
for x in xrange(len(OrderL)):
	print x+1, "      ", prods[x], "     ", OrderL[x]