# -*- coding: utf-8 -*-

from reward import *
import numpy as np
from numba import vectorize, float32, int32, jit
import time


#Author:	Jinglong Du
#email:		jid020@ucsd.edu

#Since I already messed up the regular model, it looks not same to any model I know yet.
#It is based on Q-learning, but the function is changed.

#Global data

WANNApercentage = True

#gama is the iteration speed. which means how fast you want for each Iteration.
GAMA  = 0.1

# 模拟训练
IterationTime = 100000000
DecayRate = None


# which user?
UserID = 0

# which query?
keyword = "手机"


################ READ IN DATA ###############

# READ IN QUERY
prods = None
try:
	files = open(str("Query/" + keyword + ".QL"), "r")
	prods = files.read().splitlines()
	files.close()
except Exception, e:
	print "DATA WARNING:	Failed in Finding/Reading in Query name slist."

init = np.array([])


# READ IN Q-Value if we have.
try:
	name = "model/" +str(UserID) + "&" + keyword + ".Mod"
	files = open(name, "r")
	init = np.array(files.readline().split())
	# init = [float(num) for num in init]
	init = init.astype(np.float32)
	print init
except Exception, e:
	print "DATA WARNING:	Failed to READ IN Q-Value"


#the CORE function that calculate the Q-value.
# def func(r, maxQ, q):
# 	# if not linked to other S1S, then maxQ won't work
# 	# return q + Decay(1)*GAMA*(r + maxQ - q)
# 	return q + Decay(DecayRate, N_sa(0, 0))*GAMA*(r - q)

# def func(r, maxQ, q, GAMA):
# @jit
@vectorize([float32(float32, float32)], target='cpu')
def func(r, q):
	# return q + Decay(DecayRate, N_sa(0, 0)) * GAMA * (r - q)
	# return q + GAMA * (r - q)
	return q + GAMA*(r - q)


# get q value
if init.size > 0:
	q = init
else:
	q = np.array(list(reversed(range(len(prods)))), dtype=np.float32)


# implement iteration
print "Iteration time: ", IterationTime
print "Iterating:"


if WANNApercentage:
	#================= percentage ========
	z = IterationTime/100.0 		#=====
	a = 0 							#=====
	#================= percentage ========



Rew = GetReward(UserID, keyword, len(prods))
theMaxQ = max(q)

print "Rew:" , Rew.dtype
print "q:  ", q.dtype

#start counting the total time
start_time = time.time()
for i in xrange(IterationTime):
	if WANNApercentage:
		#================= percentage ========
		if i/z > a + 1:					#=====
			a = int(i/z)				#=====
			print a , "%"				#=====
		#================= percentage ========


	#for each data set:
	# for k in xrange(len(q)):
	# 	q[k] = func(Rew[k], theMaxQ, q[k])
	# q = func(Rew, theMaxQ, q, GAMA)

	q = func(Rew, q)

		# print k+1, ": " , q[k]

#SAVE
name = "model/" +str(UserID) + "&" + keyword + ".Mod"
files = open( name , "w")
for x in xrange(len(q)):
	files.write(str(q[x]))
	files.write(" ")
files.close()


# sort order to print
orig = np.copy(q)
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

print("--- %s seconds ---" % (time.time() - start_time))