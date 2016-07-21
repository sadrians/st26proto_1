'''
Created on Jul 15, 2016

@author: ad
'''
import os 
import pprint
from django.conf import settings

from converter import St25To26Converter 
from size_estimation import ElementSizeCalculator
import converter_util as cu 

f5 = os.path.join(settings.BASE_DIR, 'seql_converter', 'st25parser', 
                  'testData', 'file5.txt') 

def calculateSizes(inFilePath, outDirPath):
    esc = ElementSizeCalculator(inFilePath)
    esc.writeSizes(outDirPath)
    print 'Element size file generated for ', inFilePath

# calculateSizes(f5, '.')

def countSt26ElementsFromCsvFile(inFilePath):
    res = {}
    esc = ElementSizeCalculator(inFilePath)
    rows = esc.generalInformationRows + esc.sequenceRows 
    
    for el in cu.TAG_LENGTH_ST26.keys():
        currentRows = [r for r in rows if r[6] == el]
        res[el] = len(currentRows)
    return res 

def countSt26ElementsFromXmlFile(inFilePath):
    res = {}
    with open(inFilePath, 'r') as f:
        xmlString = f.read()
        for el in cu.TAG_LENGTH_ST26.keys():
            if el[0].islower():
                currentElement = el
            else:
                currentElement = '</%s>' % el 
            res[el] = xmlString.count(currentElement)
    return res 

def convertFile(inFile, outDir):
    sc = St25To26Converter(inFile)
    sc.generateXmlFile(outDir)
    print 'Converted to xml file', inFile        

f5conv = 'file5_converted.xml'

def compareCounts():
    convertFile(f5, '.')
    calculateSizes(f5, '.')
    
    countCsv = countSt26ElementsFromCsvFile(f5)
    countXml = countSt26ElementsFromXmlFile(f5conv)
    
    for el in cu.TAG_LENGTH_ST26:
        c = countCsv[el]
        x = countXml[el]
        if c != x:
            print el
            print '%d in csv' %c, '%d in xml' %x 
    
# compareCounts()

def countTotals(inFilePath):
    esc = ElementSizeCalculator(inFilePath)
    rows = esc.generalInformationRows + esc.sequenceRows 
    
    for i in range(2,6):
        print cu.CSV_HEADER[i], sum([r[i] for r in rows]) 
        

countTotals(f5)





    



# countSt26ElementsFromCsvFile(f5)
# countSt26ElementsFromXmlFile(f5conv)


# d = r'/Users/ad/pyton/test/converter_in'
# l = [os.path.join(d, a) for a in os.listdir(d) if '.DS' not in a]
# 
# # pprint.pprint(l)
# 
# 
# for fp in l:
#     print fp
#     outf = fp.replace('.txt', '_lengths.txt')
#     outf = outf.replace('converter_in', 'converter_out')
#     writeSizes(fp, outf)





print 'Done'