'''
Created on Jul 15, 2016

@author: ad
'''
import os 
import re 
import pprint
from django.conf import settings

from converter import St25To26Converter 
from size_estimation import ElementSizeCalculator
import converter_util as cu 

class FileSizeComparator(object):
    def __init__(self, inFilePath, outDirPath, xmlOutDirPath):
        self.inFilePath = inFilePath 
        self.outDirPath = outDirPath
        self.xmlOutDirPath = xmlOutDirPath
        
        self.esc = ElementSizeCalculator(self.inFilePath)
        self.csvFilePath = self.esc.writeSizes(self.outDirPath)
        
        sc = St25To26Converter(self.inFilePath)
        self.xmlFilePath = sc.generateXmlFile(self.xmlOutDirPath)

        self.cleanXmlFilePath = self.cleanAndWriteXmlFile() 
        
        self.listTotals()   
    
    def cleanAndWriteXmlFile(self):
        outFile = self.xmlFilePath.replace('.xml', '_clean.xml')
        with open(self.xmlFilePath, 'r') as f, open(outFile, 'w') as wr:
            clean = re.sub(r'\s+<', '<', f.read()).replace(os.linesep, '')
            wr.write(clean)
        print 'Generated clean xml file', outFile 
        return outFile 
    
    def listTotals(self):
        rows = self.esc.generalInformationRows + self.esc.sequenceRows 
        
        for i in range(2,6):
            print cu.CSV_HEADER[i], sum([r[i] for r in rows]) 
        print 'ST.25 txt file size:', os.path.getsize(self.inFilePath)
        
        f5convcl = 'file5_converted_clean.xml'
        with open(self.cleanXmlFilePath, 'r') as f:
            s = f.read()
            print 'chars in xml clean file:', len(s)
        print 'ST.26 xml file size:', os.path.getsize(f5convcl) 
             
    def compareElementsInCsvAndXmlFiles(self):
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
        
        countCsv = countSt26ElementsFromCsvFile(self.csvFilePath)
        countXml = countSt26ElementsFromXmlFile(self.xmlFilePath)
        
        for el in cu.TAG_LENGTH_ST26:
            c = countCsv[el]
            x = countXml[el]
            if c != x:
                print el
                print '%d in csv' %c, '%d in xml' %x 


# ==================== main =========================
# f5 = os.path.join(settings.BASE_DIR, 'seql_converter', 'st25parser', 
#                   'testData', 'file5.txt') 
# 
# outDirPath = r'/Users/ad/pyton/test/st26fileSize/stats'
# xmlOutDirPath = r'/Users/ad/pyton/test/st26fileSize/converter_out'
# 
# fsc = FileSizeComparator(f5, outDirPath, xmlOutDirPath)
# =====================================================


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
