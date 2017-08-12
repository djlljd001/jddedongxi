# -*- coding: utf-8 -*-

# Author:    Jinglong Du
# email:     jid020@ucsd.edu

import numpy as np
from numba import vectorize, float32, jit
import time
from datetime import datetime as dt
import io
def importTestingUserData(UserNameID):
    try:
        ret = []
        filename = u"DispatchedData/UserDataJune/" + UserNameID
        files = io.open(filename, "r" ,encoding='utf8')
        userData = files.read().splitlines()
        # split data here once to optimize program later
        for line in userData:
            splited = line.split("\t")
            ret.append(splited)
        files.close()
        return ret
    except Exception, e:
        print "DATA WARNING:    Failed in Finding/Reading in Test Query name list."
        return None

def getTestPurchaseDict(userData):

    # [purchase sessionID, purchase sessionID, ...]
    PurchaseDict = []
    # [keyword/query: [splited, splited, splited, ...], keyword/query: [ splited, splited, splited, ...] ...]
    returnDict = {}
    PurchaseID = {}
    # this part is for getting the potential query session id.
    for splited in userData:
        # save purchase data's session number.
        if splited[7] == "1":
            PurchaseDict.append(splited[2])
            PurchaseID[splited[2]] = splited
    # this part is to get the useful query list for the potential purchase.
    for splited in userData:
        if splited[2] in PurchaseDict:
            if returnDict.has_key(splited[2]):
                returnDict[splited[2]].append( splited )
            else:
                returnDict[splited[2]] = [ splited ]
    ret = [PurchaseID, returnDict]
    return ret

def importUserData(UserNameID):
    try:
        ret = []
        filename = u"DispatchedData/UserData1-5/" + UserNameID
        files = io.open(filename, "r" ,encoding='utf8')
        userData = files.read().splitlines()
        # split data here once to optimize program later
        for line in userData:
            splited = line.split("\t")
            ret.append(splited)
        files.close()
        return ret
    except Exception, e:
        print "DATA WARNING:    Failed in Finding/Reading in Query name list."
        return None


# not enough data for now, so return None for now.
def importWLData(UserNameID):
    # =========================================================================================
    # =========================================================================================
    # try:
    #     ret = {}
    #     filename = u"DispatchedData/UserFollowJan/" + UserNameID
    #     files = io.open(filename, "r" ,encoding='utf8')
    #     userData = files.read().splitlines()
    #     # split data here once to optimize program later
    #     for line in userData:
    #         splited = line.split("\t")
    #         ret[splited[1]] = 1
    #     files.close()
    #     return ret
    # except Exception, e:
    #     # print "DATA WARNING:    Failed in Finding/Reading in", UserNameID, " wishlist product list."
    #     return None
    # =========================================================================================
    # =========================================================================================
    return None


def importShoppingData(UserNameID):
    try:
        ret = {}
        filename = u"DispatchedData/UserAddToCart1-5/" + UserNameID
        files = io.open(filename, "r" ,encoding='utf8')
        userData = files.read().splitlines()
        # split data here once to optimize program later
        for line in userData:
            splited = line.split("\t")
            ret[splited[1]] = 1
        files.close()
        return ret
    except Exception, e:
        # print "DATA WARNING:    Failed in Finding/Reading in", UserNameID, " shopping cart product list."
        return None



def getClickDict(userData):
    # ( str(product sku), int ClickDict time)
    ClickDict = {}
    # for line in userData:
    #     splited = line.split("\t")
    for splited in userData:
        # print splited
        # save click data
        if ClickDict.has_key(splited[3]):
            ClickDict[splited[3]] += int(splited[6])
        else:
            ClickDict[splited[3]] = int(splited[6])
    return ClickDict


def getPurchaseDict(userData):
    # ( str(product sku), int purchase time)
    PurchaseDict = {}
    # for line in userData:
    #     splited = line.split("\t")
    for splited in userData:
        # save purchase data
        if PurchaseDict.has_key(splited[3]):
            PurchaseDict[splited[3]] += int(splited[7])
        else:
            PurchaseDict[splited[3]] = int(splited[7])
    return PurchaseDict


def formataaaadata(UserNameID):
    # (keyword : [ 10, 9, 8, 7...])
    # Just try what's going on there.
    # the temporary dictionary for that person for that kind of data.
    global start_time

    # list of (keyword, [])
    userData = importTestingUserData(UserNameID)
    # this is a list of session number that contains all the useful session number.
    returnDict = getTestPurchaseDict(userData)

    # return [NewQuery,QValue, RewardValue]
    return returnDict

def FormatQuery(userData):
    # (query/keyword, boolean): chech which query is useful
    UsefulQuery = {}
    NewQuery = {}
    # for line in userData:
    # splited = line.split("\t")
    for splited in userData:
        #save Useful query data
        if splited[6] == "1" or splited[7] == "1":
            if not UsefulQuery.has_key(splited[0]):
                UsefulQuery[splited[0]] = True
            #     if UsefulQuery[splited[0]] >  dt.strptime(splited[5], '%Y-%m-%d %H:%M:%S'):
            #         UsefulQuery[splited[0]] = dt.strptime(splited[5], '%Y-%m-%d %H:%M:%S')
            # else:
            #     #   dt.strptime("10/12/13", "%m/%d/%y")   2017-03-12 09:48:44
            #     UsefulQuery[splited[0]] =  dt.strptime(splited[5], '%Y-%m-%d %H:%M:%S')

    # save useful query's product list.
    # for line in userData:
    # splited = line.split("\t")
    for splited in userData:
        # if it is useful query
        if UsefulQuery.has_key(splited[0]):
            # if already have this query
            if NewQuery.has_key(splited[0]):
                #if that query does not contains that product
                if int(splited[3]) not in NewQuery[splited[0]]:
                    NewQuery[splited[0]].append(int(splited[3]))
                    # #if that query's position is in the range.
                    # if int(splited[4]) <= len(NewQuery[splited[0]]):
                    #     # if the new inserted products is in the most up to date query order, then
                    #     if dt.strptime(splited[5], '%Y-%m-%d %H:%M:%S') <= UsefulQuery[splited[0]]:
                    #         # insert that products to the corresponding position into list that is newly
                    #         # shown in the up-to-date query.
                    #         NewQuery[splited[0]].insert(int(splited[4]) - 1, int(splited[3]))
                    #     else:
                    #         # append to the end of the products list
                    #         NewQuery[splited[0]].append(int(splited[3]))
                    # if it is out of range, i.e. it is the new added product for that query
                    # else:s
                    #     # append to the end of the products list
                    #     NewQuery[splited[0]].append(int(splited[3]))
            # if not have that query yet. Create new list for that query.
            else:
                NewQuery[splited[0]] = [int(splited[3])]
    return NewQuery



#decay rate function based on N_SA(s, a) value, let's first assume it is 1,
#which means no decay for any N_SA value.
def Decay (DecayRate, N_SAValue):
    return 1


#The N_SA[s1s,a] function. No data yet, so set to default 1.
def N_sa(s1s, a):
    return 1


#The main function that will return the reward R[s'] for Step 2 State
#There is no data yet, so set to 0 first.

# U = R_S( QueryList)
def R_S(QueryList):
    prodRZName = "QueryListReward.QLR"
    prodRZ = []
    try:
        files = open(prodRZName, "r")
        # prodRZ = np.array(files.read().splitlines(), dtype=np.float32)
        prodRZ = files.read().splitlines()
        files.close()
    except Exception, e:
        pass
        # print "DATA WARNING:    Failed in Finding/Reading in product Reward AT 33"

    prodRZ = [int(x) for x in prodRZ]
    prodRZ = np.array(prodRZ, dtype=np.float32)
    if prodRZ.size > 0:
        return prodRZ
    else:
        # print "WARNING:    No product reward data AT 38"
        return np.array([0]*len(QueryList), dtype=np.float32)


#this part will generate the initial value for Q.
def initQ(s1s, a, rank):
    return 0

#X = purchaseModel(QueryList, PurchaseDict)
def purchaseModel(QueryList, PurchaseDict):
    purchR = []
    #
    for each in QueryList:
        if PurchaseDict.has_key(str(each)):
            purchR.append(PurchaseDict[str(each)])
        else:
            purchR .append(0)

    reward = [0]*len(QueryList)
    for x in xrange(len(QueryList)):
        if purchR[x] < 2:
            reward[x] = 0
        elif purchR[x] < 3:
            reward[x] = 1
        elif purchR[x] < 5:
            reward[x] = 3
        elif purchR[x] < 20:
            reward[x] = 8
        else:
            reward[x] = 20
    return np.array(reward, dtype=np.float32)

# Y = clickModel(QueryList, ClickDict)
def clickModel(QueryList, ClickDict):
    clkR = []
    for each in QueryList:
        if ClickDict.has_key(str(each)):
            clkR.append(ClickDict[str(each)])
        else:
            clkR .append(0)
    minClick = min(clkR)
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
        elif clkR[x] <= maxClick*3/4:
            reward[x] = 4
        else:
            reward[x] = 5
    return np.array(reward, dtype=np.float32)



def wishListModel(QueryList, WishListDict):
    wiLiR = []
    reward = [0] * len(QueryList)
    if WishListDict != None:
        for each in QueryList:
            if WishListDict.has_key(str(each)):
                wiLiR.append(WishListDict[str(each)])
            else:
                wiLiR.append(0)
        for x in xrange(len(wiLiR)):
            if wiLiR[x] <= 0:
                reward[x] = 0
            elif wiLiR[x] <= 1:
                reward[x] = 2
            elif wiLiR[x] <= 2:
                reward[x] = 4
            elif wiLiR[x] <= 4:
                reward[x] = 5
            else:
                reward[x] = 6
    return np.array(reward, dtype=np.float32)

def ShoppingCartModel(QueryList, ShoppingCartDict):
    ShpCartR = []
    reward = [0] * len(QueryList)
    if ShoppingCartDict != None:
        for each in QueryList:
            if ShoppingCartDict.has_key(str(each)):
                ShpCartR.append(ShoppingCartDict[str(each)])
            else:
                ShpCartR.append(0)
        for x in xrange(len(ShpCartR)):
            if ShpCartR[x] <= 0:
                reward[x] = 0
            elif ShpCartR[x] <= 1:
                reward[x] = 2
            elif ShpCartR[x] <= 2:
                reward[x] = 4
            elif ShpCartR[x] <= 4:
                reward[x] = 5
            else:
                reward[x] = 6
    return np.array(reward, dtype=np.float32)

#The R[s1s, a] function, which corresponding to the target customers, key words and products.
#No data yet, so set to 0 first.

#with GPU, do that:
#@vectorize(['float32(float32, float32)'], target='cuda')


# RewardValue[each[0]] = GetReward(UserNameID, each[0], each[1])
def GetReward( QueryList, ClickDict, PurchaseDict , WishListDict, ShoppingCartDict):
    # X = purchaseModel(QueryList, PurchaseDict)
    # Y = clickModel(QueryList, ClickDict)
    # Z = wishListModel(QueryList, WishListDict)
    # U = R_S( QueryList)
    # V = ShoppingCartModel(QueryList, ShoppingCartDict)
    # ret = addTogether(X, Y, U, Z, V)
    ret = addTogether(purchaseModel(QueryList, PurchaseDict), clickModel(QueryList, ClickDict),
                      wishListModel(QueryList, WishListDict), R_S( QueryList),
                      ShoppingCartModel(QueryList, ShoppingCartDict))
    # print "Final reward func: " , ret
    return ret


# @vectorize(['float32(float32, float32, float32, float32)'], target='cpu')
# def addTogether(X, Y, Z, U):
#   return X + Y + Z + U
# @vectorize()
@vectorize(['float32(float32, float32, float32, float32, float32)'], target='cpu')
def addTogether(X, Y, Z, U, V):
    return X + Y + Z + U + V

