__author__ = 'satya'

import numpy as np

def exponentialMovingAverage(todaysClosingPrice,numberOfDays,EMA_yesterday):

    multiplier = (2) /float(numberOfDays + 1)
    EMA_today = float(todaysClosingPrice * multiplier) + float(EMA_yesterday*float(1-multiplier))
    return EMA_today

def inputRdp(todaysClosingPrice,oldClosingPrice):
    relativeDifferencePercentage = float(todaysClosingPrice-oldClosingPrice)/float(oldClosingPrice*100)

    return relativeDifferencePercentage

def trainingOutputRdp_5(todayClosingPrice,futureClosingPrice,yesterdayClosingPrice_EMA,yesterdayClosingPrice_5_EMA):

    EMA_today = exponentialMovingAverage(todayClosingPrice,3,yesterdayClosingPrice_EMA)
    EMA_fifthDay = exponentialMovingAverage(futureClosingPrice,3,yesterdayClosingPrice_5_EMA)

    RDP_5 = float(EMA_fifthDay-EMA_today)/float(EMA_today*100)

    return RDP_5

'''def scale(toBeScaled=[]):

    minimum,maximum = min(toBeScaled),max(toBeScaled)

    for iterator in xrange(0,toBeScaled.__len__()):
        toBeScaled[iterator] = float(toBeScaled[iterator]) - float(minimum)
        toBeScaled[iterator] = float(toBeScaled[iterator])/float(maximum-minimum)
        toBeScaled[iterator] = float(toBeScaled[iterator])*float(0.9-(-(0.9)))
        toBeScaled[iterator] = float(toBeScaled[iterator])+float(-0.9)

    print toBeScaled'''

def scale(toBeScaled=[]):
    minimum ,maximum = min(toBeScaled),max(toBeScaled)
    for iterator in xrange(0,toBeScaled.__len__()):
        difference1 = (toBeScaled[iterator])-(minimum)
        rangeOriginal = maximum-minimum
        result1 = float(difference1)/float(rangeOriginal)
        difference2 = 1.0-float(result1)
        toBeScaled[iterator] = float((-0.9)*float(difference2)) + float((0.9)*float(result1))

def changeInPrice(closingPriceList = [],outputClasses=[]):

    for iterator in xrange(1,closingPriceList.__len__()) :
        if(closingPriceList[iterator-1]>closingPriceList[iterator]):
            outputClasses.append(-1)
        else:
            outputClasses.append(+1)
