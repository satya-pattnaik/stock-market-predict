__author__ = 'satya'

from ReadInput import getClosingPrices
from Input_Variables import exponentialMovingAverage,inputRdp,trainingOutputRdp_5,scale,changeInPrice
import xlwt as xw
import os
import sklearn
from Output_Variables import reScale,getOutputEMA_3,getClosingPrice_5
import numpy as np
from GaussianKernel import getGaussianKernel
from MySVM import mySVR

myWorkbook = xw.Workbook(encoding='ascii')
my_sheet=myWorkbook.add_sheet('OUTPUT')



path = '/home/satya/Documents/dataset/MS'

#p = os.path.join(path,'Microsoft.xlsx')

myDict = getClosingPrices(path,'Microsoft.xlsx')
myKeys = myDict.keys()
myValues = myDict.values()
#print 'DEBUG::MY VALUES LENGTH::',myValues.__len__()
for key,value,rowi in zip(xrange(20,214,1),xrange(20,214,1),xrange(1,194,1)):
    my_sheet.write(rowi,1,myKeys[key])
    my_sheet.write(rowi,2,myValues[value])

SVM_trainingInput = []
SVM_trainingOutput = []

SVM_trainingOutputClasses = []

sumClosingPrices = 0
for iter in xrange(5,20):
    sumClosingPrices = sumClosingPrices+myValues[iter]

simpleMovingAverage = sumClosingPrices/15

emaYesterDay = simpleMovingAverage
print 'sma',simpleMovingAverage
emaList = []

for i in xrange(20,219):
    ema_15 = exponentialMovingAverage(myValues[i],15,emaYesterDay)
    emaList.append(ema_15)
    emaYesterDay= ema_15



print emaList,emaList.__len__()



ema_15_Input_List = []
rdp_5_Input_List = []
rdp_10_Input_List = []
rdp_15_Input_List = []
rdp_20_Input_List = []


for iterator,counter,rowit in zip(xrange(20,214,1),xrange(0,194,1),xrange(1,195,1)):
    #print 'DEBUG::',iterator

    SVM_rowInput = []
    ema_15_Input = myValues[iterator] - emaList[counter]
    my_sheet.write(rowit,3,float(ema_15_Input))
    ema_15_Input_List.append(ema_15_Input)
    #SVM_rowInput.append(ema_15_Input)

    rdp_5_Input = inputRdp(myValues[iterator],myValues[iterator-5])
    #SVM_rowInput.append(rdp_5_Input)
    my_sheet.write(rowit,4,ema_15_Input)
    rdp_5_Input_List.append(rdp_5_Input)

    rdp_10_Input = inputRdp(myValues[iterator],myValues[iterator-10])
    #SVM_rowInput.append(rdp_10_Input)
    my_sheet.write(rowit,5,ema_15_Input)
    rdp_10_Input_List.append(rdp_10_Input)

    rdp_15_Input = inputRdp(myValues[iterator],myValues[iterator-15])
    #SVM_rowInput.append(rdp_15_Input)
    my_sheet.write(rowit,6,ema_15_Input)
    rdp_15_Input_List.append(rdp_15_Input)

    rdp_20_Input = inputRdp(myValues[iterator],myValues[iterator-20])
    #SVM_rowInput.append(rdp_20_Input)
    my_sheet.write(rowit,7,ema_15_Input)
    rdp_20_Input_List.append(rdp_20_Input)

    #SVM_trainingInput.append(SVM_rowInput)

    #--------TRAINING OUTPUT---------

    #rdp_5_Output = trainingOutputRdp_5(myValues[iterator],myValues[iterator+5],myValues[iterator],myValues[iterator+4])
    #SVM_trainingOutput.append(rdp_5_Output)
#print 'DEBUG::',iterator,counter

for itr1,itr2 in zip(xrange(20,214,1),xrange(0,194,1)):
    if itr1 == 20:
        #print 'DEBUG:',itr1
        rdp_5_Output = trainingOutputRdp_5(myValues[itr1],myValues[itr1+5],simpleMovingAverage,emaList[itr2+4])
        SVM_trainingOutput.append(rdp_5_Output)

    else:
        rdp_5_Output = trainingOutputRdp_5(myValues[itr1],myValues[itr1+5],emaList[itr2-1],emaList[itr2+4])
        SVM_trainingOutput.append(rdp_5_Output)

print 'SVM TRAINING OUTPUT::',SVM_trainingOutput

'''scale(ema_15_Input_List)
scale(rdp_5_Input_List)
scale(rdp_10_Input_List)
scale(rdp_15_Input_List)
scale(rdp_20_Input_List)'''

#print 'DEBUG::EMA INPUTLIST LENGTH:',ema_15_Input_List.__len__()
for count in xrange(0,ema_15_Input_List.__len__()):
    rowWiseInputList = []
    rowWiseInputList.append(ema_15_Input_List[count])
    rowWiseInputList.append(rdp_5_Input_List[count])
    rowWiseInputList.append(rdp_10_Input_List[count])
    rowWiseInputList.append(rdp_15_Input_List[count])
    rowWiseInputList.append(rdp_20_Input_List[count])

    SVM_trainingInput.append(rowWiseInputList)

#print SVM_trainingInput
scale(SVM_trainingOutput)
#print 'THIS IS TARGET::',SVM_trainingOutput
o = os.path.join(path,'output.xlsx')

myWorkbook.save(o)

myTestingDict = getClosingPrices(path,'Testing.xlsx')
myTestingKeys = myTestingDict.keys()
myTestingValues = myTestingDict.values()
lastIndex = (myTestingValues.__len__())

testingClasses = []
testingClasses.append(1)
changeInPrice(myTestingValues,testingClasses)

emaLatestIndex = emaList.__len__()-1
emaLatest = emaList[emaLatestIndex]
#print 'DEBUG:LAST INDEX',lastIndex

emaTestList = []
emaOld = emaLatest
for i in xrange(0,lastIndex,1):
    ema_15 = exponentialMovingAverage(myTestingValues[i],15,emaOld)
    emaTestList.append(ema_15)
    emaOld= ema_15

ema_15_Test_List = []
rdp_5_Test_List = []
rdp_10_Test_List = []
rdp_15_Test_List = []
rdp_20_Test_List = []

for i1,i2 in zip(xrange(0,lastIndex),xrange(0,lastIndex)):

    ema_Test_Input = myTestingValues[i1]-emaTestList[i2]
    ema_15_Test_List.append(ema_Test_Input)

    if i1<5:
        rdp_5_test = inputRdp(myTestingValues[i1],myValues[i1+209])
        rdp_5_Test_List.append(rdp_5_test)

        rdp_10_test = inputRdp(myTestingValues[i1],myValues[i1+204])
        rdp_10_Test_List.append(rdp_10_test)

        rdp_15_test = inputRdp(myTestingValues[i1],myValues[i1+199])
        rdp_15_Test_List.append(rdp_15_test)

        rdp_20_Test = inputRdp(myTestingValues[i1],myValues[i1+194])
        rdp_20_Test_List.append(rdp_20_Test)

    elif i1<10:
        rdp_5_test = inputRdp(myTestingValues[i1],myTestingValues[i1-5])
        rdp_5_Test_List.append(rdp_5_test)

        rdp_10_test = inputRdp(myTestingValues[i1],myValues[i1+204])
        rdp_10_Test_List.append(rdp_10_test)

        rdp_15_test = inputRdp(myTestingValues[i1],myValues[i1+199])
        rdp_15_Test_List.append(rdp_15_test)

        rdp_20_Test = inputRdp(myTestingValues[i1],myValues[i1+194])
        rdp_20_Test_List.append(rdp_20_Test)

    elif i1<15:
        rdp_5_test = inputRdp(myTestingValues[i1],myTestingValues[i1-5])
        rdp_5_Test_List.append(rdp_5_test)

        rdp_10_test = inputRdp(myTestingValues[i1],myTestingValues[i1-10])
        rdp_10_Test_List.append(rdp_10_test)

        rdp_15_test = inputRdp(myTestingValues[i1],myValues[i1+199])
        rdp_15_Test_List.append(rdp_15_test)

        rdp_20_Test = inputRdp(myTestingValues[i1],myValues[i1+194])
        rdp_20_Test_List.append(rdp_20_Test)

    elif i1<20:
        rdp_5_test = inputRdp(myTestingValues[i1],myTestingValues[i1-5])
        rdp_5_Test_List.append(rdp_5_test)

        rdp_10_test = inputRdp(myTestingValues[i1],myTestingValues[i1-10])
        rdp_10_Test_List.append(rdp_10_test)

        rdp_15_test = inputRdp(myTestingValues[i1],myTestingValues[i1-15])
        rdp_15_Test_List.append(rdp_15_test)

        rdp_20_Test = inputRdp(myTestingValues[i1],myValues[i1+194])
        rdp_20_Test_List.append(rdp_20_Test)

    else:

        rdp_5_test = inputRdp(myTestingValues[i1],myTestingValues[i1-5])
        rdp_5_Test_List.append(rdp_5_test)

        rdp_10_test = inputRdp(myTestingValues[i1],myTestingValues[i1-10])
        rdp_10_Test_List.append(rdp_10_test)

        rdp_15_test = inputRdp(myTestingValues[i1],myTestingValues[i1-15])
        rdp_15_Test_List.append(rdp_15_test)

        rdp_20_Test = inputRdp(myTestingValues[i1],myTestingValues[i1-20])
        rdp_20_Test_List.append(rdp_20_Test)

print 'rdp_20_Test_List.__len__()',rdp_20_Test_List.__len__()
#scale(ema_15_Test_List)
#scale(rdp_5_Test_List)
#scale(rdp_10_Test_List)
#scale(rdp_15_Test_List)
#scale(rdp_20_Test_List)

SVR_TestList = []

for count1 in xrange(0,ema_15_Test_List.__len__()):
    rowWiseTestList = []
    rowWiseTestList.append(ema_15_Test_List[count1])
    rowWiseTestList.append(rdp_5_Test_List[count1])
    rowWiseTestList.append(rdp_10_Test_List[count1])
    rowWiseTestList.append(rdp_15_Test_List[count1])
    rowWiseTestList.append(rdp_20_Test_List[count1])

    SVR_TestList.append(rowWiseTestList)

print 'SVR_TESTLIST::',SVR_TestList
print

'''myKernel = getGaussianKernel(SVM_trainingInput,10)
myKernel = np.array(myKernel).tolist()
myList = []
myList = myKernel
print myList
print myList.__len__()'''

#myKernel = getGaussianKernel(SVM_trainingInput,10)

#temp = np.array(SVM_trainingInput)
#my_gamma =1/float(np.var(temp))

microsoft_SVR = sklearn.svm.SVR(kernel='rbf',gamma=(1)/float(10))#degree = 3,coef0 = 1)
microsoft_SVR.fit(SVM_trainingInput,SVM_trainingOutput)
#microsoft_SVR.fit(myKernel,SVM_trainingOutput)

#SVR_TestList_gaussianKernel = getGaussianKernel(SVR_TestList,10)

#print SVR_TestList_gaussianKernel

y = []
y = microsoft_SVR.predict(SVR_TestList)

reScale(y,np.min(y),np.max(y))
y = np.array(y).tolist()
print y

outList = []
outList = y

sum_3 = 0
for itrt1 in xrange(211,214,1):
    sum_3 = sum_3 + myValues[itr1]
SMA_3 = sum_3/3.0

ema_3_list = []
for itert1 in xrange(0,lastIndex):
    if itert1 == 0:
        ema_3 = exponentialMovingAverage(myTestingValues[itert1],3,SMA_3)
        ema_3_yester = ema_3
        ema_3_list.append(ema_3)
    else:
        ema_3 = exponentialMovingAverage(myTestingValues[itert1],3,ema_3_yester)
        ema_3_yester = ema_3
        ema_3_list.append(ema_3)

print 'EMA_3_LIST::',ema_3_list
print 'yListSize::',outList.__len__(),'EMA_3_LIST',ema_3_list.__len__()
lastIndex_1 = ema_3_list.__len__()-5

predictedPriceList = []

for it1 in xrange(0,lastIndex_1):
    ema_fifth = getOutputEMA_3(outList[it1],ema_3_list[it1])
    closingPriceFifthDay = getClosingPrice_5(ema_fifth,ema_3_list[it1+4])
    predictedPriceList.append(closingPriceFifthDay)

print predictedPriceList
print predictedPriceList.__len__(),testingClasses.__len__()

classifiedList = []
classifiedList.append(1)
changeInPrice(predictedPriceList,classifiedList)
print 'THIS IS ORIGINAL::',testingClasses
print 'THIS IS PREDICTED::',classifiedList