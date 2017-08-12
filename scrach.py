#-*- coding: utf-8 -*-
#Author:	Jinglong Du
#email:		jid020@ucsd.edu

# Way to use base64:
# file_name_string = base64.urlsafe_b64encode("***$^%^(&&^$%&%*^(&*^?<>{}:>?<***")
# print file_name_string
# file_name_string = base64.urlsafe_b64decode(file_name_string)
# print file_name_string
# exit()
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
GAMA = 0.2

# best for now: 0.2 13/1
#   0.15  9/1
#   0.18 12/1
#   0.22 13/2
#   0.24 13/2
#   0.26 13/3
#   0.28 13/3

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
    # about 9 second

    if WishListDict == None:
        global wlmiss
        wlmiss = wlmiss + 1

    if ShoppingCartDict == None:
        global shpmiss
        shpmiss = shpmiss + 1

    # (productSKU, number)
    ClickDict = getClickDict(userData)
    PurchaseDict = getPurchaseDict(userData)
    # about 10 second

    # (keyword, [sku, sku, sku ...])
    NewQuery = FormatQuery(userData)
    # print "lens of NewQuery:" , len(NewQuery)
    # about 20 seconds

    ret = {}
    for each in NewQuery.items():
        # return [userID] = [ [sku, sku ...], [float Q, float Q, ...], [Reward R, reward R, ...] ]
        ret[each[0]] = [each[1], np.zeros((len(each[1]),), dtype=np.float32),
                        GetReward(each[1], ClickDict, PurchaseDict, WishListDict, ShoppingCartDict)]

    # about 10 seconds
    # return [NewQuery,QValue, RewardValue]
    return ret

def buildModel():
    # ==================================================================================================
    # init path for Basic info and query and click and purchase data.
    path = 'DispatchedData/UserData1-5/'
    i = 0
    # ================= percentage ========
    z = len(os.listdir(path))/100.0 # =====
    a = 0                           # =====
    # ================= percentage ========

    start_time = time.time()
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
    print "=========================================================="
    print "Finished building the initial model."
    print "Wish-list miss match:    ", wlmiss
    print "shopping cart miss match:", shpmiss
    print "Total customer found:    ", len(total)
    print("--- Read in data and initialization:    %s seconds ---" % (time.time() - start_time))
    # print("--- accumulative %s seconds ---" % accTime)
    #Single thread, 1000 user data. cost 50s.
    #8 threads, 8000 user data in total, cost 100s.
    #8 threads with cuda, 8000 user data in total, cost 300s.

    # Then start first Iteration for just one time with GAMA as followed.
    print "=========================================================="
    print "Start iterations for models."
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

def getTestData(total):
    # ==================================================================================================
    # init path for Basic info and query and click and purchase data.
    path = 'DispatchedData/UserDataJune/'
    TestTotal = {}
    # Import all data into the dictionary total.
    print "Start importing testing data."
    for filename in os.listdir(path):

        ret = formataaaadata(filename)

        # purchaseID[sessionID] = targetPurchaseID
        # purchaseID = ret[0]
        # returnDict[sessionID] = [splited, splited, splited, ...]
        # returnDict = ret[1]
        TestTotal[filename] = ret

    result = []
    QValue = None
    improve = []
    dropdown = []
    noChange = []

    notFound = 0
    totalData = 0

    # for each users in the test
    for each in TestTotal.items():
        purchaseID = each [1][0]

        # each[0] is the filename, which represent userID
        # each[1] is the ret for this user that need to be tested.
        #       each [1][0] is the purchaseID
        #       each [1][1] is the returnDict

        # if there is more than one in returnDict, which means there is purchase
        if len(each[1][1].items())>1:
            # print len(each[1].items())

            # for each purchases for one user
            for SinglePurchase in each[1][1].items():

                # get that purchase's query from the the first record's query.
                SinglePurchaseQuery = SinglePurchase[1][0][0]


                totalData = totalData + 1
                TempData = None
                # [query, userid, sessionid, productid, rank, time, click, purchase]
                try:
                    # get potential data from total.
                    TempData = total[each[0]]
                except Exception, e:
                    # print " Not found userID:", each[0], " and query:", SinglePurchase[0]
                    # not fount user.
                    notFound = notFound + 1

                # for now, I have SinglePurchase and TempData
                # SinglePurchase represents:
                    # SinglePurchase[0] is the sessionID
                    # SinglePurchase[1] is the splits' list.
                # TempData represents:
                    # Data[Query/keywords] = [ [sku list], [Initial Q-Value], [Reward List] ]
                # if has corresponding user
                if TempData != None:

                    # print SinglePurchaseQuery, " == ", SinglePurchase[0]
                    # if has corresponding query
                    if TempData.has_key(SinglePurchaseQuery):
                        # ModelDataList = [ [sku list], [Initial Q-Value], [Reward List] ]
                        ModelDataList = TempData[SinglePurchaseQuery]
                        # print "Length of the current purchase's Q-list: ", len(SinglePurchase[1])
                        # start form 0, ends at 10, total length is 10.
                        # That Q-value is corresponding to the SinglePurchase's new query.
                        QValue = np.arange(0, 10, 10.0/len(SinglePurchase[1]), dtype=np.float32)
                        QValue = np.flip(QValue, 0)

                        # for splited in SinglePurchase[1]:
                        for number in xrange(len(SinglePurchase[1])):
                            # [query, userid, sessionid, productid, rank, time, click, purchase]
                            # if the products is in the model's products list, then
                            if int(SinglePurchase[1][number][3]) in ModelDataList[0]:
                                index = ModelDataList[0].index(int(SinglePurchase[1][number][3]))
                                QValue[number] += ModelDataList[1][index]
                        # print QValue
                        # ===================================================================
                        # get the current purchase product ID
                        SinglePurchasedProductID = int(purchaseID[SinglePurchase[0]][3])
                        # match with the correspond model products.
                        productIDPosition = None
                        for each in xrange(len(SinglePurchase[1])):
                            if SinglePurchasedProductID == int(SinglePurchase[1][each][3]):
                                productIDPosition = each
                                # oldPos = SinglePurchase[1][each][5]
                                # print SinglePurchase[1][each][4] , "==", each +1
                                break
                        TargetQValue = QValue[productIDPosition]

                        # print "======================================================="
                        # print "old position: ", productIDPosition + 1, " ==> Q-value:", TargetQValue
                        # print QValue
                        QValue.sort()
                        QValue = np.flip(QValue, 0)
                        # print "After: ========================"
                        # print QValue
                        newProductPosition = list(QValue).index(TargetQValue)
                        if newProductPosition < productIDPosition:
                            improve.append("old position: "+ str(productIDPosition + 1) +
                                " || New position :"+ str(newProductPosition + 1) +
                                " || productID: " + str(SinglePurchasedProductID) + " || Query: " + SinglePurchaseQuery)

                        elif newProductPosition > productIDPosition:
                            dropdown.append("old position: " + str(productIDPosition + 1) +
                                " || New position :" + str(newProductPosition + 1) +
                                " || productID: " + str(SinglePurchasedProductID) + " || Query: " + SinglePurchaseQuery)
                        else:
                            noChange.append("old position: " + str(productIDPosition + 1) +
                                " || New position :" + str(newProductPosition + 1) +
                                " || productID: " + str(SinglePurchasedProductID) + " || Query: " + SinglePurchaseQuery)
                        # print "old position: ", productIDPosition + 1, " || New position :", newProductPosition + 1
                        # if SinglePurchasedProductID in ModelDataList[0]:
                        #     # get the position in that products list.
                        #     productIDPosition = ModelDataList[0].index(SinglePurchasedProductID)
                        #     print len(QValue)
                        #     print "SinglePurchasedProductID:" , SinglePurchasedProductID
                        #     print "productIDPosition:       " , productIDPosition
                        #     NewQValueForPurchaseProducts = QValue[productIDPosition]
                        #     print "NewQValueForPurchaseProducts:    " , NewQValueForPurchaseProducts
                    else:
                        # not found query for this user.
                        notFound = notFound + 1

                # QVal = TempData[1][productIDPosition]
                #
                # sortedQValueOrder = list(TempData[1])
                # # print sortedQValueOrder
                # sortedQValueOrder.sort()
                # sortedQValueOrder.reverse()
                # # print sortedQValueOrder
                # newProductPosition = sortedQValueOrder.index(QVal)

                #Q-value here
                # print QValue
                #purchaseID[sessionID]

                # tempSessionID = SinglePurchase[1][0][2]
                # print "==============================================="
                # print "first session ID is :", tempSessionID
                # for trefagefa in SinglePurchase[1]:
                #     if tempSessionID != trefagefa[2]:
                #         print "==============================================="
                #         print "first session ID is :", tempSessionID
                #         print "Different SessionID is: ", trefagefa[2]





    # ********************************************************************************************
    #         for SinglePurchase in each[1].item():
    #             # print "============================="
    #             # print SinglePurchase
    #             totalData = totalData + 1
    #             TempData = None
    #             # [query, userid, sessionid, productid, rank, time, click, purchase
    #             try:
    #                 # all the data needed here from total.
    #                 TempData = total[each[0]][SinglePurchase[0]]
    #             except Exception, e:
    #                 # print " Not found userID:", each[0], " and query:", SinglePurchase[0]
    #                 notFound = notFound + 1
    #
    #             # the product ID that purchased.
    #             TempProductID = int(SinglePurchase[3])
    #             # the old position that in the search list
    #             TempOldProductPosition = int(SinglePurchase[4])
    #             # if product found here
    #
    #             if TempData != None:
    #                 if TempProductID in TempData[0]:
    #                     # print int(SinglePurchase[3]) ," at ==> \n",total[each[0]][SinglePurchase[0]][0]
    #                     # print "TempData[0]", TempData[0]
    #                     # print "TempData[1]", TempData[1]
    #
    #                     productIDPosition =  TempData[0].index(TempProductID)
    #                     QVal = TempData[1][productIDPosition]
    #
    #                     sortedQValueOrder = list(TempData[1])
    #                     # print sortedQValueOrder
    #                     sortedQValueOrder.sort()
    #                     sortedQValueOrder.reverse()
    #                     # print sortedQValueOrder
    #
    #                     newProductPosition = sortedQValueOrder.index(QVal)
    #
    #                     if TempOldProductPosition > newProductPosition + 1:
    #                         improve.append("old: " + str(TempOldProductPosition) +
    #                                        "|| new: " + str(newProductPosition + 1))
    #                     elif TempOldProductPosition < newProductPosition + 1:
    #                         dropdown.append("old: " + str(TempOldProductPosition) +
    #                                         "|| new: " + str(newProductPosition + 1))
    #                     else:
    #                         noChange.append("old: " + str(TempOldProductPosition) +
    #                                         "|| new: " + str(newProductPosition + 1))
    #                 # else not found
    #                 else:
    #                     notFound = notFound + 1
    # print " total purchase number is:", totalData
    # print " total found number is:   ", totalData - notFound

    print "Finished test."
    print "=========================================================="
    print " improve  :" , len(improve)
    for each in improve:
        print each
    print "=========================================================="

    print " dropdown :" , len(dropdown)
    for each in dropdown:
        print each
    # print "=========================================================="
    # print len(noChange)
    # ********************************************************************************************
    print "total Purchase History for tested month:       ", totalData
    print "Model that not Found for corresponding query:  ", notFound
    print "GAMA: ", GAMA

    return [improve, dropdown, noChange]

# total = None
total = buildModel()

#result = [improve, dropdown, noChange]
result = getTestData(total)
# for each in result:
#     print each

