__author__ = 'satya'

from ReadInput import getClosingPrices
from Input_Variables import exponentialMovingAverage,inputRdp,trainingOutputRdp_5,changeInPrice,scale
from sklearn import svm,preprocessing
import numpy as np
from Output_Variables import calculateCorrectPredictions

pathOfMicrosoft = '/home/satya/Documents/dataset/MS'

datePriceDictionary = getClosingPrices(pathOfMicrosoft,'MicrosoftTraining.xlsx')
initialPriceDictionary = getClosingPrices(pathOfMicrosoft,'Training.xlsx')
last5PriceDictionary = getClosingPrices(pathOfMicrosoft,'Last5Days.xlsx')
dateList = datePriceDictionary.keys()
closingPriceList = datePriceDictionary.values()
initialPriceValues = initialPriceDictionary.values()

SVM_trainingInput = []
SVM_trainingOutputValues = []
SVM_trainingOutputClasses = []
SVM_trainingOutputClasses.append(1)

last5List = last5PriceDictionary.values()

changeInPrice(closingPriceList,SVM_trainingOutputClasses)

sumClosingPrices = 0.0
for iter in xrange(5,20):
    sumClosingPrices = sumClosingPrices+float(initialPriceValues[iter])

simpleMovingAverage = sumClosingPrices/float(15)

emaYesterDay = simpleMovingAverage
emaList = []

for i in xrange(0,closingPriceList.__len__()):
    ema_15 = exponentialMovingAverage(closingPriceList[i],15,emaYesterDay)
    emaList.append(ema_15)
    emaYesterDay= ema_15

emaLastList = []
for j in xrange(0,5):
    ema_15Last = exponentialMovingAverage(last5List[j],15,emaYesterDay)
    emaLastList.append(ema_15Last)

ema_15_Input_List = []
rdp_5_Input_List = []
rdp_10_Input_List = []
rdp_15_Input_List = []
rdp_20_Input_List = []

for iterator in xrange(0,closingPriceList.__len__()):

    ema15Input = closingPriceList[iterator] - emaList[iterator]
    ema_15_Input_List.append(ema15Input)

    if iterator<5:
        rdp_5_Input = inputRdp(closingPriceList[iterator],initialPriceValues[iterator+15])
        rdp_5_Input_List.append(rdp_5_Input)

        rdp_10_Input = inputRdp(closingPriceList[iterator],initialPriceValues[iterator+10])
        rdp_10_Input_List.append(rdp_10_Input)

        rdp_15_Input = inputRdp(closingPriceList[iterator],initialPriceValues[iterator+5])
        rdp_15_Input_List.append(rdp_15_Input)

        rdp_20_Input = inputRdp(closingPriceList[iterator],initialPriceValues[iterator])
        rdp_20_Input_List.append(rdp_20_Input)

    elif iterator<10:

        rdp_5_Input = inputRdp(closingPriceList[iterator],closingPriceList[iterator-5])
        rdp_5_Input_List.append(rdp_5_Input)

        rdp_10_Input = inputRdp(closingPriceList[iterator],initialPriceValues[iterator+10])
        rdp_10_Input_List.append(rdp_10_Input)

        rdp_15_Input = inputRdp(closingPriceList[iterator],initialPriceValues[iterator+5])
        rdp_15_Input_List.append(rdp_15_Input)

        rdp_20_Input = inputRdp(closingPriceList[iterator],initialPriceValues[iterator])
        rdp_20_Input_List.append(rdp_20_Input)

    elif iterator<15:

        rdp_5_Input = inputRdp(closingPriceList[iterator],closingPriceList[iterator-5])
        rdp_5_Input_List.append(rdp_5_Input)

        rdp_10_Input = inputRdp(closingPriceList[iterator],closingPriceList[iterator-10])
        rdp_10_Input_List.append(rdp_10_Input)

        rdp_15_Input = inputRdp(closingPriceList[iterator],initialPriceValues[iterator+5])
        rdp_15_Input_List.append(rdp_15_Input)

        rdp_20_Input = inputRdp(closingPriceList[iterator],initialPriceValues[iterator])
        rdp_20_Input_List.append(rdp_20_Input)

    elif iterator<20:

        rdp_5_Input = inputRdp(closingPriceList[iterator],closingPriceList[iterator-5])
        rdp_5_Input_List.append(rdp_5_Input)

        rdp_10_Input = inputRdp(closingPriceList[iterator],closingPriceList[iterator-10])
        rdp_10_Input_List.append(rdp_10_Input)

        rdp_15_Input = inputRdp(closingPriceList[iterator],closingPriceList[iterator-15])
        rdp_15_Input_List.append(rdp_15_Input)

        rdp_20_Input = inputRdp(closingPriceList[iterator],initialPriceValues[iterator])
        rdp_20_Input_List.append(rdp_20_Input)

    else:

        rdp_5_Input = inputRdp(closingPriceList[iterator],closingPriceList[iterator-5])
        rdp_5_Input_List.append(rdp_5_Input)

        rdp_10_Input = inputRdp(closingPriceList[iterator],closingPriceList[iterator-10])
        rdp_10_Input_List.append(rdp_10_Input)

        rdp_15_Input = inputRdp(closingPriceList[iterator],closingPriceList[iterator-15])
        rdp_15_Input_List.append(rdp_15_Input)

        rdp_20_Input = inputRdp(closingPriceList[iterator],closingPriceList[iterator-20])
        rdp_20_Input_List.append(rdp_20_Input)

closingPriceListLength = closingPriceList.__len__()

for itr1 in xrange(0,closingPriceListLength):
    if itr1 == 0:
        rdp_5_Output = trainingOutputRdp_5(closingPriceList[itr1],closingPriceList[itr1+5],simpleMovingAverage,emaList[itr1+4])
        SVM_trainingOutputValues.append(rdp_5_Output)

    elif itr1 < (closingPriceListLength-5):
        rdp_5_Output = trainingOutputRdp_5(closingPriceList[itr1],closingPriceList[itr1+5],emaList[itr1-1],emaList[itr1+4])
        SVM_trainingOutputValues.append(rdp_5_Output)

    else:
        rdp_5_Output = trainingOutputRdp_5(closingPriceList[itr1],last5List[abs(closingPriceListLength-iterator-5)],emaList[itr1-1],emaLastList[abs(closingPriceListLength-iterator-5)])
        SVM_trainingOutputValues.append(rdp_5_Output)

print 'DEBUGGING:',ema_15_Input_List.__len__()

'''preprocessing.scale(ema_15_Input_List)
preprocessing.scale(rdp_5_Input_List)
preprocessing.scale(rdp_10_Input_List)
preprocessing.scale(rdp_15_Input_List)
preprocessing.scale(rdp_20_Input_List)'''

for count in xrange(0,ema_15_Input_List.__len__()):
    rowWiseInputList = []
    rowWiseInputList.append(ema_15_Input_List[count])
    rowWiseInputList.append(rdp_5_Input_List[count])
    rowWiseInputList.append(rdp_10_Input_List[count])
    rowWiseInputList.append(rdp_15_Input_List[count])
    rowWiseInputList.append(rdp_20_Input_List[count])

    SVM_trainingInput.append(rowWiseInputList)

testingDictionary = getClosingPrices(pathOfMicrosoft,'MicrosoftTesting.xlsx')
testingInputValues = testingDictionary.values()

emaTestList = []
emaOld=emaList[emaList.__len__()-1]

for it in xrange(0,testingInputValues.__len__()):
    emaTest = exponentialMovingAverage(testingInputValues[it],15,emaOld)
    emaTestList.append(emaTest)
    emaOld=emaTest

ema_15_Test_List = []
rdp_5_Test_List = []
rdp_10_Test_List = []
rdp_15_Test_List = []
rdp_20_Test_List = []

closingPricesLast_20_daysList = []
for itr2 in xrange(closingPriceList.__len__()-20,closingPriceList.__len__()):
    closingPricesLast_20_daysList.append(closingPriceList[itr2])

for iterator_1 in xrange(0,testingInputValues.__len__()):
    ema_15TestInput = testingInputValues[iterator_1] - emaTestList[iterator_1]
    ema_15_Test_List.append(ema_15TestInput)

    if iterator_1 < 5:
        rdp_5_test = inputRdp(testingInputValues[iterator_1],closingPricesLast_20_daysList[iterator_1+15])
        rdp_5_Test_List.append(rdp_5_test)

        rdp_10_test = inputRdp(testingInputValues[iterator_1],closingPricesLast_20_daysList[iterator_1+10])
        rdp_10_Test_List.append(rdp_10_test)

        rdp_15_test = inputRdp(testingInputValues[iterator_1],closingPricesLast_20_daysList[iterator_1+5])
        rdp_15_Test_List.append(rdp_15_test)

        rdp_20_Test = inputRdp(testingInputValues[iterator_1],closingPricesLast_20_daysList[iterator_1])
        rdp_20_Test_List.append(rdp_20_Test)

    elif iterator_1<10:

        rdp_5_test = inputRdp(testingInputValues[iterator_1],testingInputValues[iterator_1-5])
        rdp_5_Test_List.append(rdp_5_test)

        rdp_10_test = inputRdp(testingInputValues[iterator_1],closingPricesLast_20_daysList[iterator_1+10])
        rdp_10_Test_List.append(rdp_10_test)

        rdp_15_test = inputRdp(testingInputValues[iterator_1],closingPricesLast_20_daysList[iterator_1+5])
        rdp_15_Test_List.append(rdp_15_test)

        rdp_20_Test = inputRdp(testingInputValues[iterator_1],closingPricesLast_20_daysList[iterator_1])
        rdp_20_Test_List.append(rdp_20_Test)

    elif iterator_1<15:
        rdp_5_test = inputRdp(testingInputValues[iterator_1],testingInputValues[iterator_1-5])
        rdp_5_Test_List.append(rdp_5_test)

        rdp_10_test = inputRdp(testingInputValues[iterator_1],testingInputValues[iterator_1-10])
        rdp_10_Test_List.append(rdp_10_test)

        rdp_15_test = inputRdp(testingInputValues[iterator_1],closingPricesLast_20_daysList[iterator_1+5])
        rdp_15_Test_List.append(rdp_15_test)

        rdp_20_Test = inputRdp(testingInputValues[iterator_1],closingPricesLast_20_daysList[iterator_1])
        rdp_20_Test_List.append(rdp_20_Test)

    elif iterator_1<20:
        rdp_5_test = inputRdp(testingInputValues[iterator_1],testingInputValues[iterator_1-5])
        rdp_5_Test_List.append(rdp_5_test)

        rdp_10_test = inputRdp(testingInputValues[iterator_1],testingInputValues[iterator_1-10])
        rdp_10_Test_List.append(rdp_10_test)

        rdp_15_test = inputRdp(testingInputValues[iterator_1],testingInputValues[iterator_1-15])
        rdp_15_Test_List.append(rdp_15_test)

        rdp_20_Test = inputRdp(testingInputValues[iterator_1],closingPricesLast_20_daysList[iterator_1])
        rdp_20_Test_List.append(rdp_20_Test)

    else:
        rdp_5_test = inputRdp(testingInputValues[iterator_1],testingInputValues[iterator_1-5])
        rdp_5_Test_List.append(rdp_5_test)

        rdp_10_test = inputRdp(testingInputValues[iterator_1],testingInputValues[iterator_1-10])
        rdp_10_Test_List.append(rdp_10_test)

        rdp_15_test = inputRdp(testingInputValues[iterator_1],testingInputValues[iterator_1-15])
        rdp_15_Test_List.append(rdp_15_test)

        rdp_20_Test = inputRdp(testingInputValues[iterator_1],testingInputValues[iterator_1-20])
        rdp_20_Test_List.append(rdp_20_Test)

'''preprocessing.scale(ema_15_Test_List)
preprocessing.scale(rdp_5_Test_List)
preprocessing.scale(rdp_10_Test_List)
preprocessing.scale(rdp_15_Test_List)
preprocessing.scale(rdp_20_Test_List)'''

#-------------------------------------------------------
minMaxScaler = preprocessing.MinMaxScaler(feature_range=(-0.9,0.9))
minMaxScaler.fit(SVM_trainingInput)
SVM_trainingInputScaled = minMaxScaler.transform(SVM_trainingInput)
print 'SVM_trainingInputScaled' ,SVM_trainingInputScaled

#--------------------------------------------------------
SVR_TestList = []

for count1 in xrange(0,ema_15_Test_List.__len__()):
    rowWiseTestList = []
    rowWiseTestList.append(ema_15_Test_List[count1])
    rowWiseTestList.append(rdp_5_Test_List[count1])
    rowWiseTestList.append(rdp_10_Test_List[count1])
    rowWiseTestList.append(rdp_15_Test_List[count1])
    rowWiseTestList.append(rdp_20_Test_List[count1])

    SVR_TestList.append(rowWiseTestList)

SVR_TestListExpectedOutput = []
SVR_TestListExpectedOutput.append(1)
changeInPrice(testingInputValues,SVR_TestListExpectedOutput)
#----------------------------------------------Classification----------------------------------------------

#temp = np.array(SVM_trainingInput)
#myGamma = 1/float(np.power(np.var(SVM_trainingInput),2))

#------------------------------------------------------------
minMaxScaler.fit(SVR_TestList)
SVR_TestListScaled = minMaxScaler.transform(SVR_TestList)

#------------------------------------------------------------
classifier = svm.SVC(kernel='rbf',gamma=1/10.0)
classifier.fit(SVM_trainingInputScaled,SVM_trainingOutputClasses)

y = classifier.predict(SVR_TestList)

regression = svm.SVR(kernel='poly',coef0=3,degree=1)#(kernel='rbf',gamma=1/1000.0)
scale(SVM_trainingOutputValues)
regression.fit(SVM_trainingInput,SVM_trainingOutputValues)
print 'SVROUTPUTTRAINING::',SVM_trainingOutputValues
print 'SVRTEST::',SVR_TestList
z = regression.predict(SVR_TestList)
z = np.array(z).tolist()

print z
predictedList = []
predictedList.append(1)
changeInPrice(z,predictedList)

print 'SVR_TestListLength:',SVR_TestList.__len__()
print 'Expected Value:',SVR_TestListExpectedOutput
print 'Predicted::',predictedList

numberOfCorrectPredictions,probabiltyOfCorrectPredictions = calculateCorrectPredictions(SVR_TestListExpectedOutput,predictedList)
print 'NUMBER OF CORRECT CLASSIFICATIONS::',numberOfCorrectPredictions
print 'PROBABILITY OF CORRECT CLASSIFICATION::',probabiltyOfCorrectPredictions