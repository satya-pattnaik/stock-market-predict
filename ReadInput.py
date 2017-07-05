__author__ = 'satya'

import xlrd as xl
import unicodedata
import os
from collections import OrderedDict

#path = '/home/satya/Documents/dataset/MS'

#p = os.path.join(path,'Microsoft.xlsx')

def getClosingPrices(path,fileName):

    myPath = os.path.join(path,fileName)
    microsoftWorksheet = xl.open_workbook(myPath)

    mySheet = microsoftWorksheet.sheets()[0]
    row = mySheet.row(0)
    rowSize = mySheet.nrows

    print rowSize

    dateList=[]
    closingPriceList=[]

    for iterator in xrange(1,(rowSize)):
        dateValue = mySheet.cell_value(iterator,0)
        dateList.append(unicodedata.normalize('NFKC',dateValue).encode('ascii','ignore'))
        closingPriceList.append(mySheet.cell_value(iterator,1))

    myDictionary = OrderedDict(zip(dateList,closingPriceList))

    return myDictionary


