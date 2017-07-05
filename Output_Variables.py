__author__ = 'satya'

def reScale(toBeRescaled,minimum,maximum):

    #minimum,maximum = min(toBeScaled),max(toBeScaled)

    for iterator in xrange(0,toBeRescaled.__len__()):
        '''toBeScaled[iterator] = float(toBeScaled[iterator]) - float(minimum)
        toBeScaled[iterator] = float(toBeScaled[iterator])/float(maximum-minimum)
        toBeScaled[iterator] = float(toBeScaled[iterator])*float(0.9-(-(0.9)))
        toBeScaled[iterator] = float(toBeScaled[iterator])+float(-0.9)'''

        toBeRescaled[iterator] = float(toBeRescaled[iterator]) - float(-0.9)
        toBeRescaled[iterator] = float(toBeRescaled[iterator])/float(0.9-(-(0.9)))
        toBeRescaled[iterator] = float(toBeRescaled[iterator])*float(maximum-minimum)
        toBeRescaled[iterator] = float(toBeRescaled[iterator])+float(minimum)

def getOutputEMA_3(output,EMA_Today):

    ema_FifhDay_3 = float(output*float(EMA_Today*3)) + float(EMA_Today)
    return ema_FifhDay_3

def getClosingPrice_5(EMA_FifthDay_3,EMA_yesterday):

    multiplier = (2) /float(3 + 1)

    closingPrice = float(float(EMA_FifthDay_3)-(float(EMA_yesterday)*float(1-multiplier))) / float(multiplier)

    return closingPrice

'''def scale(toBeScaled=[]):
    minimum ,maximum = min(toBeScaled),max(toBeScaled)
    for iterator in xrange(0,toBeScaled.__len__()):
        difference1 = (toBeScaled[iterator])-(minimum)
        rangeOriginal = maximum-minimum
        result1 = float(difference1)/float(rangeOriginal)
        difference2 = 1.0-float(result1)
        toBeScaled[iterator] = float((-0.9)*float(difference2)) + float((0.9)*float(result1))

def rescale(toBeRescaled=[],minimum,maximum):
    for iterator in xrange(0,toBeRescaled.__len__()):
        expression_1 ='''

def calculateCorrectPredictions(expectedPredictions=[],predicted=[]):
    correctCount =0
    for iterator in xrange(0,expectedPredictions.__len__()):
        if expectedPredictions[iterator] == predicted[iterator]:
            correctCount = correctCount+1

    correctProbability = correctCount/float(expectedPredictions.__len__())
    return correctCount,correctProbability