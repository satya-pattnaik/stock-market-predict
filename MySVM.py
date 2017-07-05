__author__ = 'satya'

from sklearn.svm import SVR

def mySVR(trainingData,targetData):

    microsoft_SVR = SVR
    microsoft_SVR.fit(trainingData,targetData)
    return microsoft_SVR

