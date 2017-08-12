# -*- coding: utf-8 -*-
# Author:	Jinglong Du
# email:	jid020@ucsd.edu

# Way to use base64:
# file_name_string = base64.urlsafe_b64encode("***$^%^(&&^$%&%*^(&*^?<>{}:>?<***")
# print file_name_string
# file_name_string = base64.urlsafe_b64decode(file_name_string)
# print file_name_string
# exit()
# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))
# from saver import *
from reward import *
import numpy as np
from numba import vectorize, float32, jit
import time
import base64
from datetime import datetime as dt
import os
from auc2 import *

wlmiss = 0
shpmiss = 0
GAMA = 0.9
scale = 1.0
QueryEmulator = True

ImprovePosition = 0
DropDownPosition = 0
ImprovePositionPercentage = 0.
DropDownPositionPercentage = 0.
totalPurchase = 0

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


def formatdata(UserNameID, existdata, path, ShoppingCartTrainingPath, WishlistTrainingPath, TotalDict):
    global start_time
    global accTime

    # list of (keyword, [])
    userData = importUserData(UserNameID, path)
    ShoppingCartDict = importShoppingData(UserNameID, ShoppingCartTrainingPath)
    WishListDict = importWLData(UserNameID, WishlistTrainingPath)

    # print "Size:    ", sys.getsizeof(TotalDict)
    # Shopping Cart Dictionary
    if UserNameID in TotalDict[2]:
        TotalDict[2][UserNameID] = addDictTogether(TotalDict[2][UserNameID], ShoppingCartDict)
    else:
        # print "."
        TotalDict[2][UserNameID] = ShoppingCartDict

    # WishList Dictionary, empty for now.
    if UserNameID in TotalDict[3]:
        TotalDict[3][UserNameID] = addDictTogether(TotalDict[3][UserNameID], WishListDict)
    else:
        # print "."
        TotalDict[3][UserNameID] = WishListDict

    if WishListDict is None:
        global wlmiss
        wlmiss = wlmiss + 1

    if ShoppingCartDict is None:
        global shpmiss
        shpmiss = shpmiss + 1

    # (productSKU, number)
    ClickDict = getClickDict(userData)
    if UserNameID in TotalDict[0]:
        TotalDict[0][UserNameID] = addDictTogether(TotalDict[0][UserNameID], ClickDict)
    else:
        # print "."
        TotalDict[0][UserNameID] = ClickDict

    PurchaseDict = getPurchaseDict(userData)
    if UserNameID in TotalDict[1]:
        TotalDict[1][UserNameID] = addDictTogether(TotalDict[1][UserNameID], PurchaseDict)
    else:
        # print "."
        TotalDict[1][UserNameID] = PurchaseDict

    # (keyword, [sku, sku, sku ...])
    NewQuery = FormatQuery(userData)
    # print "lens of NewQuery:" , len(NewQuery)
    # about 20 seconds

    newData = {}
    for each in NewQuery.items():
        # return [userID] = [ [sku, sku ...], [float Q, float Q, ...], [Reward R, reward R, ...] ]
        newData[each[0]] = [each[1], np.zeros((len(each[1]),), dtype=np.float32),
                            GetReward(each[1], ClickDict, PurchaseDict, WishListDict, ShoppingCartDict)]

    # existdata:       [NewQuery, QValue, RewardValue]
    ret = newData
    if len(existdata) > 0:
        # print existdata.items()[0]
        # combine two data set together.
        ret = combineTwoData(newData, existdata)

    # about 10 seconds
    # return [NewQuery,QValue, RewardValue]
    return ret


def buildModel(total, path, ShoppingCartTrainingPath, WishlistTrainingPath, Iteration, TotalDict):
    global wlmiss
    global shpmiss
    # ============================================================================================
    # init path for Basic info and query and click and purchase data.
    # path = 'DispatchedData/UserData1-5/'
    i = 0
    # ================= percentage ========
    z = len(os.listdir(path))/20.0  # ====
    a = 0                            # ====
    # ================= percentage ========

    start_time = time.time()

    # Import all data into the dictionary total.
    print "\n"
    print "Start importing data and generating model."
    print "====================================="

    for filename in os.listdir(path):
        # ================= percentage ========
        if i / z > a + 1:               # =====
            a = int(i / z)              # =====
            print "-",                  # =====
        # ================= percentage ========

        # see if current user exits
        existdata = []
        if filename in total:
            existdata = total[filename]

        data = formatdata(filename, existdata, path, ShoppingCartTrainingPath, WishlistTrainingPath, TotalDict)
        total[filename] = data
        i = i+1

    # for each in total.items():
    #     print each[0], " ==> ", each[1]
    #     break
    print ""
    print "====================================="
    # print "Finished building the initial model."
    # print "Wish-list miss match:    ", wlmiss
    #
    # wlmiss = 0
    # print "shopping cart miss match:", shpmiss
    #
    # shpmiss = 0
    # print "Total customer found:    ", len(total)

    # print("--- Read in data and initialization:    %s seconds ---" % (time.time() - start_time))

    # print("--- accumulative %s seconds ---" % accTime)
    # Single thread, 1000 user data. cost 50s.
    # 8 threads, 8000 user data in total, cost 100s.
    # 8 threads with cuda, 8000 user data in total, cost 300s.

    # Then start first Iteration for just one time with GAMA as followed.
    if Iteration:

        # print "Start iterations for models."
        start_time = time.time()
        for data in total.items():
            for each in data[1].items():
                # each ==> [sku[], InitQ[], Reward[]]
                # print "========================================================"
                # # total[userID][keyword/query][Q-value]
                # print total[data[0]][each[0]][1]
                total[data[0]][each[0]][1] = CoreFunc(each[1][2], each[1][1])
                # print total[data[0]][each[0]][1]
        # print("--- Last Iteration time: %s seconds ---" % (time.time() - start_time))
    return total


def getTestData(total, TotalResult, path, TotalDict):
    # ==========================================================================================
    # init path for Basic info and query and click and purchase data.
    # path = 'DispatchedData/UserDataJune/'
    TestTotal = {}
    # Import all data into the dictionary total.
    # print "Start importing testing data."
    for filename in os.listdir(path):
        ret = formatTestdata(filename, path)
        TestTotal[filename] = ret

    global ImprovePosition
    global DropDownPosition
    # global ImprovePositionPercentage
    # global DropDownPositionPercentage
    improve = []
    dropdown = []
    noChange = []
    AUC2 = []

    notFound = 0
    totalData = 0

    # for each users in the test
    for each in TestTotal.items():
        purchaseID = each[1][0]

        # each[0] is the filename, which represent userID
        # each[1] is the ret for this user that need to be tested.
        #       each [1][0] is the purchaseID
        #       each [1][1] is the returnDict
        global totalPurchase
        totalPurchase += len(each[1][1])

        # if there is more than one in returnDict, which means there is purchase
        if len(each[1][1].items()) >= 1:
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

                if True:
                # if TempData is not None:
                    # print SinglePurchaseQuery, " == ", SinglePurchase[0]
                    # if has corresponding query
                    # if TempData.has_key(SinglePurchaseQuery):
                    if False:
                    # if SinglePurchaseQuery in TempData:

                        # ModelDataList = [ [sku list], [Initial Q-Value], [Reward List] ]
                        ModelDataList = TempData[SinglePurchaseQuery]
                        # print "Length of the current purchase's Q-list: ", len(SinglePurchase[1])
                        # start form 0, ends at 10, total length is 10.
                        # That Q-value is corresponding to the SinglePurchase's new query.
                        QValue = np.arange(0, scale, scale*1.0/len(SinglePurchase[1]), dtype=np.float32)
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
                            ImprovePosition += productIDPosition - newProductPosition
                            # ImprovePositionPercentage += float(productIDPosition - newProductPosition)\
                            #                              /(productIDPosition + 1)
                            improve.append("Improve: " + str(productIDPosition - newProductPosition) +
                                           " || old position: " + str(productIDPosition + 1) +
                                           " || New position :" + str(newProductPosition + 1) +
                                           " || productID: " + str(SinglePurchasedProductID) +
                                           " || Query: " + SinglePurchaseQuery)
                            # AUC2 = [old position, new position, product ID, Query, Query Length]
                            AUC2.append([int(productIDPosition + 1), int(newProductPosition + 1),
                                         str(SinglePurchasedProductID), SinglePurchaseQuery, len(QValue)])

                        elif newProductPosition > productIDPosition:
                            DropDownPosition += newProductPosition - productIDPosition
                            # DropDownPositionPercentage += float(newProductPosition - productIDPosition)\
                            #                               /(newProductPosition + 1)
                            dropdown.append("Dropdown: " + str(newProductPosition - productIDPosition) +
                                            " || old position: " + str(productIDPosition + 1) +
                                            " || New position :" + str(newProductPosition + 1) +
                                            " || productID: " + str(SinglePurchasedProductID) +
                                            " || Query: " + SinglePurchaseQuery)
                            # AUC2 = [old position, new position, product ID, Query, Query Length]
                            AUC2.append([int(productIDPosition + 1), int(newProductPosition + 1),
                                         str(SinglePurchasedProductID), SinglePurchaseQuery, len(QValue)])

                        else:
                            noChange.append("old position: " + str(productIDPosition + 1) +
                                            " || New position :" + str(newProductPosition + 1) +
                                            " || productID: " + str(SinglePurchasedProductID) +
                                            " || Query: " + SinglePurchaseQuery)
                    else:
                        # not found query for this user.
                        notFound = notFound + 1
                        # use emulator?
                        if QueryEmulator:
                            # print "Emulator start......................................................"
                            QValue = np.arange(0, scale, scale * 1.0 / len(SinglePurchase[1]), dtype=np.float32)
                            QValue = np.flip(QValue, 0)
                            # RewardEmulator = np.zeros(len(SinglePurchase[1]), dtype=np.float32)
                            # if the userID is in the total Dict, which means it could be emulated.
                            skuList = []

                            for eaches in SinglePurchase[1]:
                                skuList.append(eaches[3])
                            # print "==============================="
                            # print len(skuList)
                            # print len(QValue)
                            ClickDict = {}
                            PurchaseDict = {}
                            ShoppingCartDict = {}
                            WishlistDict = {}
                            # TotalDict[0] = accumulativeClickDict
                            # TotalDict[1] = accumulativePurchaseDict
                            # TotalDict[2] = accumulativeShoppingCartDict
                            # TotalDict[3] = accumulativeWishlistDict

                            try:
                                # print each[0]
                                # print len(TotalDict[0])
                                # print TotalDict[0].items()[0]
                                ClickDict = TotalDict[0][each[0]]
                                # print "."
                            except Exception, e:
                                pass

                            try:
                                PurchaseDict = TotalDict[1][each[0]]
                                # print "."
                            except Exception, e:
                                pass

                            try:
                                ShoppingCartDict = TotalDict[2][each[0]]
                                # print "."
                            except Exception, e:
                                pass

                            try:
                                WishlistDict = TotalDict[3][each[0]]
                                # print "."
                            except Exception, e:
                                pass

                            RewardEmulator = GetReward(skuList, ClickDict, PurchaseDict,
                                                       WishlistDict, ShoppingCartDict)
                            # print RewardEmulator
                            if len(QValue) == len(RewardEmulator):

                                # QValue = QValue + RewardEmulator
                                QValue = CoreFunc( RewardEmulator,QValue)
                            else:
                                QValue = CoreFunc( RewardEmulator, QValue[:len(RewardEmulator)])
                              # QValue = QValue[:len(RewardEmulator)] + RewardEmulator


                            SinglePurchasedProductID = int(purchaseID[SinglePurchase[0]][3])
                            # match with the correspond model products.
                            productIDPosition = None
                            for eaches in xrange(len(SinglePurchase[1])):
                                if SinglePurchasedProductID == int(SinglePurchase[1][eaches][3]):
                                    productIDPosition = eaches
                                    # oldPos = SinglePurchase[1][each][5]
                                    # print SinglePurchase[1][each][4] , "==", each +1
                                    break
                            QValue = list(QValue)
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
                                ImprovePosition += productIDPosition - newProductPosition
                                # ImprovePositionPercentage += float(productIDPosition - newProductPosition)\
                                #                              /(productIDPosition + 1)
                                improve.append("Improve: " + str(productIDPosition - newProductPosition) +
                                               " || old position: " + str(productIDPosition + 1) +
                                               " || New position :" + str(newProductPosition + 1) +
                                               " || productID: " + str(SinglePurchasedProductID) +
                                               " || Query: " + SinglePurchaseQuery)
                                # AUC2 = [old position, new position, product ID, Query, Query Length]
                                AUC2.append([int(productIDPosition + 1), int(newProductPosition + 1),
                                             str(SinglePurchasedProductID), SinglePurchaseQuery, len(QValue)])

                            elif newProductPosition > productIDPosition:
                                DropDownPosition += newProductPosition - productIDPosition
                                # DropDownPositionPercentage += float(newProductPosition - productIDPosition)\
                                #                               /(newProductPosition + 1)
                                dropdown.append("Dropdown: " + str(newProductPosition - productIDPosition) +
                                                " || old position: " + str(productIDPosition + 1) +
                                                " || New position :" + str(newProductPosition + 1) +
                                                " || productID: " + str(SinglePurchasedProductID) +
                                                " || Query: " + SinglePurchaseQuery)
                                # AUC2 = [old position, new position, product ID, Query, Query Length]
                                AUC2.append([int(productIDPosition + 1), int(newProductPosition + 1),
                                             str(SinglePurchasedProductID), SinglePurchaseQuery, len(QValue)])

                            else:
                                noChange.append("old position: " + str(productIDPosition + 1) +
                                                " || New position :" + str(newProductPosition + 1) +
                                                " || productID: " + str(SinglePurchasedProductID) +
                                                " || Query: " + SinglePurchaseQuery)

    # print "Finished current test."
    # print "=========================================================="
    # print " improve  :", len(improve)
    # for each in improve:
    #     print each
    # print "=========================================================="
    #
    # print " dropdown :", len(dropdown)
    # for each in dropdown:
    #     print each
    # print "=========================================================="
    # print " noChange :", len(noChange)
    # # ********************************************************************************************
    # print "total Purchase History for tested month:       ", totalData
    # print "Model that not Found for corresponding query:  ", notFound
    # print "GAMA: ", GAMA

    TotalResult[0] = TotalResult[0] + improve
    TotalResult[1] = TotalResult[1] + dropdown
    TotalResult[2] = TotalResult[2] + noChange
    TotalResult[3] = TotalResult[3] + AUC2
    return TotalResult

# ==========================================================
# ================ Start the func ==========================
# ==========================================================
total = {}
# accumulativeClickDict = {}
# accumulativePurchaseDict = {}
# accumulativeShoppingCartDict = {}
# accumulativeWishlistDict = {}

# TotalDict = [accumulativeClickDict, accumulativePurchaseDict, accumulativeShoppingCartDict, accumulativeWishlistDict]
TotalDict = [{}, {}, {}, {}]
# result = [improve, dropdown, noChange]
TotalResult = [[], [], [], []]

# TrainingPath = 'DispatchedData/UserDataJan/'
# ShoppingCartTrainingPath = "DispatchedData/UserAddToCartJan/"
# WishlistTrainingPath = "DispatchedData/UserFollowJan/"
# total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True, TotalDict)
#
# TestingPath = 'DispatchedData/UserDataFeb/'
# TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)
#
# TrainingPath = 'DispatchedData/UserDataFeb/'
# ShoppingCartTrainingPath = "DispatchedData/UserAddToCartFeb/"
# WishlistTrainingPath = "DispatchedData/UserFollowFeb/"
# total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True, TotalDict)
#
# TestingPath = 'DispatchedData/UserDataMar/'
# TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)
#
# TrainingPath = 'DispatchedData/UserDataMar/'
# ShoppingCartTrainingPath = "DispatchedData/UserAddToCartMar/"
# WishlistTrainingPath = "DispatchedData/UserFollowMar/"
# total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True, TotalDict)
#
# TestingPath = 'DispatchedData/UserDataApr/'
# TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)
#
# TrainingPath = 'DispatchedData/UserDataApr/'
# ShoppingCartTrainingPath = "DispatchedData/UserAddToCartApr/"
# WishlistTrainingPath = "DispatchedData/UserFollowApr/"
# total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True, TotalDict)
#
# TestingPath = 'DispatchedData/UserDataMay/'
# TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)
#
# TrainingPath = 'DispatchedData/UserDataMay/'
# ShoppingCartTrainingPath = "DispatchedData/UserAddToCartMay/"
# WishlistTrainingPath = "DispatchedData/UserFollowMay/"
# total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True, TotalDict)
#
# TestingPath = 'DispatchedData/UserDataJune/'
# TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)

# TrainingPath = 'DispatchedData/UserDataJan/'
# ShoppingCartTrainingPath = "DispatchedData/UserAddToCartJan/"
# WishlistTrainingPath = "DispatchedData/UserFollowJan/"
# total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)
# Path = 'DispatchedData/UserDataFeb/'
# TotalResult = getTestData(total, TotalResult, TestingPath)
#
# TrainingPath = 'DispatchedData/UserDataJan+Feb/'
# ShoppingCartTrainingPath = "DispatchedData/UserAddToCartJan+Feb/"
# WishlistTrainingPath = "DispatchedData/UserFollowJan+Feb/"
# total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)
#
# TestingPath = 'DispatchedData/UserDataMar/'
# TotalResult = getTestData(total, TotalResult, TestingPath)
#
# TrainingPath = 'DispatchedData/UserDataJan+Feb+Mar/'
# ShoppingCartTrainingPath = "DispatchedData/UserAddToCartJan+Feb+Mar/"
# WishlistTrainingPath = "DispatchedData/UserFollowJan+Feb+Mar/"
# total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)
#
# TestingPath = 'DispatchedData/UserDataApr/'
# TotalResult = getTestData(total, TotalResult, TestingPath)
#
# TrainingPath = 'DispatchedData/UserDataJan+Feb+Mar+Apr/'
# ShoppingCartTrainingPath = "DispatchedData/UserAddToCartJan+Feb+Mar+Apr/"
# WishlistTrainingPath = "DispatchedData/UserFollowJan+Feb+Mar+Apr/"
# total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)
#
# TestingPath = 'DispatchedData/UserDataMay/'
# TotalResult = getTestData(total, TotalResult, TestingPath)
#
# TrainingPath = 'DispatchedData/UserData1-5/'
# ShoppingCartTrainingPath = "DispatchedData/UserAddToCart1-5/"
# WishlistTrainingPath = "DispatchedData/UserFollow1-5/"
# total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)
#
# TestingPath = 'DispatchedData/UserDataJune/'
# TotalResult = getTestData(total, TotalResult, TestingPath)


for x in xrange(30):
    TrainingPath = 'NewDispatchedData/UserDataJan/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartJan/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowJan/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)

    TestingPath = 'NewDispatchedData/UserDataJan/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)

TrainingPath = 'NewDispatchedData/UserDataJan/' + str(31) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartJan/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowJan/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)

TestingPath = 'NewDispatchedData/UserDataFeb/'+ str(1)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)

for x in xrange(30):
    TrainingPath = 'NewDispatchedData/UserDataFeb/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartFeb/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowFeb/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)
    TestingPath = 'NewDispatchedData/UserDataFeb/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)

TrainingPath = 'NewDispatchedData/UserDataFeb/' + str(31) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartFeb/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowFeb/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)
TestingPath = 'NewDispatchedData/UserDataMar/'+ str(1)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)

for x in xrange(30):
    TrainingPath = 'NewDispatchedData/UserDataMar/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartMar/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowMar/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)
    TestingPath = 'NewDispatchedData/UserDataMar/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)


TrainingPath = 'NewDispatchedData/UserDataMar/' + str(31) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartMar/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowMar/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)

TestingPath = 'NewDispatchedData/UserDataApr/'+ str(1)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)

for x in xrange(30):
    TrainingPath = 'NewDispatchedData/UserDataApr/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartApr/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowApr/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)

    TestingPath = 'NewDispatchedData/UserDataApr/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)

TrainingPath = 'NewDispatchedData/UserDataApr/' + str(31) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartApr/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowApr/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)

TestingPath = 'NewDispatchedData/UserDataMay/'+ str(1)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)

for x in xrange(30):
    TrainingPath = 'NewDispatchedData/UserDataMay/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartMay/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowMay/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)
    TestingPath = 'NewDispatchedData/UserDataMay/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)


TrainingPath = 'NewDispatchedData/UserDataMay/' + str(31) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartMay/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowMay/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)

TestingPath = 'NewDispatchedData/UserDataJune/'+ str(1)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)

for x in xrange(30):
    TrainingPath = 'NewDispatchedData/UserDataJune/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartJune/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowJune/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)

    TestingPath = 'NewDispatchedData/UserDataJune/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)

TrainingPath = 'NewDispatchedData/UserDataJune/' + str(30) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartJune/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowJune/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, False, TotalDict)

TestingPath = 'NewDispatchedData/UserDataJune/'+ str(31)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath, TotalDict)

print "=========================================================="
print "================ The Final Result ========================"
print "=========================================================="
# print "Improve  :", len(TotalResult[0]), "; Improve position: ", ImprovePosition, \
#     ", Average: ", float(ImprovePosition)/len(TotalResult[0]), \
#     ", Improve percentage: ", ImprovePositionPercentage/len(TotalResult[0])
for each in TotalResult[0]:
    print each
print "=========================================================="
# print "Dropdown :", len(TotalResult[1]),"; Dropdown position: ", DropDownPosition, \
#     ", Average: ", float(DropDownPosition)/len(TotalResult[1]), \
#     ", Dropdown percentage: ", DropDownPositionPercentage/len(TotalResult[1])
# for each in TotalResult[1]:
#     print each
print "=========================================================="
print "Improve  :", len(TotalResult[0]), "; Improve position: ", ImprovePosition, \
    ", Average: ", float(ImprovePosition)/len(TotalResult[0])
    # ", Improve percentage: ", ImprovePositionPercentage/len(TotalResult[0])
print "Dropdown :", len(TotalResult[1]), "; Dropdown position: ", DropDownPosition, \
    ", Average: ", float(DropDownPosition)/len(TotalResult[1])
    # ", Dropdown percentage: ", DropDownPositionPercentage/len(TotalResult[1])
print "No Change :", len(TotalResult[2])
print "GAMA: ", GAMA

# for each in TotalResult[3]:
#     print "old position: ", each[0], "new position: ", each[1], "|| product ID: ", each[2], \
#         "|| Query:", each[3],"|| Query Lenth", each[4]

# AUCDrop = []
# AUCDropAveTotal = 0.0
# AUCImprove = []
# AUCImproveAveTotal = 0.0

print "=========================================================="
print "AUC2 :", len(TotalResult[3])
print "average based on : AUC2@1, @2, @3, @4, @5, @6, @10, @20, @40, @all"
OldAverageTotal = 0.0
NewAverageTotal = 0.0

# AUC2@ =    [ @1, @2, @3, @4, @5, @6, @10, @20, @40, @all]
oldAUC2at =  [ [], [], [], [], [], [],  [],  [],  [],   []]
newAUC2at =  [ [], [], [], [], [], [],  [],  [],  [],   []]


for each in TotalResult[3]:
    retAUC = auc2(each)
    # oldAUC2Ave = sum(retAUC[0])/len(retAUC[0])
    # OldAverageTotal += oldAUC2Ave
    # newAUC2Ave = sum(retAUC[1]) / len(retAUC[1])
    # NewAverageTotal += newAUC2Ave
    #
    # average = newAUC2Ave - oldAUC2Ave

    # print " || old position: ", str(each[0]), " || new position: ", \
    #     str(each[1]), "|| product ID: ", str(each[2]), "|| Query: ", \
    #     each[3], "|| Query Lenth: ", str(each[4])

    positionlist = [1,2,3,4,5,6,10,20,40,"all"]
    for x in xrange(len(retAUC[0]) -1):
        oldAUC2at[x].append(retAUC[0][x])
        newAUC2at[x].append(retAUC[1][x])
        # print "old AUC @" ,positionlist[x],": ", retAUC[0][x], "new AUC @" ,positionlist[x],": ", retAUC[1][x]

    oldAUC2at[len(positionlist) -1].append(retAUC[0][len(retAUC[0]) -1])
    newAUC2at[len(positionlist) - 1].append(retAUC[1][len(retAUC[1]) - 1])
    # print "old AUC @", positionlist[len(positionlist) -1], ": ", retAUC[0][len(retAUC[0]) -1], "new AUC @", \
    #         positionlist[len(positionlist) -1], ": ", retAUC[1][len(retAUC[1]) -1]

print "=========================================================="
print "Average AUC2 comparision"
positionlist = [1, 2, 3, 4, 5, 6, 10, 20, 40, "all"]
overallDiff = 0.0
for x in xrange(10):
    new = sum(newAUC2at[x])/len(newAUC2at[x])
    old = sum(oldAUC2at[x])/len(oldAUC2at[x])
    Diff = (new - old)/(old)
    print "old AUC @" ,positionlist[x],": ",old, "|| new AUC @" ,positionlist[x],": ", new , "|| RP: ", Diff*100 , "%"
    overallDiff += Diff

print "Average RP :", overallDiff*10 , "%"

print "totalPurchase:" , totalPurchase

# print "Average old AUC2:        ", OldAverageTotal/len(TotalResult[3])
# print "Average new AUC2:        ", NewAverageTotal/len(TotalResult[3])
# print "Improvement (new - old): ", NewAverageTotal/len(TotalResult[3]) - OldAverageTotal/len(TotalResult[3])
    # AUC2 = [old position, new position, product ID, Query, Query Length]
    # if retAUC[0] > retAUC[1]:
    #     AUCDrop.append("AUC drop: " + str(retAUC[0] - retAUC[1]) + " || old position: " +
    #                 str(each[0]) + " || new position: " +  str(each[1]) +  "|| product ID: " +
    #                 str(each[2]) + "|| Query: " +  each[3] + "|| Query Lenth: " + str(each[4]))
    #     AUCDropAveTotal += retAUC[0] - retAUC[1]
    # else:
    #     AUCImprove.append("AUC Improve: " + str(retAUC[1] - retAUC[0]) + " || old position: " +
    #                 str(each[0]) + " || new position: " +  str(each[1]) +  "|| product ID: " +
    #                 str(each[2]) + "|| Query: " +  each[3] + "|| Query Lenth: " + str(each[4]))
    #     AUCImproveAveTotal += retAUC[1] - retAUC[0]



# AUCDropAve = AUCDropAveTotal/ len(AUCDrop)
# AUCImproveAve = AUCImproveAveTotal/len(AUCImprove)
# print "=========================================================="
# print "=========================================================="
# print "AUC2 dropdown total: ", AUCDropAveTotal, "AUC2 dropdown average: ", AUCDropAve, \
#         " || , AUC2 drop down number: ", len(AUCDrop)
# print
# for each in AUCDrop:
#     print each
# print
# print "=========================================================="
# print "=========================================================="
# print "AUC2 Improve total: ", AUCImproveAveTotal, "AUC2 Improve average: ", AUCImproveAve, \
#         " || , AUC2 Improve number: ", len(AUCImprove)
# print
# for each in AUCImprove:
#     print each
#
# print "=========================================================="
# print "=========================================================="
# print "AUC improve - dropdown: ", str(AUCImproveAveTotal - AUCDropAveTotal)