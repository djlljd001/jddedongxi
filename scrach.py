#-*- coding: utf-8 -*-
#Author:	Jinglong Du
#email:		jid020@ucsd.edu


# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))

from reward import *
import numpy as np
from numba import vectorize, float32, jit
import time
import io
import os


#   total:      [userID: Data, userID: Data...]
#   Data:       [NewQuery, QValue, RewardValue]
#   NewQuery:   [keyword: [int SKU, int SKU...],      keyword:  [int SKU, int SKU...], ... ]
#   QValue:     [keyword: [float32 Q, float32 Q...],  keyword:  [float32 Q, float32 Q...], ... ]
#   RewardValue:[keyword: [float32 R, float32 R...],  keyword:  [float32 R, float32 R...], ... ]

@vectorize([float32(float32, float32)], target='cpu')
def CoreFunc(r, q):
    # return q + Decay(DecayRate, N_sa(0, 0)) * GAMA * (r - q)
    # return q + GAMA * (r - q)
    return (1 - GAMA) * q + GAMA * r


def formatdata(UserNameID):
    # (keyword : [ 10, 9, 8, 7...])
    # Just try what's going on there.
    # the temporary dictionary for that person for that kind of data.
    global start_time
    global accTime

    # list of (keyword, [])
    userData = importUserData(UserNameID)
    WishListDict = importWLData(UserNameID)
    ShoppingCartDict = importShoppingData(UserNameID)
    # about 9 seccond

    if WishListDict == None:
        global wlmiss
        wlmiss = wlmiss + 1

    if ShoppingCartDict == None:
        global shpmiss
        shpmiss = shpmiss + 1

    # (productSKU, number)
    ClickDict = getClickDict(userData)
    PurchaseDict = getPurchaseDict(userData)
    # about 10 seccond

    # (keyword, [sku, sku, sku ...])
    NewQuery = FormatQuery(userData)
    # print "lens of NewQuery:" , len(NewQuery)
    # about 20 seconds

    ret = {}
    for each in NewQuery.items():
        # return [userID] = [ [sku, sku ...], [float Q, float Q, ...], [Reward R, reward R, ...] ]
        ret[each[0]] = [each[1], np.flip(np.arange(len(each[1]), dtype=np.float32), 0),
                        GetReward(each[1], ClickDict, PurchaseDict, WishListDict, ShoppingCartDict)]

    # about 10 seccods
    # return [NewQuery,QValue, RewardValue]
    return ret

# ==================================================================================================
GAMA = 0.5

# init path for Basic info and query and click and purchase data.
path = 'UserData/'
total = []
i = 0
# ================= percentage ========
z = len(os.listdir(path))/100.0 # =====
a = 0                           # =====
# ================= percentage ========

wlmiss = 0
shpmiss = 0


start_time = time.time()
accTime = 0.0
total = {}

# Import all data into the dictionary total.
print "Start importing data and generating initial models."
for filename in os.listdir(path):
    # ================= percentage ========
    if i / z > a + 1:               # =====
        a = int(i / z)              # =====
        print a, "%"                # =====
    # ================= percentage ========
    data = formatdata(filename)
    total[filename] = data
    i = i+1


for each in total.items():
    print each[0], " ==> ", each[1]
    break

print "wishlist miss: ", wlmiss
print "shopping cart miss: ", shpmiss
print "total: ", len(total)

print("--- %s seconds ---" % (time.time() - start_time))
print("--- accumulative %s seconds ---" % accTime)
#Single thread, 1000 user data. cost 50s.
#8 threads, 8000 user data in total, cost 100s.
#8 threads with cuda, 8000 user data in total, cost 300s.

# Then start first Iteration for just one time with GAMA as followed.


print "Start first iterations for models."
start_time = time.time()
for data in total.items():
    for each in data[1].items():
        # print "========================================================"
        # print each[1][0]
        # print CoreFunc(each[1][2], each[1][1])
        # total[userID] [keyword/query][Q-value]
        total[data[0]][each[0]][1] = CoreFunc(each[1][2], each[1][1])
        # print total[data[0]][each[0]][1]
        # each = [sku[], InitQ[], Reward[]]
        #newQ = CoreFunc(each[2], each[1])

print("--- %s seconds ---" % (time.time() - start_time))
#
# @vectorize([float32(float32, float32)], target='cpu')
# def CoreFunc(r, q):
#     # return q + Decay(DecayRate, N_sa(0, 0)) * GAMA * (r - q)
#     # return q + GAMA * (r - q)
#     return (1 - GAMA) * q + GAMA * r


