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
def R_S(s2s):
	return proR[s2s]


#this part will generate the initial value for Q. 
def initQ(s1s, a, rank):
	return 0

def purchaseModel(purc):
	reward = [0]*len(purc)
	for x in xrange(len(purc)):
		if purc[x] < 1:
			reward[x] = 0
		elif purc[x] < 2:
			reward[x] = -1
		elif purc[x] < 5:
			reward[x] = 3
		elif purc[x] < 20:
			reward[x] = 8
		else:
			reward[x] = 20
	return reward


def clickModel(click):
	minClick = min(click)
	newClick = [0]*len(click)
	newClick[:] = [x - minClick for x in click]
	maxClick = max(newClick)
	reward = [0]*len(click)
	for x in xrange(len(click)):
		if click[x] <= 0:
			reward[x] = 0
		elif click[x] <= maxClick/16:
			reward[x] = 1
		elif click[x] <= maxClick/8:
			reward[x] = 1.5
		elif click[x] <= maxClick/4:
			reward[x] = 2
		elif click[x] <= maxClick/2:
			reward[x] = 3
		elif click[x] <= maxClick:
			reward[x] = 4
		else:
			reward[x] = 5
	return reward


def wishListModel(wiL):
	reward = [0]*len(wiL)
	for x in xrange(len(wiL)):
		if wiL[x] <= 0:
			reward[x] = 0
		elif wiL[x] <= 1:
			reward[x] = 3
		elif wiL[x] <= 2:
			reward[x] = 4
		elif wiL[x] <= 4:
			reward[x] = 5
		else:
			reward[x] = 6
	return reward


#The R[s1s, a] function, which corresponding to the target customers, key words and products.
#No data yet, so set to 0 first.


#with GPU, do that:
#@vectorize(['float32(float32, float32)'], target='cuda')
def GetReward(num, ProductList):
	# with GPU, just do:
	# return x + y + z + u
	return [x+y+z+u for x,y,z,u in zip(purchaseModel(purchase[num]),clickModel(click[num]),wishListModel(wishList[num]),R_S(ProductList))]



# with GPU, need to change the form to:

pur0 = [ 1, 0, 0, 0, 2, 0, 3, 0, 0, 0]
pur1 = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


cli0 = [10, 1, 3, 5, 2, 8,39, 2, 1, 1]
cli1 = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


WiL0 = [ 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
WiL1 = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


proR0= [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
proR1= [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


# search : 手机
prod0 = [ "小米 5         ",
          "华为 p10       ",
          "iphone 7       ",
          "魅族 MX5       ",
          "红米 note 3    ",
          "三星 S8        ",
          "一加 5         ",
          "Oppo R11       ",
          "VIVO Xplay 5   ",
          "Nokia 3310     "]


# search : 小米
prod1 = [ "小米 MIX       ",
          "小米 5s        ",
          "小米 6         ",
          "红米 note 2    ",
          "红米 note 3    ",
          "小米 MAX 2     ",
          "小米笔记本 13.3 ",
          "小米电视 4A     ",
          "小米盒子 3 pro  ",
          "小米盒子 3 mini "]



prod = [prod0, prod1]
proR = [proR0, proR1]


purchase = [pur0, pur1]
click = [cli0, cli1]
wishList = [WiL0, WiL1]