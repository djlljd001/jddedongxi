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
IterationTime = 476842
DecayRate = None


# which user&query?
WhichOne = 0


#query?
keyword = "手机"
#the result product list?
QueryList = 0

# #if customer 0 and 1 is, lets assume,  >95% similarity
# similar = 0.01

# init = None
init = np.array([])

# READ IN DATA
try:
	files = open(str(WhichOne), "r")
	init = files.readline().split()
	init = [float(num) for num in init]
	#print init
except Exception, e:
	pass

#the CORE function that calculate the Q-value.
def func(r, maxQ, q):
	# if not linked to other S1S, then maxQ won't work
	# return q + Decay(1)*GAMA*(r + maxQ - q)
	return q + Decay(DecayRate, N_sa(0, 0))*GAMA*(r - q)

# get q value
if len(init) > 0:
	q = init
else:
	q = list(range(10))

# implement iteration
print "Iterating:"
z = IterationTime/100
a = 0
for i in xrange(IterationTime):
	# print "\nThe " , i+1 , " Round: "
	if i/z > a:
		a = i/z
		print a , "%"
	theMaxQ = max(q)
	#for each data set:
	Rew = GetReward(WhichOne, 0)

	for k in xrange(len(q)):
		q[k] = func(Rew[k], theMaxQ, q[k])
		# print k+1, ": " , q[k]


#SAVE
files = open(str(WhichOne), "w")
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
			OrderL.append(prod[WhichOne][j]);
			break
OrderL.reverse()

print "=============================="
print "== Customer:      ", WhichOne, "    =="
print "=============================="
print "Rank     Original              New"
for x in xrange(len(OrderL)):
	print x+1, "      ", prod[WhichOne][9-x], "     ", OrderL[x]