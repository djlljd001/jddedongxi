#-*- coding: utf-8 -*-
#Author:	Jinglong Du
#email:		jid020@ucsd.edu


# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))

from reward import *
import numpy as np
from numba import vectorize, float32, jit
import time
import base64
from datetime import datetime as dt
import os

wlmiss = 0
shpmiss = 0
GAMA = 0.5


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

def buildModel():
    # ==================================================================================================
    # init path for Basic info and query and click and purchase data.
    path = 'DispatchedData/UserDataJan/'
    i = 0
    # ================= percentage ========
    z = len(os.listdir(path))/100.0 # =====
    a = 0                           # =====
    # ================= percentage ========

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


    # for each in total.items():
    #     print each[0], " ==> ", each[1]
    #     break

    print "wishlist miss: ", wlmiss
    print "shopping cart miss: ", shpmiss
    print "total: ", len(total)

    print("--- %s seconds ---" % (time.time() - start_time))
    # print("--- accumulative %s seconds ---" % accTime)
    #Single thread, 1000 user data. cost 50s.
    #8 threads, 8000 user data in total, cost 100s.
    #8 threads with cuda, 8000 user data in total, cost 300s.

    # Then start first Iteration for just one time with GAMA as followed.
    print "Start first iterations for models."
    start_time = time.time()
    for data in total.items():
        for each in data[1].items():
            # each ==> [sku[], InitQ[], Reward[]]
            # print "========================================================"
            # # total[userID][keyword/query][Q-value]
            # print total[data[0]][each[0]][1]
            total[data[0]][each[0]][1] = CoreFunc(each[1][2], each[1][1])
            # print total[data[0]][each[0]][1]
    print("--- Last Iteration time: %s seconds ---" % (time.time() - start_time))
    return total

def formataaaadata(UserNameID):
    # (keyword : [ 10, 9, 8, 7...])
    # Just try what's going on there.
    # the temporary dictionary for that person for that kind of data.
    global start_time

    # list of (keyword, [])
    userData = importTestingUserData(UserNameID)
    PurchaseDict = getTestPurchaseDict(userData)
    # return [NewQuery,QValue, RewardValue]
    return PurchaseDict

def getTestData(total):
    # ==================================================================================================
    # init path for Basic info and query and click and purchase data.
    path = 'DispatchedData/UserDataJan/'

    TestTotal = {}
    # Import all data into the dictionary total.
    print "Start importing testing data."
    for filename in os.listdir(path):
        data = formataaaadata(filename)
        TestTotal[filename] = data


    # Way to use base64:
    # file_name_string = base64.urlsafe_b64encode("***$^%^(&&^$%&%*^(&*^?<>{}:>?<***")
    # print file_name_string
    # file_name_string = base64.urlsafe_b64decode(file_name_string)
    # print file_name_string
    # exit()

    # total[userID]
    # TestTotal[userID]
    result = []
    improve = []
    dropdown = []
    noChange = []

    notFound = 0
    totalData = 0
    for each in TestTotal.items():

        # each[0] is the filename, which represent userID
        # each[1] is the purchase history for this user that need to be tested.
        if len(each[1])>1:

            # print len(each[1])
            for SinglePurchase in each[1]:
                # print "============================="
                # print SinglePurchase
                totalData = totalData + 1
                TempData = None
                # [query, userid, sessionid, productid, rank, time, click, purchase
                try:
                    # all the data needed here from total.
                    TempData = total[each[0]][SinglePurchase[0]]
                except Exception, e:
                    # print " Not found userID:", each[0], " and query:", SinglePurchase[0]
                    notFound = notFound + 1


                # the product ID that purchased.
                TempProductID = int(SinglePurchase[3])
                # the old position that in the search list
                TempOldProductPosition = int(SinglePurchase[4])
                # if product found here

                if TempData != None:
                    if TempProductID in TempData[0]:
                        # print int(SinglePurchase[3]) ," at ==> \n",total[each[0]][SinglePurchase[0]][0]
                        # print "TempData[0]", TempData[0]
                        # print "TempData[1]", TempData[1]

                        productIDPosition =  TempData[0].index(TempProductID)
                        QVal = TempData[1][productIDPosition]

                        sortedQValueOrder = list(TempData[1])
                        # print sortedQValueOrder
                        sortedQValueOrder.sort()
                        sortedQValueOrder.reverse()
                        # print  sortedQValueOrder

                        newProductPosition = sortedQValueOrder.index(QVal)

                        if TempOldProductPosition > newProductPosition + 1:
                            improve.append("old: " + str(TempOldProductPosition) +
                                           "|| new: " + str(newProductPosition + 1))
                        elif TempOldProductPosition < newProductPosition + 1:
                            dropdown.append("old: " + str(TempOldProductPosition) +
                                            "|| new: " + str(newProductPosition + 1))
                        else:
                            noChange.append("old: " + str(TempOldProductPosition) +
                                            "|| new: " + str(newProductPosition + 1))


                        # result.append("old: " + str(TempOldProductPosition) +
                            # "|| new: " + str(newProductPosition + 1))

                    # else not found
                    else:
                        # s
                        notFound = notFound + 1
    print " total purchase number is:", totalData
    print " total found number is:   ", totalData - notFound
    print "=========================================================="
    print " improve  :" , len(improve)
    for each in improve:
        print each
    print "=========================================================="

    print " dropdown :" , len(dropdown)
    for each in dropdown:
        print each
                # if int(SinglePurchase[3]) in getit[0]:
                #     print "get it :" , getit[0]
                # result[SinglePurchase[2]] = 0
    return result
# total = None
total = buildModel()
result = getTestData(total)

for each in result:
    print each
