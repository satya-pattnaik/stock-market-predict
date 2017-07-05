__author__ = 'satya'

from scipy.spatial.distance import cdist
import math

import numpy as np

def getGaussianKernel(inputArray,bandWidth):
    pairwiseDistance = (cdist(inputArray,inputArray, 'euclidean'))
    #pairwiseDistanceSquare = np.power(pairwiseDistance,2)
    #bandWidthSquare = math.pow(bandWidth,2)
    #myExpression = (-1)/float(bandWidthSquare*pairwiseDistanceSquare)
    #gaussianKernel = math.exp(myExpression)

    for rowIterator,eachRow in enumerate(pairwiseDistance):
        for columnIterator,eachColumn in enumerate(pairwiseDistance[rowIterator,:]):
            pairwiseDistance[rowIterator,columnIterator] = (np.power(pairwiseDistance[rowIterator,columnIterator],2)) * (float(-1))
            pairwiseDistance[rowIterator,columnIterator] = (pairwiseDistance[rowIterator,columnIterator]/float(np.power(bandWidth,2)))
            pairwiseDistance[rowIterator,columnIterator] = np.exp(pairwiseDistance[rowIterator,columnIterator])

    return pairwiseDistance


'''def getGaussianKernel(inputArray,bandwidth):
    inputArray = np.array(inputArray)
    numberOfRows,numberOfColumns = inputArray.shape
    print 'ROWS:',numberOfRows,'Columns:',numberOfColumns
    GaussMatrix = np.zeros(shape=(numberOfRows,numberOfRows))

    iter1 = 0
    for value_iter1 in inputArray:
        iter2 = 0
        for value_iter2 in inputArray:
            GaussMatrix[iter1,iter2] = Gaussian(value_iter1.T,value_iter2.T,bandwidth)
            iter2 = iter2+1
        iter1=iter1+1

    return GaussMatrix'''

'''def Gaussian(x,y,sig):
    value = math.exp((-((x-y)**2))/float(math.pow(sig,2)))
    return value


def getGaussianKernel(inputArray,bandWidth):
    #numberRows,numberColumns = inputArray.shape
    for iter1,valueRow in enumerate(inputArray):
        for iter2,valueCol in enumerate(inputArray):
            inputArray[iter1,iter2] = Gaussian(valueRow,valueCol,bandWidth)
    return inputArray'''