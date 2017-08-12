# -*- coding: utf-8 -*-
# Iterating based on days.
from scrach import *

# total = {}
# # result = [improve, dropdown, noChange]
# TotalResult = [[], [], []]
# wlmiss = 0
# shpmiss = 0
# GAMA = 0.2


# ImprovePosition = 0
# DropDownPosition = 0
# ImprovePositionPercentage = 0.
# DropDownPositionPercentage = 0.
total = {}
# result = [improve, dropdown, noChange]
TotalResult = [[], [], []]

global scrach
global ImprovePosition
global ImprovePositionPercentage
global DropDownPosition
global DropDownPositionPercentage

# ======================================================================================================
# ======================================================================================================
# ======================================================================================================
for x in xrange(30):
    TrainingPath = 'NewDispatchedData/UserDataJan/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartJan/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowJan/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)

    TestingPath = 'NewDispatchedData/UserDataJan/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath)


TrainingPath = 'NewDispatchedData/UserDataJan/' + str(31) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartJan/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowJan/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)

TestingPath = 'NewDispatchedData/UserDataFeb/'+ str(1)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath)

for x in xrange(30):
    TrainingPath = 'NewDispatchedData/UserDataFeb/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartFeb/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowFeb/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)
    TestingPath = 'NewDispatchedData/UserDataFeb/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath)

TrainingPath = 'NewDispatchedData/UserDataFeb/' + str(31) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartFeb/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowFeb/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)
TestingPath = 'NewDispatchedData/UserDataMar/'+ str(1)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath)

for x in xrange(30):
    TrainingPath = 'NewDispatchedData/UserDataMar/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartMar/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowMar/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)
    TestingPath = 'NewDispatchedData/UserDataMar/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath)


TrainingPath = 'NewDispatchedData/UserDataMar/' + str(31) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartMar/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowMar/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)

TestingPath = 'NewDispatchedData/UserDataApr/'+ str(1)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath)

for x in xrange(30):
    TrainingPath = 'NewDispatchedData/UserDataApr/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartApr/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowApr/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)

    TestingPath = 'NewDispatchedData/UserDataApr/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath)

TrainingPath = 'NewDispatchedData/UserDataApr/' + str(31) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartApr/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowApr/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)

TestingPath = 'NewDispatchedData/UserDataMay/'+ str(1)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath)

for x in xrange(30):
    TrainingPath = 'NewDispatchedData/UserDataMay/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartMay/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowMay/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)
    TestingPath = 'NewDispatchedData/UserDataMay/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath)


TrainingPath = 'NewDispatchedData/UserDataMay/' + str(31) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartMay/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowMay/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)

TestingPath = 'NewDispatchedData/UserDataJune/'+ str(1)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath)

for x in xrange(29):
    TrainingPath = 'NewDispatchedData/UserDataJune/' + str(x+1) + "/"
    ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartJune/" + str(x+1)+ "/"
    WishlistTrainingPath = "NewDispatchedData/UserFollowJune/" + str(x+1)+ "/"
    total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)

    TestingPath = 'NewDispatchedData/UserDataJune/'+ str(x+2)+ "/"
    TotalResult = getTestData(total, TotalResult, TestingPath)

TrainingPath = 'NewDispatchedData/UserDataJune/' + str(30) + "/"
ShoppingCartTrainingPath = "NewDispatchedData/UserAddToCartJune/" + str(31)+ "/"
WishlistTrainingPath = "NewDispatchedData/UserFollowJune/" + str(31)+ "/"
total = buildModel(total, TrainingPath, ShoppingCartTrainingPath, WishlistTrainingPath, True)

TestingPath = 'NewDispatchedData/UserDataJune/'+ str(31)+ "/"
TotalResult = getTestData(total, TotalResult, TestingPath)


# ======================================================================================================
# ======================================================================================================
# ======================================================================================================





print "=========================================================="
print "================ The Final Result ========================"
print "=========================================================="
print "Improve  :", len(TotalResult[0]), "; Improve position: ", ImprovePosition, \
    ", Average: ", ImprovePosition / len(TotalResult[0]), \
    ", Improve percentage: ", ImprovePositionPercentage / len(TotalResult[0])
for each in TotalResult[0]:
    print each
print "=========================================================="
print "Dropdown :", len(TotalResult[1]), "; Dropdown position: ", DropDownPosition, \
    ", Average: ", DropDownPosition / len(TotalResult[1]), \
    ", Dropdown percentage: ", DropDownPositionPercentage / len(TotalResult[1])
for each in TotalResult[1]:
    print each
print "=========================================================="
print "No Change :", len(TotalResult[2])
print "GAMA: ", GAMA
