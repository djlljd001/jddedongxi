#-*- coding: utf-8 -*-

#Author:	Jinglong Du
#email:		jid020@ucsd.edu


# if need gpu, then do this:
#from numba import *
import numpy as np


#decay rate function based on N_SA(s, a) value, let's first assume it is 1,
#which means no decay for any N_SA value.
def Decay (DecayRate, N_SAValue):
	return 1


#The N_SA[s1s,a] function. No data yet, so set to default 1.
def N_sa(s1s, a):
	return 1


#The main function that will return the reward R[s'] for Step 2 State
#There is no data yet, so set to 0 first.
def R_S(keyword, lens):

	prodRZ = None
	prodRZName = "Query/" + keyword + ".QLR"
	try:
		files = open(prodRZName, "r")
		prodRZ = files.read().splitlines()
		files.close()
	except Exception, e:
		print "DATA WARNING:	Failed in Finding/Reading in product Reward AT 33"

	if prodRZ != None:
		return [int(x) for x in prodRZ]
	else:
		print "WARNING:	No product reward data AT 38"
		return [0]*lens


#this part will generate the initial value for Q. 
def initQ(s1s, a, rank):
	return 0


def purchaseModel(UserID, keyword, lens):
	purchR = None
	purchRName = "Data/purchase/" + str(UserID) + "&" + keyword + ".Hisdat"
	print "purchase address:       " , purchRName
	try:
		files = open(purchRName, "r")
		purchR = files.read().splitlines()
		files.close()
	except Exception, e:
		print "DATA WARNING:	Failed in Finding/Reading in purchase Reward. AT 58"

	if purchR != None:
		purchR = [int(x) for x in purchR]
		print "purchase data:          " , purchR
	else:
		print "WARNING:	No purchase reward. AT 64"
		purchR = [0]*lens

	reward = [0]*len(purchR)
	for x in xrange(len(purchR)):
		if purchR[x] < 1:
			reward[x] = 0
		elif purchR[x] < 2:
			reward[x] = -1
		elif purchR[x] < 5:
			reward[x] = 3
		elif purchR[x] < 20:
			reward[x] = 8
		else:
			reward[x] = 20
	return reward


def clickModel(UserID, keyword, lens):

	clkR = None
	clkRName = "Data/click/" + str(UserID) + "&" + keyword + ".Hisdat"
	print "click address:          " , clkRName
	try:
		files = open(clkRName, "r")
		clkR = files.read().splitlines()
		files.close()
	except Exception, e:
		print "DATA WARNING:	Failed in Finding/Reading in click Reward. AT 93"

	if clkR != None:
		clkR = [int(x) for x in clkR]
		print "click data:             ",  clkR
	else:
		print "WARNING:	No click reward. AT 99"
		clkR = [0]*lens

	minClick = min(clkR)
	print "minClick: " , min(clkR)
	newClick = [0]*len(clkR)
	newClick[:] = [x - minClick for x in clkR]
	maxClick = max(newClick)
	reward = [0]*len(clkR)
	for x in xrange(len(clkR)):
		if clkR[x] <= 0:
			reward[x] = 0
		elif clkR[x] <= maxClick/16:
			reward[x] = 1
		elif clkR[x] <= maxClick/8:
			reward[x] = 1.5
		elif clkR[x] <= maxClick/4:
			reward[x] = 2
		elif clkR[x] <= maxClick/2:
			reward[x] = 3
		elif clkR[x] <= maxClick:
			reward[x] = 4
		else:
			reward[x] = 5
	return reward


def wishListModel(UserID, keyword, lens):

	wiLiR = None
	wiLiRName = "Data/Cart&WishList/" + str(UserID) + "&" + keyword + ".Hisdat"
	print "Wishlist & Cart address:" , wiLiRName
	try:
		files = open(wiLiRName, "r")
		wiLiR = files.read().splitlines()
		files.close()
	except Exception, e:
		print "DATA WARNING:	Failed in Finding/Reading in wishList Reward. AT 133"

	if wiLiR != None:
		wiLiR = [int(x) for x in wiLiR]
		print "Wishlist & Cart data:   ",  wiLiR
	else:
		print "WARNING:	No wishList reward. AT 139"
		wiLiR = [None]*lens

	reward = [0]*len(wiLiR)
	for x in xrange(len(wiLiR)):
		if wiLiR[x] <= 0:
			reward[x] = 0
		elif wiLiR[x] <= 1:
			reward[x] = 3
		elif wiLiR[x] <= 2:
			reward[x] = 4
		elif wiLiR[x] <= 4:
			reward[x] = 5
		else:
			reward[x] = 6
	return reward


#The R[s1s, a] function, which corresponding to the target customers, key words and products.
#No data yet, so set to 0 first.

#with GPU, do that:
#@vectorize(['float32(float32, float32)'], target='cuda')
def GetReward(UserID, keyword, lens):
	# with GPU, just do:
	# return x + y + z + u
	ret = [x+y+z+u for x,y,z,u in zip(purchaseModel(UserID, keyword, lens), clickModel(UserID, keyword, lens), wishListModel(UserID, keyword, lens), R_S(keyword, lens))]
	print "Final reward func: " , ret
	return ret